"""Module/feature/mainline curricula projected onto the native task ledger.

Initial grouping is an inspectable proposal. Reviewed discoveries refine it;
source functions, graph nodes and reading chunks never become curriculum tasks.
"""
from collections import Counter,defaultdict
from copy import deepcopy
import csv
from fnmatch import fnmatchcase
from html import escape
import io
import json
from pathlib import PurePosixPath
import re

from .store import atomic_write,canonical,digest,identity,now,require
from . import study,whole

DEFAULT={'max_files':24,'max_source_bytes':240000,'region_lines':200}
OUTPUTS=['behavior_and_conditions','state_producers_consumers','resource_and_error_paths',
         'cross_module_impacts','test_oracle','operations_observations','explicit_unknowns']
TOPICS=[
 ('cost','代价与基数估算',['*cost*','*selectiv*','*selfunc*','*clausesel*','*statistics*']),
 ('joins','连接路径与连接约束',['*join*','*geqo*']),
 ('plans','计划生成与计划接口',['*plan*','*pathkey*']),
 ('cache','缓存、失效与复用',['*cache*','*inval*','*gplan*']),
 ('transactions','事务、可见性与结束处理',['*xact*','*snapshot*','*visibility*']),
 ('resources','资源寿命与错误清理',['*mem*','*resowner*','*elog*','*error*']),
 ('configuration','配置注册与生效',['*guc*','*config*']),
 ('recovery','持久化与恢复',['*xlog*','*wal*','*redo*','*recovery*']),
]


def current(store,required=False):
    key=store.get_meta('curriculum_head');value=store.get_meta(key) if key else None
    if value and (value['snapshot']!=study.current(store)['snapshot'] or value['plan_id']!=study.current(store)['id']):value=None
    require(value or not required,'Initialize a module/feature curriculum through start')
    return value


def _topic(module,key):
    stem=PurePosixPath(key).stem.casefold()
    for code,title,patterns in TOPICS:
        if any(fnmatchcase(stem,pattern) for pattern in patterns):return code,title,'filename_behavior_candidate'
    if '/test' in module or '/regress' in module or '/expected' in module or '/sql' in module:
        token=re.sub(r'[_-]?\d+$','',stem).split('_')[0] or 'regression'
        return 'test-'+token,'回归主题：'+token,'paired_test_name_candidate'
    return 'mechanism','模块实现、接口与状态机制','module_scope_candidate'


def _modules_for_feature(feature,modules,aliases):
    hint=feature.get('module_hint')
    hints=hint if isinstance(hint,list) else [hint] if hint else []
    matched={m for m in modules for h in hints if h and (m==h or m.startswith(str(h).rstrip('/')+'/') or str(h).startswith(m.rstrip('/')+'/') or m.endswith('/'+str(h)))}
    if matched:return sorted(matched),'provided_module_hint'
    terms=[str(feature.get('name','')).casefold(),*[str(t).casefold() for t in feature.get('aliases',[])]]
    matched=set()
    for m in modules:
        leaf=m.rsplit('/',1)[-1].casefold();names=[leaf,*aliases.get(leaf,[])]
        if any(len(t)>2 and any(t==n.casefold() or (len(n)>3 and n.casefold() in t) for n in names) for t in terms):matched.add(m)
    return sorted(matched),'name_or_alias_candidate' if matched else 'not_located'


def _packages(plan,assets,features,policy):
    output=[]
    for module,info in sorted(plan['modules'].items()):
        groups=defaultdict(list);labels={};basis={}
        for key in info['files']:
            topic,title,why=_topic(module,key);groups[topic].append(key);labels[topic]=title;basis[topic]=why
        for topic,keys in sorted(groups.items()):
            chunks=[];chunk=[];size=0
            for key in sorted(keys):
                weight=assets[key].get('bytes',0)
                if chunk and (len(chunk)>=policy['max_files'] or size+weight>policy['max_source_bytes']):chunks.append(chunk);chunk=[];size=0
                chunk.append(key);size+=weight
            if chunk:chunks.append(chunk)
            for index,selected in enumerate(chunks,1):
                fids=[f['id'] for f in features if module in f.get('module_candidates',[])]
                title=labels[topic]+(f' / 分批{index}' if len(chunks)>1 else '')
                output.append({'id':identity('package',[plan['id'],module,topic,index]),'module':module,'title':title,
                    'topic':topic,'grouping_basis':basis[topic],'scope_status':'candidate_requires_source_review',
                    'question':f'{title}：解释行为、入口、状态生产消费、构建条件、异常清理、跨模块影响、测试依据与可观测性。',
                    'files':selected,'cpp_files':sum(PurePosixPath(k).suffix.lower() in {'.cpp','.cc','.cxx','.c++'} for k in selected),
                    'feature_ids':fids,'mainline_ids':[],'depends_on':[info['task']],
                    'budget':{'files':len(selected),'source_bytes':sum(assets[k].get('bytes',0) for k in selected),
                              'max_read_lines':policy['region_lines'],'large_file_requires_chunks':any(assets[k].get('bytes',0)>policy['max_source_bytes'] for k in selected)},
                    'expected_outputs':OUTPUTS,'tasks':[]})
    return output


def ensure(store,inputs=None,policy=None):
    plan=study.current(store);program=whole.current(store)
    options={**DEFAULT,**(policy or {})}
    require(not set(options)-set(DEFAULT),'Unknown curriculum policy option')
    require(type(options['max_files']) is int and 2<=options['max_files']<=80,'Curriculum max_files must be 2..80')
    require(type(options['max_source_bytes']) is int and 10000<=options['max_source_bytes']<=2000000,'Invalid curriculum byte budget')
    require(type(options['region_lines']) is int and 20<=options['region_lines']<=400,'Invalid source-region line budget')
    manifest=inputs or store.get_meta('learning_inputs',{})
    cid=identity('curriculum',[program['id'],manifest.get('digest'),options])
    old=current(store)
    from . import implementation
    if old and old['id']==cid:
        implementation.ensure(store,program,region_lines=options['region_lines'])
        return old
    assets={r['key']:json.loads(r['data']) for r in store.db.execute("SELECT key,data FROM assets WHERE snapshot=? AND kind IN ('source','document')",(plan['snapshot'],))}
    features=deepcopy(manifest.get('features',[]))
    for feature in features:
        choices,why=_modules_for_feature(feature,plan['modules'],plan['product_adapter'].get('aliases',{}))
        feature.update(module_candidates=choices,mapping_basis=why,mapping_status='candidate' if choices else 'not_located')
    packages=_packages(plan,assets,features,options)
    by_owner={k:m for m,info in plan['modules'].items() for k in info['files']}
    mainlines=[]
    for template in program['templates']:
        modules=sorted({by_owner[k] for k in template['seed_files'] if k in by_owner})
        item={k:deepcopy(template.get(k)) for k in ('id','title','task','kind','question','scope_status')}
        item.update(modules=modules,source_files=template['seed_files'],status='scope_candidate_not_knowledge')
        mainlines.append(item)
    for package in packages:
        package['mainline_ids']=[item['id'] for item in mainlines if package['module'] in item['modules']]
    value={'schema':'module-feature-curriculum/v1','id':cid,'plan_id':plan['id'],'program':program['id'],
        'snapshot':plan['snapshot'],'run':plan['run'],'profile':plan['profile'],'policy':options,'created':now(),
        'input_digest':manifest.get('digest'),'input_summary':manifest.get('summary',{}),'input_issues':manifest.get('issues',[]),
        'features':features,'mainlines':mainlines,'packages':packages,
        'domains':program['policy']['domains'],'planning_status':'candidate_plan_not_semantic_completion'}
    value['revision']=digest(value)
    implementation.ensure(store,program,region_lines=options['region_lines'])
    with store.transaction():
        store.set_meta(cid,value);store.set_meta('curriculum_head',cid)
        store.event('curriculum_created',{'curriculum':cid,'modules':len(plan['modules']),'packages':len(packages),'functions_as_tasks':False})
    return value


def inventory_ready(store,module):
    p=whole.current(store);plan=study.current(store)
    allowed=set(plan['modules'].get(module,{}).get('files',[]))
    _,inventories,_=whole._report_state(store,p)
    report=inventories.get(module)
    return bool(report and allowed<=set(r['asset'] for r in report['progress'].get('assets',[])))


def ready_modules(store,program=None,plan=None):
    """Resolve inventory once per advance, not once per work package."""
    program=program or whole.current(store);plan=plan or study.current(store)
    _,inventories,_=whole._report_state(store,program)
    return {module for module,report in inventories.items() if module in plan['modules']
            and set(plan['modules'][module]['files'])<=set(r['asset'] for r in report['progress'].get('assets',[]))}


def prerequisites(store,task):
    """Scope acceptance and published knowledge are distinct prerequisites."""
    if not current(store):return []
    from .planner import task_status
    blockers=[]
    for dep in task.get('dependencies',[]):
        d=task_status(store,dep)
        if d['kind']=='module_survey' and not inventory_ready(store,d['bundle'].get('module')):
            blockers.append({'kind':'inventory_incomplete','task':dep})
        elif d['kind']!='module_survey' and not whole._task_published(store,dep):
            blockers.append({'kind':'knowledge_not_published','task':dep})
    needed=task['bundle'].get('requires_knowledge',[])
    units=whole.reference_units(store,needed)
    for uid in needed:
        if uid not in units or not whole._applicable(store,units[uid],whole.current(store)):
            blockers.append({'kind':'required_knowledge_missing_or_stale','unit':uid})
    return blockers


def advance(store,max_tasks=8):
    value=current(store)
    if not value:return {'created_or_reused':[]}
    require(1<=max_tasks<=500,'Bound curriculum batch to 1..500 tasks')
    from .planner import create_task
    plan=study.current(store);program=whole.current(store)
    ready=ready_modules(store,program,plan)
    if not ready:return {'created_or_reused':[],'stalled':[],'automatic_knowledge_acceptance':False}
    states={r['asset']:r for r in whole._rows(store,program)}
    from . import implementation
    regions=implementation.evaluated(store,program);unclosed=defaultdict(list)
    for row in regions.values():
        if row['state'] not in {'explained','no_implementation'}:unclosed[row['asset']].append(row)
    results=[];stalled=[];changed=False
    with store.transaction():
        value=deepcopy(current(store,True))
        for package in value['packages']:
            if len(results)>=max_tasks:break
            module=package['module']
            if module not in ready:continue
            pending=store.db.execute("SELECT id FROM tasks WHERE snapshot=? AND run=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.module')=? AND status IN ('queued','leased','submitted','needs_research') AND kind<>'module_survey'",(plan['snapshot'],plan['run'],plan['id'],module)).fetchall()
            # Do not compete with reviewed mechanism discoveries or an in-flight package.
            if pending:continue
            remaining=[key for key in package['files'] if states[key]['state'] not in {'studied','supporting','input_exclusion'} or unclosed.get(key)]
            if not remaining:continue
            cursor=[(key,states[key]['state'],(states[key].get('disposition') or {}).get('unit_hashes',{}),
                     [(r['item'],r['state'],(r['disposition'] or {}).get('unit_hashes',{})) for r in unclosed.get(key,[])]) for key in remaining]
            b={'plan_id':plan['id'],'program_id':program['id'],'module':module,'package_id':package['id'],
               'curriculum':value['id'],'feature_ids':package['feature_ids'],'mainline_ids':package['mainline_ids'],
               'question':package['question'],'selected_files':remaining,'source_anchor_refs':[],
               'expected_outputs':package['expected_outputs'],'budget':package['budget'],'remaining_scope_digest':digest(cursor),
               'requires_knowledge':package.get('requires_knowledge',[])}
            tid=create_task(store,snapshot=plan['snapshot'],run=plan['run'],profile=plan['profile'],kind='feature_research',bundle=b,dependencies=package['depends_on'])
            state=store.db.execute('SELECT status FROM tasks WHERE id=?',(tid,)).fetchone()[0]
            if tid not in package['tasks']:package['tasks'].append(tid);changed=True
            if state in {'queued','needs_research'}:results.append({'task':tid,'kind':'feature_research','package':package['id']})
            elif state=='accepted':stalled.append({'module':module,'package':package['id'],'task':tid,'reason':'No new reviewed source coverage; refine knowledge or resolve gaps before repeating'})
        if changed:store.set_meta(value['id'],value)
    return {'created_or_reused':results,'stalled':stalled,'automatic_knowledge_acceptance':False}


def feature_status(store,module=None):
    value=current(store,True);program=whole.current(store)
    reports,_,_=whole._report_state(store,program);decisions={}
    for record in reports:
        for row in record['progress'].get('feature_mappings',[]):decisions[row['feature_id']]=row
    out=[]
    for feature in value['features']:
        decision=decisions.get(feature['id']);state=feature.get('status','not_located')
        if state not in {'duplicate','ambiguous','invalid'}:state='not_located'
        if decision:
            state=decision['state']
            if state=='mapped':
                units=whole.reference_units(store,decision.get('unit_ids',[]))
                from .knowledge import content_hash
                if not all(uid in units and whole._applicable(store,units[uid],program) and content_hash(units[uid])==decision.get('unit_hashes',{}).get(uid) for uid in decision.get('unit_ids',[])):state='pending_knowledge'
        row={**feature,'state':state,'reviewed_mapping':decision}
        related=set(feature.get('module_candidates',[]))|set((decision or {}).get('modules',[]))
        if module is None or module in related:out.append(row)
    return out


def validate_feature_mappings(store,program,task,rows,available,reads):
    from .knowledge import content_hash
    require(isinstance(rows,list) and len(rows)<=2000,'Feature mappings must be a bounded list')
    features={f['id']:f for f in current(store,True)['features']};out=[]
    for source in rows:
        row=dict(source);require(row.get('feature_id') in features,'Unknown historical feature ID')
        require(row.get('state') in {'mapped','ambiguous','not_located','out_of_scope'},'Invalid feature mapping state')
        require(row.get('reason') and row.get('evidence_refs') and set(row['evidence_refs'])<=reads,'Feature mapping requires actual source/manual evidence and a reason')
        modules=row.get('modules',[])
        require(isinstance(modules,list) and set(modules)<=set(study.current(store)['modules']),'Unknown feature implementation module')
        if task['bundle'].get('module'):require(task['bundle']['module'] in modules,'Mapping must include the investigating module')
        if row['state']=='mapped':require(row.get('unit_ids') and set(row['unit_ids'])<=set(available),'Mapped feature needs real mechanism knowledge')
        if row['state']=='mapped':
            ids=row['unit_ids']
            require(any(available[uid].get('kind') in {'mechanism','claim','contract','flow','requirement'} for uid in ids),'Mapped feature needs substantive mechanism knowledge')
            cited={ref for uid in ids for ref in available[uid].get('source_refs',[])}
            require(cited & set(row['evidence_refs']),'Feature mapping evidence must support the mapped knowledge')
            row['unit_hashes']={uid:content_hash(available[uid]) for uid in ids}
        out.append(row)
    return out


def status(store,module=None):
    value=current(store,True);plan=study.current(store)
    modules=plan['modules']
    if module:require(module in modules,'Unknown curriculum module');modules={module:modules[module]}
    features=feature_status(store,module)
    packages=[p for p in value['packages'] if not module or p['module']==module]
    cpp={k for info in modules.values() for k in info['files'] if PurePosixPath(k).suffix.lower() in {'.cpp','.cc','.cxx','.c++'}}
    mapped={key for p in packages for key in p['files']}
    source_files={key for info in modules.values() for key in info['files']}
    from . import implementation
    return {'schema':'curriculum-status/v1','id':value['id'],'revision':value['revision'],'module':module,
        'modules':len(modules),'packages':len(packages),'cpp_files':len(cpp),'unassigned_cpp':sorted(cpp-mapped),
        'unassigned_assets':sorted(source_files-mapped),'historical_feature_states':dict(Counter(f['state'] for f in features)),
        'unresolved_feature_rows':sum(f['state'] not in {'mapped','duplicate','out_of_scope'} for f in features),
        'implementation':implementation.audit(store,module),'mainline_tasks':len(value['mainlines']),
        'planning_status':'candidate_plan_not_semantic_completion','database_execution':'not_run'}


def listing(store,module=None,offset=0,limit=30):
    require(offset>=0 and 1<=limit<=200,'Read 1..200 curriculum packages per page')
    value=current(store,True);items=[p for p in value['packages'] if not module or p['module']==module]
    return {'id':value['id'],'revision':value['revision'],'total':len(items),'items':items[offset:offset+limit],
            'next_offset':offset+limit if offset+limit<len(items) else None}


def refine(store,module,packages,author,expected_revision):
    value=current(store,True);require(value['revision']==expected_revision,'Curriculum changed; read latest revision')
    require(author and module in study.current(store)['modules'],'Actual planner and module required')
    require(isinstance(packages,list) and 1<=len(packages)<=100,'Provide 1..100 mechanism work packages')
    owned=set(study.current(store)['modules'][module]['files']);covered=set();new=[]
    feature_ids={f['id'] for f in value['features']};mainline_ids={m['id'] for m in value['mainlines']}
    for p in packages:
        require(p.get('id') and p.get('title') and p.get('question') and p.get('files'),'Package id/title/question/files required')
        require(set(p['files'])<=owned,'Package files outside module')
        require(len(p['files'])==len(set(p['files'])),'Repeated package file')
        require(set(p.get('feature_ids',[]))<=feature_ids and set(p.get('mainline_ids',[]))<=mainline_ids,'Unknown historical feature/mainline ID')
        require(len(p['files'])<=value['policy']['max_files'],'Split oversized package by behavior and continuation budget')
        covered.update(p['files']);new.append({**p,'id':identity('package',[value['plan_id'],module,p['id']]),'module':module,
            'feature_ids':p.get('feature_ids',[]),'mainline_ids':p.get('mainline_ids',[]),'depends_on':[study.current(store)['modules'][module]['task']],
            'tasks':[],'scope_status':'planner_refined_requires_research','grouping_basis':'explicit_module_plan',
            'expected_outputs':OUTPUTS,'budget':{'max_read_lines':value['policy']['region_lines']}})
    require(owned<=covered,'Refinement must preserve every owned asset obligation')
    require(len({p['id'] for p in new})==len(new),'Repeated logical package IDs')
    for old in value['packages']:
        if old['module']==module:
            require(not old['tasks'],'Refine before execution; existing package tasks preserve immutable scope')
    with store.transaction():
        require(current(store,True)['revision']==expected_revision,'Curriculum changed during refinement')
        value=deepcopy(value);value['packages']=[p for p in value['packages'] if p['module']!=module]+new
        value['revision']=digest([expected_revision,module,new,author]);value['refined_by']=author
        store.set_meta(value['id'],value);store.event('curriculum_refined',{'module':module,'revision':value['revision'],'author':author})
    return {'revision':value['revision'],'module':module,'packages':len(new),'semantic_approval':'not_granted'}


def export(store):
    value=current(store,True);summary=status(store);folder=store.home/'curriculum';plan=study.current(store)
    atomic_write(folder/'PLAN.json',json.dumps({'curriculum':value,'status':summary,'features':feature_status(store)},ensure_ascii=False,indent=2)+'\n')
    text=['# 模块、特性与主干流程学习计划','',f"{len(plan['modules'])}模块 / {summary['packages']}功能工作包候选 / {summary['cpp_files']}个C++实现文件。",'',
          '先按模块确认课程，再研究机制与主干；函数、TU和图节点不是学习任务。分组是待核候选，不是已审知识。','',
          '| 模块 | 工作包 | C++文件 | 历史特性候选 | 依赖 |','| --- | --- | ---: | --- | --- |']
    for p in value['packages']:text.append(f"| {p['module']} | {p['title']} | {p.get('cpp_files','待核')} | {';'.join(p['feature_ids'])} | {';'.join(p['depends_on'])} |")
    text+=['','## 主干流程与公共机制','']+[f"- {m['id']} {m['title']}：{'、'.join(m['modules']) or '需定位'}；任务 `{m['task']}`" for m in value['mainlines']]
    text+=['','## 覆盖与输入状态','','```json',json.dumps(summary,ensure_ascii=False,indent=2),'```']
    atomic_write(folder/'PLAN.md','\n'.join(text)+'\n')
    out=io.StringIO();w=csv.writer(out);w.writerow(['package','module','title','files','feature_ids','mainline_ids','task_ids','scope_status'])
    for p in value['packages']:w.writerow([p['id'],p['module'],p['title'],';'.join(p['files']),';'.join(p['feature_ids']),';'.join(p['mainline_ids']),';'.join(p['tasks']),p['scope_status']])
    atomic_write(folder/'WORK-PACKAGES.csv','\ufeff'+out.getvalue())
    payload=json.dumps({'packages':value['packages'],'features':feature_status(store),'status':summary},ensure_ascii=False).replace('<','\\u003c')
    html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>模块功能学习计划</title><style>body{margin:2rem;font:15px/1.6 system-ui;color:#172637}input{padding:.6rem;width:70%}table{border-collapse:collapse;width:100%}td,th{padding:.5rem;border:1px solid #ccd6de;text-align:left}pre{white-space:pre-wrap}small{color:#52687a}</style><h1>模块 / 特性 / 主干流程学习计划</h1><p>分组是可调整的待核课程；所有源码保留学习义务，已读/已审/编译/运行分别统计。</p><p><a href="PLAN.md">计划</a> · <a href="PLAN.json">JSON</a> · <a href="WORK-PACKAGES.csv">工作包</a> · <a href="../whole/index.html">全仓覆盖</a></p><input id="q" placeholder="筛选模块、特性、机制主题"><p id="count"></p><table><thead><tr><th>模块</th><th>功能工作包与研究问题</th><th>资产/C++</th><th>状态</th></tr></thead><tbody id="rows"></tbody></table><h2>真实覆盖与输入缺口</h2><pre id="status"></pre><script type="application/json" id="data">PAYLOAD</script><script>const d=JSON.parse(document.getElementById('data').textContent);const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function render(){const q=document.getElementById('q').value.toLowerCase();const p=d.packages.filter(p=>JSON.stringify([p.module,p.title,p.feature_ids,p.question]).toLowerCase().includes(q));document.getElementById('count').textContent=p.length+' / '+d.packages.length+' 个工作包';document.getElementById('rows').innerHTML=p.map(p=>'<tr><td>'+e(p.module)+'</td><td><details><summary>'+e(p.title)+'</summary><p>'+e(p.question)+'</p><small>'+e(p.id)+'</small></details></td><td>'+p.files.length+' / '+(p.cpp_files??'待核')+'</td><td>'+e(p.scope_status)+'</td></tr>').join('')}document.getElementById('q').oninput=render;document.getElementById('status').textContent=JSON.stringify(d.status,null,2);render()</script>'''.replace('PAYLOAD',payload)
    atomic_write(folder/'index.html',html)
    return {'html':str(folder/'index.html'),'plan':str(folder/'PLAN.md'),'json':str(folder/'PLAN.json'),'work_packages':str(folder/'WORK-PACKAGES.csv'),'summary':summary}
