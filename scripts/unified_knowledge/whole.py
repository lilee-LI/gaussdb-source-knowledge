"""Version-bound whole-repository curriculum and evidence-backed coverage.

Task/review/knowledge state remains authoritative. These tables are projections
of reviewed task reports; no generated plan or model draft counts as learned.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import csv
from fnmatch import fnmatchcase
from html import escape
import io
import json
from pathlib import Path

from . import study
from .store import atomic_write, canonical, digest, identity, now, read_json, require

ROOT=Path(__file__).resolve().parents[2]
SEMANTIC={'.c','.cc','.cpp','.cxx','.h','.hh','.hpp','.hxx','.inc','.inl','.y','.yy','.l','.ll',
          '.sql','.py','.sh','.pl','.ps1','.cmake','.proto','.rs','.go','.java','.md','.sgml','.sgmlin','.html','.htm','.docx','.pdf',
          '.txt','.json','.yaml','.yml','.xml','.ini','.map','.conf','.control','.out','.expected','.bat','.mk','.am','.in'}
REPORT_LISTS=('assets','leads','proposals','contracts','gaps','templates','implementations','feature_mappings')


def policy(spec=None, adapter=None):
    if spec is None:
        spec='generic' if (adapter or {}).get('id')=='generic-cpp' else 'postgres-family'
    if isinstance(spec,dict):value=deepcopy(spec)
    else:
        path=ROOT/'adapters/learning'/(str(spec)+'.json')
        value=read_json(path if path.is_file() else Path(spec))
    require(value.get('schema')=='whole-learning-policy/v1','Unsupported learning policy')
    require(isinstance(value.get('domains'),list) and value['domains'],'Learning domains required')
    require(type(value.get('partition_max_files',80)) is int and 8<=value.get('partition_max_files',80)<=1000,'Invalid partition budget')
    ids=[x['id'] for x in value.get('templates',[])]
    require(len(ids)==len(set(ids)) and len(ids)<=64,'Invalid learning templates')
    pending={x['id']:set(x.get('depends_on',[])) for x in value.get('templates',[])}
    require(all(d<=set(ids) for d in pending.values()),'Unknown template prerequisite')
    while pending:
        ready={k for k,v in pending.items() if not v}
        require(ready,'Cyclic learning template dependencies')
        pending={k:v-ready for k,v in pending.items() if k not in ready}
    value.pop('digest',None);value['digest']=digest(value)
    return value


def partition(groups, maximum, explicit=()):
    """Refine broad directories, never invent a task for every symbol or file."""
    output={}
    def split(name,files):
        if len(files)<=maximum or name in explicit:
            output[name]=sorted(files);return
        parts=defaultdict(list);direct=[]
        prefix=name.rstrip('/')+'/'
        for key in files:
            tail=key[len(prefix):] if key.startswith(prefix) else key.rsplit('/',1)[-1]
            if '/' in tail:parts[prefix+tail.split('/',1)[0]].append(key)
            else:direct.append(key)
        if not parts:
            output[name]=sorted(files);return
        if direct:output[name]=sorted(direct)
        for child,keys in sorted(parts.items()):split(child,keys)
    for name,files in sorted(groups.items()):split(name,files)
    return output


def current(store,required=True):
    if not store.get_meta('study_head'):
        require(not required,'Run start to initialize the study plan')
        return None
    plan=study.current(store)
    pid=store.get_meta('whole-for:'+plan['id'])
    value=store.record('learning_programs',pid) if pid else None
    require(value or not required,'Run start or whole-plan to initialize the whole-repository program')
    return value


def _category(asset):
    path=Path(asset['path']);suffix=path.suffix.lower();name=path.name.lower()
    semantic=asset['kind']=='document' or suffix in SEMANTIC or name in {'makefile','cmakelists.txt','configure','configure.in'}
    if asset['status']=='excluded':return 'input_exclusion',False
    if asset.get('material_kind')=='build_context':return 'build_context_inventory',False
    if asset.get('bytes')==0:return 'empty_material',False
    if asset['kind']=='document':return 'material',True
    if '/test/' in asset['key'] and '/data/' in asset['key'] and suffix not in SEMANTIC- {'.txt','.json','.xml','.ini'}:
        return 'test_dataset',False
    if suffix in {'.data','.png','.jpg','.gif','.svg','.ico','.woff','.woff2','.ttf'}:return 'supporting_data',False
    return ('implementation_or_text' if semantic else 'resource'),semantic


def _domain(key,p):
    matches=[(len(pattern.replace('*','')),d['id']) for d in p['domains'] for pattern in d.get('patterns',[]) if fnmatchcase(key,pattern)]
    return max(matches)[1] if matches else 'unclassified'


def ensure(store, spec=None):
    plan=study.current(store)
    old=current(store,False)
    if plan.get('worker_scope'):
        require(old,'Worker kit lacks the coordinator program; request an updated kit')
        return old
    p=policy(spec or plan.get('learning_policy'),plan.get('product_adapter'))
    pid=identity('whole-program',[plan['id'],plan['snapshot'],plan['profile'],p['digest']])
    if old and old['id']==pid:return old
    assets=[json.loads(r[0]) for r in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind IN ('source','document') ORDER BY key",(plan['snapshot'],))]
    owners={a:m for m,v in plan['modules'].items() for a in v['files']}
    templates=[];created={}
    from .planner import create_task
    with store.transaction():
        for a in assets:
            kind,semantic=_category(a)
            data={'asset':a['key'],'kind':kind,'status':a['status'],'domain':_domain(a['key'],p),'bytes':a.get('bytes',0),'reason':a.get('reason') or a.get('extraction_error')}
            store.db.execute('INSERT OR IGNORE INTO learning_assets VALUES(?,?,?,?,?,?)',(pid,a['key'],owners.get(a['key']),a.get('text_sha') or a.get('sha'),int(semantic),canonical(data)))
        pending=list(p.get('templates',[]))
        while pending:
            for template in list(pending):
                if not set(template.get('depends_on',[]))<=set(created):continue
                selected=[]
                for pattern in template.get('patterns',[]):
                    hits=[a['key'] for a in assets if a['status']=='frozen' and fnmatchcase(a['key'],pattern)]
                    selected.extend(sorted(hits,key=lambda k:(Path(k).suffix.lower() not in {'.cpp','.c','.h'},k))[:2])
                selected=list(dict.fromkeys(selected))[:8]
                owner=next((owners[k] for k in selected if k in owners),None)
                refs=[]
                for key in selected[:3]:
                    a=store.asset(plan['snapshot'],key);lines=store.source_lines(a.get('text_sha') or a['sha'])
                    if lines:refs.append(store.anchor(plan['snapshot'],key,1,min(30,len(lines)),text_sha=a.get('text_sha'))['id'])
                deps=[created[d] for d in template.get('depends_on',[])]
                if owner:deps.append(plan['modules'][owner]['task'])
                kind=template['kind'] if selected else 'scope_research'
                question=template['question'] if selected else '定位或有证据地说明本范围是否涉及：'+template['title']+'。目录未命中不证明不适用。'
                tid=create_task(store,snapshot=plan['snapshot'],run=plan['run'],profile=plan['profile'],kind=kind,
                    bundle={'plan_id':plan['id'],'program_id':pid,'program_item':template['id'],'module':owner,'question':question,
                            'selected_files':selected,'source_anchor_refs':refs,'unlocated_template':not bool(selected)},dependencies=deps)
                created[template['id']]=tid
                templates.append({**template,'task':tid,'module':owner,'seed_files':selected,'scope_status':'located' if selected else 'needs_scope_decision'})
                pending.remove(template)
        value={'id':pid,'schema':'whole-learning-program/v1','plan_id':plan['id'],'snapshot':plan['snapshot'],'profile':plan['profile'],
               'source_index':plan.get('source_index'),'policy':p,'templates':templates,'created':now(),'assets':len(assets),
               'modules':{m:{'task':v['task'],'assets':len(v['files'])} for m,v in plan['modules'].items()},
               'scope_digest':digest([(a['key'],a.get('sha'),a.get('text_sha'),a['status']) for a in assets]),'worker_scope':None}
        store.db.execute('INSERT OR REPLACE INTO learning_programs VALUES(?,?,?,?,?)',(pid,plan['id'],plan['snapshot'],plan['profile'],canonical(value)))
        store.set_meta('whole-for:'+plan['id'],pid)
        store.event('whole_program_created',{'program':pid,'assets':len(assets),'modules':len(plan['modules']),'template_tasks':len(templates),'semantic_completion':False})
    return value


def reference_units(store, ids):
    found=store.units(ids=sorted(set(ids)))
    ticket=store.get_meta('work_kit')
    if ticket:
        synced=store.get_meta('synced-references:'+ticket,{})
        found={**synced.get('units',{}),**found}
    return {key:found[key] for key in ids if key in found}


def _applicable(store,unit,program):
    from .knowledge import content_hash
    cache=getattr(store,'_coverage_freshness',{})
    key=(program['id'],store.get_meta('knowledge_head'),unit['id'],content_hash(unit))
    if key not in cache:
        if len(cache)>=5000:cache.clear()
        cache[key]=_check_applicable(store,unit,program)
        store._coverage_freshness=cache
    return cache[key]


def _check_applicable(store, unit, program):
    b=unit.get('_binding',{})
    if b.get('profile')!=program['profile']:return False
    for ref in unit.get('source_refs',[]):
        try:
            anchor=store.record('anchors',ref)
            if not store.evidence_in_scope(anchor,program['snapshot']):return False
        except ValueError:return False
    if unit.get('review',{}).get('verdict')!='accept':return False
    if store.get_meta('work_kit'):
        from .knowledge import content_hash
        synced=store.get_meta('synced-references:'+store.get_meta('work_kit'),{})
        # A shard intentionally lacks global symbol adjacency. Reuse the signed
        # coordinator freshness proof for the exact same global graph and inputs.
        if synced.get('source_index')==study.current(store).get('source_index') and synced.get('applicable_hashes',{}).get(unit['id'])==content_hash(unit):return True
    from .knowledge import UnitMap, freshness
    synced=store.get_meta('synced-references:'+str(store.get_meta('work_kit')),{})
    units=UnitMap(store,store.get_meta('knowledge_head'),{**synced.get('units',{}),**reference_units(store,[unit['id']])})
    return not freshness(store,unit,program['snapshot'],study.current(store)['run'],units)


def _complete_span(store, snapshot, asset, refs):
    a=store.asset(snapshot,asset)
    if a['status']!='frozen':return False
    total=len(store.source_lines(a.get('text_sha') or a['sha']))
    position=1
    spans=[]
    for ref in refs:
        e=store.record('anchors',ref)
        if e['asset']==asset and store.evidence_in_scope(e,snapshot):spans.append((e['start'],e['end']))
    for first,last in sorted(spans):
        if first<=position:position=max(position,last+1)
    return position>total


def validate_progress(store, task, report, drafts, complete_reads, *, imported=False):
    from .knowledge import content_hash
    require(isinstance(report,dict) and not set(report)-{'program','inventory_complete',*REPORT_LISTS},'Invalid progress report fields')
    p=current(store);require(report.get('program',p['id'])==p['id'],'Progress program mismatch')
    require(task['snapshot']==p['snapshot'] and task['profile']==p['profile'],'Progress scope mismatch')
    module=task['bundle'].get('module')
    allowed=set(study.current(store)['modules'].get(module,{}).get('files',[]))
    if module is None and task['kind']=='scope_research':allowed=set()
    normalized={'program':p['id'],'inventory_complete':report.get('inventory_complete',False)}
    require(type(normalized['inventory_complete']) is bool,'inventory_complete must be boolean')
    requested={u for key in ('assets','leads','templates','implementations','feature_mappings') for row in report.get(key,[]) for u in row.get('unit_ids',[])}
    requested.update(r.get('unit') for r in report.get('contracts',[]) if r.get('unit'))
    available={**reference_units(store,requested),**drafts}
    for key in REPORT_LISTS:
        rows=report.get(key,[]);require(isinstance(rows,list) and len(rows)<=2000,'Progress section too large: '+key)
        normalized[key]=deepcopy(rows)
    seen=set()
    for row in normalized['assets']:
        require(row.get('asset') in allowed and row['asset'] not in seen,'Progress asset outside assigned module or repeated')
        seen.add(row['asset']);require(row.get('disposition') in {'studied','partial','supporting','excluded','deferred'},'Invalid asset disposition')
        require(isinstance(row.get('reason'),str) and row['reason'].strip(),'Asset disposition reason required')
        refs=row.get('evidence_refs',[]);ids=row.get('unit_ids',[])
        require(isinstance(refs,list) and isinstance(ids,list) and len(ids)<=100 and set(ids)<=set(available),'Unknown progress knowledge IDs')
        if row.get('reuse'):
            require(ids and all(u in reference_units(store,ids) for u in ids),'Reuse requires accepted knowledge')
            require(all(_applicable(store,available[u],p) for u in ids),'Reused knowledge is not applicable')
            cited={r for u in ids for r in available[u].get('source_refs',[])}
            require(set(refs)<=cited,'Reuse evidence is not cited by accepted knowledge')
        else:require(set(refs)<=complete_reads,'Progress evidence not fully read in this lease')
        for ref in refs:
            a=store.record('anchors',ref);require(store.evidence_in_scope(a,p['snapshot']),'Progress evidence snapshot mismatch')
        metadata=store.db.execute('SELECT semantic FROM learning_assets WHERE program=? AND asset=?',(p['id'],row['asset'])).fetchone()
        require(metadata is not None,'Progress asset absent from program')
        if row['disposition']=='supporting':require(not metadata[0],'Implementation/text assets cannot be dismissed as supporting data')
        if row['disposition'] in {'studied','excluded'} and metadata[0]:
            require(refs and _complete_span(store,p['snapshot'],row['asset'],refs),'Semantic asset requires a full frozen evidence span')
        if row['disposition'] in {'studied','partial'}:
            require(ids,'Asset '+row['asset']+' disposition='+row['disposition']+' requires staged/accepted unit_ids; for inventory-only use deferred for EVERY asset, never guessed knowledge IDs')
            cited={r for u in ids for r in available[u].get('source_refs',[])}
            require(set(refs)<=cited,'Coverage evidence must be cited by its knowledge units')
            if row['disposition']=='studied':require(_complete_span(store,p['snapshot'],row['asset'],cited),'Knowledge citations do not cover the studied file')
        row['unit_hashes']={u:content_hash(available[u]) for u in ids}
    from . import curriculum,implementation
    course=curriculum.current(store)
    if course and normalized['inventory_complete']:
        require(task['kind']=='module_survey' and seen==allowed,'Complete inventory must account for EVERY asset in the assigned module')
    if course:
        normalized['implementations']=implementation.validate(store,p,task,normalized['implementations'],available,complete_reads)
        normalized['feature_mappings']=curriculum.validate_feature_mappings(store,p,task,normalized['feature_mappings'],available,complete_reads)
    else:
        require(not normalized['implementations'] and not normalized['feature_mappings'],'Initialize the module curriculum before submitting implementation/feature mappings')
    from .task_planning import candidates
    leads={x['id']:x for x in candidates(store,study.current(store))}
    proposal_ids={r.get('id') for r in normalized['proposals']}
    require(None not in proposal_ids and len(proposal_ids)==len(normalized['proposals']),'Proposal local IDs must be unique')
    for row in normalized['leads']:
        require(row.get('candidate_id') in leads and leads[row['candidate_id']].get('owner_module')==module,'Lead outside assigned module')
        require(row.get('state') in {'mapped','research','excluded','deferred'} and row.get('reason'),'Invalid lead disposition')
        require(set(row.get('unit_ids',[]))<=set(available),'Unknown lead knowledge IDs')
        require(set(row.get('proposal_ids',[]))<=proposal_ids|set(leads),'Unknown lead research proposal')
        require(row['state']!='mapped' or row.get('unit_ids'),'Mapped lead needs knowledge')
        require(row['state']!='research' or row.get('proposal_ids'),'Research lead needs proposed mechanism')
        require(row.get('evidence_refs'),'Lead disposition needs cited source evidence')
        cited=[store.record('anchors',ref) for ref in row['evidence_refs']]
        require(any(a['asset']==e['asset'] and a['start']<=e['end'] and a['end']>=e['start'] for a in cited for e in leads[row['candidate_id']]['evidence']),'Lead disposition does not cite its inventory evidence')
        require(set(row.get('evidence_refs',[]))<=complete_reads or row.get('unit_ids') and all(_applicable(store,available[u],p) for u in row['unit_ids']),'Lead disposition needs actual evidence or applicable reuse')
        row['unit_hashes']={u:content_hash(available[u]) for u in row.get('unit_ids',[])}
    for row in normalized['proposals']:
        require(row.get('owner_module')==module and row.get('title') and row.get('question') and row.get('reason'),'Invalid mechanism proposal')
        require(set(row.get('depends_on',[]))<=proposal_ids|set(leads),'Unknown mechanism prerequisite')
        evidence=row.get('evidence',[]);require(isinstance(evidence,list) and 1<=len(evidence)<=40,'Mechanism evidence seeds required')
        require(any(e['asset'] in allowed for e in evidence),'Mechanism needs owned source evidence')
        for e in evidence:
            a=store.asset(p['snapshot'],e['asset']);length=len(store.source_lines(a.get('text_sha') or a['sha']))
            require(type(e['start']) is int and type(e['end']) is int and 1<=e['start']<=e['end']<=length,'Invalid mechanism evidence range')
            spans=[store.record('anchors',r) for r in complete_reads]
            position=e['start'];selected=[s for s in spans if s['asset']==e['asset'] and s['end']>=e['start'] and s['start']<=e['end']]
            for span in sorted(selected,key=lambda s:s['start']):
                if span['start']<=position:position=max(position,span['end']+1)
            require(position>e['end'],'Mechanism seed was not fully read in this lease: '+e['asset']+':'+str(e['start'])+'..'+str(e['end']))
            row['evidence_refs']=sorted(set(row.get('evidence_refs',[]))|{s['id'] for s in selected})
        require(set(row.get('supersedes',[]))<=set(leads),'Unknown superseded lead')
    pending={r['id']:set(r.get('depends_on',[]))&proposal_ids for r in normalized['proposals']}
    while pending:
        ready={k for k,v in pending.items() if not v};require(ready,'Cyclic progress proposals')
        pending={k:v-ready for k,v in pending.items() if k not in ready}
    for row in normalized['contracts']:
        require(row.get('side') in {'producer','consumer'} and row.get('unit') and row.get('reason'),'Invalid contract verification')
        require(row.get('module')==module,'Contract side must be checked by the owning module')
        require(row.get('producer_module')!=row.get('consumer_module') and module==row[row['side']+'_module'],'Contract endpoint mismatch')
        require(row['producer_module'] in p['modules'] and row['consumer_module'] in p['modules'],'Unknown contract module')
        require(row.get('evidence_refs') and set(row['evidence_refs'])<=complete_reads,'Contract side needs fresh task evidence')
        u=available.get(row['unit']);require(u and u.get('kind')=='contract','Contract verification needs an existing or staged contract')
        endpoints=u.get('producers' if row['side']=='producer' else 'consumers',[])
        require(endpoints,'Contract has no endpoint symbols')
        owned=set(study.current(store)['modules'].get(module,{}).get('files',[]))
        require(any(any(x['asset'] in owned for x in store.lookup_symbols(task['run'],s,names=False,limit=1)) for s in endpoints),'Contract endpoint is outside the checking module')
        row['unit_hash']=content_hash(u)
    for row in normalized['gaps']:
        require(row.get('question') and row.get('reason'),'Concrete gap required')
        if row.get('resolved_by'):
            require(isinstance(row['resolved_by'],list),'resolved_by must be a list of accepted knowledge IDs')
            resolved=reference_units(store,row['resolved_by'])
            require(isinstance(row['resolved_by'],list) and row['resolved_by'] and set(resolved)==set(row['resolved_by']) and all(_applicable(store,u,p) for u in resolved.values()),'Gap resolution needs applicable accepted knowledge IDs')
            row['unit_hashes']={u:content_hash(resolved[u]) for u in resolved}
    for row in normalized['templates']:
        require(row.get('id')==task['bundle'].get('program_item') and row.get('state') in {'verified','not_applicable'} and row.get('reason'),'Template decision mismatch')
        require(row.get('evidence_refs') and set(row['evidence_refs'])<=complete_reads,'Template decision needs actual evidence')
        if row['state']=='verified':require(row.get('unit_ids') and set(row['unit_ids'])<=set(available),'Verified template requires known knowledge')
        row['unit_hashes']={u:content_hash(available[u]) for u in row.get('unit_ids',[])}
    return normalized


def stage_progress(store,task,worker,token,report,previous_digest=None):
    from .planner import _check_lease, task_status, _complete_reads
    with store.transaction():
        row=_check_lease(store,task,worker,token);t=task_status(store,task)
        key='progress-draft:'+task+':'+str(row['attempt'])
        old=store.get_meta(key,{'program':current(store)['id']})
        require(previous_digest is None and not any(old.get(k) for k in REPORT_LISTS) or previous_digest==digest(old),'Progress draft changed; supply previous_digest')
        merged={**old,**{k:v for k,v in report.items() if k not in REPORT_LISTS}}
        for section in REPORT_LISTS:
            rows={canonical(r):r for r in old.get(section,[])}
            # A repeated semantic key updates a row instead of inflating the ledger.
            keys={'assets':'asset','leads':'candidate_id','proposals':'id','contracts':'unit','templates':'id','gaps':'question','implementations':'item','feature_mappings':'feature_id'}
            updates=report.get(section,[])
            def semantic_key(r):
                return tuple(r.get(k) for k in ('unit','side','module','producer_module','consumer_module')) if section=='contracts' else r.get(keys[section])
            replaced={semantic_key(r) for r in updates}
            merged[section]=[r for r in rows.values() if semantic_key(r) not in replaced]+updates
        drafts=store.get_meta('research_drafts:'+task+':'+str(row['attempt']),{})
        value=validate_progress(store,t,merged,drafts,_complete_reads(store,task,worker,token))
        store.set_meta(key,value)
        store.event('progress_staged',{'task':task,'attempt':row['attempt'],'digest':digest(value),'semantic_approval':'not_granted'})
    return {'progress_digest':digest(value),'sections':{k:len(value[k]) for k in REPORT_LISTS},'semantic_approval':'not_granted'}


def apply_reviewed_locked(store,task,result,review):
    """Called within the native task-review transaction, only after acceptance."""
    report=result.get('progress')
    if not report:return
    p=current(store);require(report['program']==p['id'],'Accepted progress belongs to a stale program')
    rid=identity('progress-report',[p['id'],task['id'],digest(result)])
    if store.db.execute('SELECT 1 FROM learning_reports WHERE id=?',(rid,)).fetchone():return
    data={'id':rid,'progress':report,'module':task['bundle'].get('module'),'task':task['id'],'result_digest':digest(result),'review':review,'created':now()}
    store.db.execute('INSERT INTO learning_reports VALUES(?,?,?,?,?)',(rid,p['id'],task['id'],digest(result),canonical(data)))
    for row in report.get('assets',[]):
        row=deepcopy(row)
        previous=store.db.execute('SELECT data FROM learning_dispositions WHERE program=? AND asset=?',(p['id'],row['asset'])).fetchone()
        if previous and row['disposition']=='partial':
            prior=json.loads(previous[0])
            if prior['disposition'] in {'partial','studied'}:
                row['unit_ids']=sorted(set(prior.get('unit_ids',[]))|set(row.get('unit_ids',[])))
                row['evidence_refs']=sorted(set(prior.get('evidence_refs',[]))|set(row.get('evidence_refs',[])))
                row['unit_hashes']={**prior.get('unit_hashes',{}),**row['unit_hashes']}
        store.db.execute('INSERT OR REPLACE INTO learning_dispositions VALUES(?,?,?,?)',(p['id'],row['asset'],rid,canonical(row)))
    for row in report.get('leads',[]):store.db.execute('INSERT OR REPLACE INTO learning_leads VALUES(?,?,?,?)',(p['id'],row['candidate_id'],rid,canonical({**row,'report':rid})))
    for row in report.get('contracts',[]):store.db.execute('INSERT OR REPLACE INTO learning_contract_checks VALUES(?,?,?,?,?,?,?,?)',(p['id'],row['unit'],row['side'],row['module'],row['producer_module'],row['consumer_module'],task['id'],canonical(row)))
    if report.get('implementations'):
        from .implementation import apply_locked
        apply_locked(store,p,rid,report['implementations'])
    store.event('progress_review_applied',{'task':task['id'],'report':rid,'program':p['id']})


def _rows(store,p):
    dispositions={r['asset']:json.loads(r['data']) for r in store.db.execute('SELECT asset,data FROM learning_dispositions WHERE program=?',(p['id'],))}
    ids={u for row in dispositions.values() for u in row.get('unit_ids',[])}
    units=reference_units(store,ids);out=[]
    from .knowledge import content_hash
    for r in store.db.execute('SELECT * FROM learning_assets WHERE program=? ORDER BY asset',(p['id'],)):
        data=json.loads(r['data']);d=dispositions.get(r['asset']);state='unreviewed'
        if data['status']=='excluded':state='input_exclusion'
        elif data['status']!='frozen':state='unavailable'
        elif d:
            state=d['disposition']
            if state in {'studied','partial'}:
                if not all(u in units and _applicable(store,units[u],p) and content_hash(units[u])==d['unit_hashes'].get(u) for u in d.get('unit_ids',[])):state='pending_knowledge'
                elif _complete_span(store,p['snapshot'],r['asset'],{ref for u in d['unit_ids'] for ref in units[u].get('source_refs',[])}):state='studied'
        out.append({**data,'module':r['module'],'sha256':r['sha'],'semantic':bool(r['semantic']),'state':state,'disposition':d})
    return out


def _report_state(store,p):
    reports=[json.loads(r[0]) for r in store.db.execute('SELECT data FROM learning_reports WHERE program=? ORDER BY rowid',(p['id'],))]
    inventories={r['module']:r for r in reports if r['progress'].get('inventory_complete')}
    latest={r['task']:r for r in reports}
    return reports,inventories,latest


def status(store,module=None):
    p=current(store);rows=_rows(store,p);reports,inventories,latest=_report_state(store,p)
    from .task_planning import candidates
    leads=candidates(store,study.current(store));dispositions={r['candidate']:json.loads(r['data']) for r in store.db.execute('SELECT candidate,data FROM learning_leads WHERE program=?',(p['id'],))}
    candidate_state={}
    for c in leads:
        d=dispositions.get(c['id']);state='unreviewed'
        if d:
            state=d['state']
            if state=='mapped':
                units=reference_units(store,d['unit_ids'])
                from .knowledge import content_hash
                if not all(u in units and _applicable(store,units[u],p) and content_hash(units[u])==d['unit_hashes'][u] for u in d['unit_ids']):state='pending_knowledge'
            if state=='research':
                linked=store.get_meta('report-proposals:'+p['id'],{})
                mapped=[linked.get(d['report']+':'+x,x) for x in d.get('proposal_ids',[])]
                tasks=[r for cid in mapped for r in store.db.execute("SELECT id,status FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.candidate_id')=?",(p['snapshot'],p['plan_id'],cid))]
                if tasks and all(r['status']=='accepted' for r in tasks) and all(_task_published(store,r['id']) for r in tasks):state='mapped'
        if not d and c['id'] in store.get_meta('approved-program-candidates:'+p['id'],[]):
            tasks=[r[0] for r in store.db.execute("SELECT id FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.candidate_id')=?",(p['snapshot'],p['plan_id'],c['id']))]
            if tasks and all(_task_published(store,t) for t in tasks):state='mapped'
        candidate_state[c['id']]={'state':state,'module':c.get('owner_module')}
    from . import curriculum,implementation
    course=curriculum.current(store);region_open=Counter()
    if course:
        owners={r['asset']:r['module'] for r in rows}
        for r in implementation.evaluated(store,p).values():
            if r['state'] not in {'explained','no_implementation'}:region_open[owners.get(r['asset'])]+=1
    modules=[]
    for name,info in p['modules'].items():
        if p.get('worker_scope') and name!=p['worker_scope']:continue
        if module and module!=name:continue
        owned=[r for r in rows if r['module']==name];counts=Counter(r['state'] for r in owned)
        ccounts=Counter(v['state'] for v in candidate_state.values() if v['module']==name)
        tasks=[dict(r) for r in store.db.execute("SELECT id,kind,status,owner FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.module')=?",(p['snapshot'],p['plan_id'],name))]
        closed=(name in inventories and not region_open[name] and all(r['state'] in {'studied','supporting','input_exclusion'} for r in owned) and all(v['state'] in {'mapped','excluded'} for v in candidate_state.values() if v['module']==name) and not any(t['status'] in {'leased','submitted','needs_research','queued'} and t['kind']!='module_survey' for t in tasks))
        domains=dict(Counter(r['domain'] for r in owned))
        modules.append({'module':name,'domains':domains,'assets':len(owned),'states':dict(counts),'lead_states':dict(ccounts),'inventory_reviewed':name in inventories,'unexplained_cpp_regions':region_open[name] if course else None,'source_knowledge_closed':closed,'tasks':tasks})
    return {'schema':'whole-learning-status/v1','program':p['id'],'snapshot':p['snapshot'],'profile':p['profile'],'knowledge_revision':store.get_meta('knowledge_head'),
            'assets':len(rows),'asset_states':dict(Counter(r['state'] for r in rows)),'semantic_assets':sum(r['semantic'] for r in rows),
            'modules':modules,'candidate_states':dict(Counter(v['state'] for v in candidate_state.values())),'candidates':candidate_state,
            'reviewed_progress_reports':len(reports),'source_only':True,'database_execution':'not_run'}


def _task_published(store,task):
    t=store.record('tasks',task)
    row=store.db.execute('SELECT status,result FROM tasks WHERE id=?',(task,)).fetchone()
    if row['status']!='accepted':return False
    result=json.loads(row['result'])
    ids=[u['id'] for u in result.get('claims',[])]
    if not ids:
        decisions=result.get('progress',{}).get('templates',[])
        return bool(decisions and all(d['state']=='not_applicable' for d in decisions))
    units=reference_units(store,ids)
    from .knowledge import content_hash
    return all(u['id'] in units and content_hash(u)==content_hash(units[u['id']]) and _applicable(store,units[u['id']],current(store)) for u in result['claims'])


def advance(store,max_tasks=8):
    p=current(store);require(type(max_tasks) is int and 1<=max_tasks<=100,'Invalid batch size')
    from . import curriculum
    course=curriculum.current(store)
    from .task_planning import propose, construct
    reports,inv,_=_report_state(store,p)
    mapping=store.get_meta('report-proposals:'+p['id'],{})
    approved=set(store.get_meta('approved-program-candidates:'+p['id'],[]))
    for record in reports:
        proposals=record['progress'].get('proposals',[]);pending=list(proposals)
        local=lambda x:record['id']+':'+x
        while pending:
            ready=[r for r in pending if all(local(x) in mapping for x in r.get('depends_on',[]) if x in {i['id'] for i in proposals})]
            require(ready,'Reviewed proposal prerequisites cannot be resolved')
            for r in ready:
                if local(r['id']) not in mapping:
                    item={k:r[k] for k in ('title','question','reason','owner_module','evidence')}
                    item['supersedes']=r.get('supersedes',[]);item['depends_on']=[mapping.get(local(x),x) for x in r.get('depends_on',[])]
                    value=propose(store,{'study_plan':p['plan_id'],'author':record['review']['reviewer'],'reason':'Reviewed module progress '+record['task'],'parent_task':record['task'],'candidates':[item]})
                    mapping[local(r['id'])]=value['candidates'][0]['id'];approved.add(mapping[local(r['id'])])
                    with store.transaction():
                        store.set_meta('report-proposals:'+p['id'],mapping);store.set_meta('approved-program-candidates:'+p['id'],sorted(approved))
                pending.remove(r)
    made=construct(store,max_tasks=max_tasks,candidate_ids=sorted(approved),apply=True) if approved else {'tasks':[],'task_results':[]}
    from .planner import create_task
    states=status(store)
    assets=_rows(store,p)
    closure=defaultdict(list)
    closure_kinds={'open_gap','unverified_cross_module_contract','one_sided_contract','changed_contract','contract_endpoint_disagreement','unpublished_contract'}
    owners={r['asset']:r['module'] for r in assets}
    if any(m['inventory_reviewed'] for m in states['modules']):
        for issue in audit(store)['blockers']:
            if issue['kind'] not in closure_kinds:continue
            modules=set(issue.get('producer_modules',[])+issue.get('consumer_modules',[]))
            if issue.get('task'):modules.add(store.record('tasks',issue['task'])['bundle'].get('module'))
            if issue.get('unit'):
                u=reference_units(store,[issue['unit']]).get(issue['unit'],{})
                modules.update(owners.get(r['asset']) for sym in u.get('producers',[])+u.get('consumers',[]) for r in store.lookup_symbols(study.current(store)['run'],sym,names=False,limit=1))
            for name in modules-{None}:closure[name].append(issue)
    for m in states['modules']:
        leads=[cid for cid,info in states['candidates'].items() if info['module']==m['module'] and info['state'] not in {'mapped','excluded'}]
        if leads:closure[m['module']].append({'kind':'candidate_disposition','candidate_ids':leads[:100],'remaining':len(leads)})
    stalled=[]
    with store.transaction():
        for m in states['modules']:
            if len(made['task_results'])>=max_tasks:break
            if not m['inventory_reviewed']:continue
            if any(t['status'] in {'queued','leased','submitted','needs_research'} and t['kind']!='module_survey' for t in m['tasks']):continue
            missing=[r['asset'] for r in assets if r['module']==m['module'] and r['state'] not in {'studied','supporting','input_exclusion','pending_knowledge'}]
            if not missing and closure.get(m['module']):
                issues=closure[m['module']]
                tid=create_task(store,snapshot=p['snapshot'],run=study.current(store)['run'],profile=p['profile'],kind='closure_research',
                    bundle={'plan_id':p['plan_id'],'program_id':p['id'],'module':m['module'],'question':'逐项核对未决问题、原始线索与跨模块契约；已有适用知识能解答时在progress.gaps明确resolved_by；线索用progress.leads记录归属；契约按本方side登记progress.contracts。未证实的项继续保留，不猜测。',
                            'closure_issues':issues,'selected_files':study.current(store)['modules'][m['module']]['files'][:12], 'source_anchor_refs':[]},dependencies=[study.current(store)['modules'][m['module']]['task']])
                if store.db.execute('SELECT status FROM tasks WHERE id=?',(tid,)).fetchone()[0]=='queued':made['task_results'].append({'task':tid,'kind':'closure_research'})
                else:stalled.append({'module':m['module'],'task':tid,'reason':'Reviewed closure task did not resolve these issues; owner must reconcile the remaining evidence.'})
                continue
            if not missing or course:continue
            cursor=[(r['asset'],(r['disposition'] or {}).get('unit_hashes',{})) for r in assets if r['asset'] in missing]
            tid=create_task(store,snapshot=p['snapshot'],run=study.current(store)['run'],profile=p['profile'],kind='coverage_research',
                bundle={'plan_id':p['plan_id'],'program_id':p['id'],'module':m['module'],'question':'按module_assets中的已审引用继续未覆盖区间；大文件可partial分段积累已审知识，不逐函数拆任务。','selected_files':missing[:12], 'remaining_scope_digest':digest(cursor),'source_anchor_refs':[]},dependencies=[study.current(store)['modules'][m['module']]['task']])
            t=store.db.execute('SELECT status FROM tasks WHERE id=?',(tid,)).fetchone()
            if t['status']=='queued':made['task_results'].append({'task':tid,'kind':'coverage_research'})
            elif t['status']=='accepted':stalled.append({'module':m['module'],'task':tid,'reason':'Accepted task produced no new asset coverage; review scope/gaps before scheduling the same work again.'})
    if course and len(made['task_results'])<max_tasks:
        more=curriculum.advance(store,max_tasks-len(made['task_results']))
        made['task_results'].extend(more['created_or_reused']);stalled.extend(more.get('stalled',[]))
    return {'program':p['id'],'approved_mechanism_candidates':len(approved),'created_or_reused':made['task_results'],'stalled':stalled,'automatic_knowledge_acceptance':False}


def next_task(store,worker,module=None):
    import time
    p=current(store);plan=study.current(store)
    if plan.get('worker_scope'):
        require(module in (None,plan['worker_scope']),'Worker kit is scoped to one module')
        module=plan['worker_scope']
    if module:require(module in p['modules'],'Unknown module')
    busy=[dict(r) for r in store.db.execute("SELECT id,status FROM tasks WHERE snapshot=? AND owner=? AND json_extract(data,'$.bundle.plan_id')=? AND (status='submitted' OR (status='leased' AND deadline>?))",(p['snapshot'],worker,p['plan_id'],time.time()))]
    active=[r for r in busy if r['status']=='leased']
    if active:return {'state':'in_progress','tasks':active,'next':'Continue the active lease or release it; no token is stolen.'}
    if len(busy)>=p['policy'].get('max_pending_per_worker',4):return {'state':'waiting_review','tasks':busy}
    sql="SELECT t.id,t.data,t.kind,t.rowid sequence FROM tasks t WHERE snapshot=? AND run=? AND status IN ('queued','needs_research','leased') AND (status<>'leased' OR deadline<?) AND json_extract(data,'$.bundle.plan_id')=? AND NOT EXISTS(SELECT 1 FROM task_edges e JOIN tasks d ON e.dependency=d.id WHERE e.task=t.id AND d.status<>'accepted')"
    rows=store.db.execute(sql,(p['snapshot'],plan['run'],time.time(),p['plan_id'])).fetchall()
    # Continue ready mechanisms before opening hundreds of unrelated surveys.
    # FIFO within each stage keeps modules from being ordered by opaque hashes.
    priority={'shared_research':0,'feature_research':1,'gap_research':1,'coverage_research':1,'closure_research':1,'integration_research':2,'scope_research':3,'module_survey':4}
    from .dispatch import candidate_allowed,authorized_delegate
    from .curriculum import prerequisites
    grant=store.get_meta('dispatch-actor:'+worker)
    granted=set(grant.get('allowed_tasks',[])) if grant else None
    for row in sorted(rows,key=lambda r:(priority.get(r['kind'],9),r['sequence'])):
        bundle=json.loads(row['data'])['bundle'];owner=bundle.get('module')
        if module and owner!=module:continue
        if granted is not None and row['id'] not in granted:continue
        from .planner import task_status
        task=task_status(store,row['id'])
        if not candidate_allowed(store,worker,task) or prerequisites(store,task):continue
        order=store.get_meta('assignment:'+p['plan_id']+':'+str(owner),{})
        if order and order['worker']!=worker and not authorized_delegate(store,worker,order['worker'],task):continue
        return {'state':'ready','task':task}
    return {'state':'waiting_review' if busy else 'blocked_or_complete','pending_review':busy,'next':'Run coverage to see blockers; submitted work is never auto-approved.'}


def module_assets(store,module,offset=0,limit=50):
    require(type(offset) is int and offset>=0 and type(limit) is int and 1<=limit<=200,'Invalid asset page')
    rows=[r for r in _rows(store,current(store)) if r['module']==module]
    return {'module':module,'total':len(rows),'items':rows[offset:offset+limit],'next_offset':offset+limit if offset+limit<len(rows) else None}


def guidance(store,task):
    p=current(store);module=task['bundle'].get('module')
    return {'program':p['id'],'module':module,'program_item':task['bundle'].get('program_item'),
        'workflow':['module_assets: page every owned asset','read_source: frozen ranges with receipts',
                    'stage_research_unit: evidence-backed knowledge','stage_progress: versioned coverage and mechanism proposals',
                    'finish_research: use both latest drafts_digest and progress_digest','stop for independent research and knowledge review'],
        'progress_example':{'program':p['id'],'inventory_complete':task['kind']=='module_survey',
            'assets':[{'asset':'repo/path.cpp','disposition':'studied','reason':'Explain mechanism and boundaries',
                       'evidence_refs':['evidence:actual_full_spans'],'unit_ids':['mechanism:actual']}],
            'leads':[{'candidate_id':'actual candidate ID','state':'mapped','reason':'Covered by mechanism',
                       'evidence_refs':['evidence:actual'],'unit_ids':['mechanism:actual']}],
            'proposals':[{'id':'local-unique','title':'One mechanism','question':'Concrete behavior question','owner_module':module,
                          'reason':'Why separate research','evidence':[{'asset':'repo/path.cpp','start':1,'end':20}], 'depends_on':[]}],
            'contracts':[],'gaps':[],'templates':[]},
        'rules':['Never claim a file studied from a short excerpt: accepted knowledge citations must cover its full frozen text.',
                 'Large files use disposition=partial with actual read/cited spans and knowledge IDs; reviewed published spans accumulate across tasks. module_assets exposes prior citations; continue their uncovered ranges.',
                 'All raw candidates need mapped/research/excluded/deferred dispositions; they do not each become a task.',
                 'Semantic files cannot be supporting data. Exclusions and not-applicable decisions need concrete reviewed evidence.',
                 'Reuse requires reuse=true and applicable accepted units. New facts require fresh reads in this lease.',
                 'Public mechanism/integration tasks must report templates:[{id:program_item,state:verified|not_applicable,reason,evidence_refs,unit_ids}].',
                 'Cross-module contracts report producer and consumer sides from each owning module with real endpoint symbols.',
                 'Only a module_survey with EVERY assigned asset may set inventory_complete=true; deeper tasks leave it false. Open questions remain gaps, never pretend completion.']}


def read_source(store,task,worker,token,asset,start=1,lines=200):
    from .planner import _check_lease,create_task_evidence,read_for_task
    require(type(start) is int and start>=1 and type(lines) is int and 1<=lines<=400,'Read 1..400 source lines')
    row=_check_lease(store,task,worker,token);a=store.asset(row['snapshot'],asset)
    require(a['status']=='frozen','Material has no readable frozen text')
    count=len(store.source_lines(a.get('text_sha') or a['sha']))
    require(start<=max(1,count),'Start exceeds frozen text length')
    end=min(count,start+lines-1)
    require(end>=start,'Empty material has no evidence range; report an explicit exclusion')
    anchor=create_task_evidence(store,task,worker,token,asset,start,end)
    reading=read_for_task(store,task,worker,token,anchor['id'],max_chars=100000)
    return {**reading,'total_lines':count,'next_line':end+1 if end<count else None}


def search_source(store,task,worker,token,query,asset_patterns=None,limit=30,offset=0,line_offset=0):
    """Bounded literal search of frozen materials; hits are not read receipts."""
    from .planner import _check_lease,task_status
    _check_lease(store,task,worker,token)
    require(isinstance(query,str) and 1<=len(query)<=500 and type(limit) is int and 1<=limit<=100 and type(offset) is int and offset>=0 and type(line_offset) is int and line_offset>=0,'Invalid bounded source search')
    p=study.current(store);t=task_status(store,task)
    if asset_patterns:
        require(isinstance(asset_patterns,list) and 1<=len(asset_patterns)<=40,'Use 1..40 source path patterns')
        keys=[r[0] for r in store.db.execute("SELECT key FROM assets WHERE snapshot=? AND status='frozen' AND kind IN ('source','document') ORDER BY key",(p['snapshot'],)) if any(fnmatchcase(r[0],pattern) for pattern in asset_patterns)]
    else:
        synced=store.get_meta('synced-references:'+str(store.get_meta('work_kit')),{})
        keys=sorted(set(p['modules'].get(t['bundle'].get('module'),{}).get('files',[]))|set(t['bundle'].get('selected_files',[]))|set(synced.get('extra_materials',[])))
    matches=[];selected=keys[offset:offset+200];used=0;hit_line=None;unavailable=[]
    for key in selected:
        used+=1
        a=store.asset(p['snapshot'],key)
        if a['status']!='frozen':unavailable.append(key);continue
        sha=a.get('text_sha') or a['sha'];path=store.blob_path(sha)
        require(store.file_hash(path)==sha,'Search source hash mismatch')
        with path.open('r',encoding='utf-8',errors='replace') as stream:
            for number,line in enumerate(stream,1):
                if used==1 and number<=line_offset:continue
                if query.casefold() in line.casefold():
                    matches.append({'asset':key,'line':number,'text':line[:500].rstrip()})
                    if len(matches)>=limit:hit_line=number;break
        if len(matches)>=limit:break
    with store.transaction():
        _check_lease(store,task,worker,token)
        for match in matches:
            a=store.asset(p['snapshot'],match['asset'])
            match['evidence']=store.anchor(p['snapshot'],match['asset'],match['line'],match['line'],text_sha=a.get('text_sha'))['id']
    next_file=offset+used-1 if hit_line else offset+used
    return {'matches':matches,'files_available':len(keys),'files_searched':used,'unavailable':unavailable,'scope_digest':digest(keys),'truncated':used<len(keys)-offset or hit_line is not None,
            'next_file_offset':next_file if next_file<len(keys) else None,'next_line_offset':hit_line or 0,'read_receipts':'not_created; use read_source/read_task_evidence'}


def audit(store,module=None):
    p=current(store)
    require(module is None or module in p['modules'],'Unknown coverage module')
    s=status(store,module);rows=[r for r in _rows(store,p) if module is None or r['module']==module];reports,_,latest=_report_state(store,p)
    blockers=[]
    missing=[r['asset'] for r in rows if r['state'] not in {'studied','supporting','input_exclusion'}]
    if missing:blockers.append({'kind':'asset_coverage','count':len(missing),'examples':missing[:20]})
    incomplete=[m['module'] for m in s['modules'] if not m['source_knowledge_closed']]
    if incomplete:blockers.append({'kind':'module_closure','count':len(incomplete),'examples':incomplete[:20]})
    unclosed=[k for k,v in s['candidates'].items() if (module is None or v['module']==module) and v['state'] not in {'mapped','excluded'}]
    if unclosed:blockers.append({'kind':'candidate_disposition','count':len(unclosed),'examples':unclosed[:20]})
    for t in p['templates']:
        if module is not None and t['module']!=module:continue
        if not _task_published(store,t['task']):blockers.append({'kind':'program_item','id':t['id'],'task':t['task']});continue
        record=latest.get(t['task']);decisions=record and record['progress'].get('templates',[])
        if not decisions:blockers.append({'kind':'template_scope_decision','id':t['id']})
    contracts=defaultdict(list)
    checked={}
    for row in store.db.execute('SELECT data FROM learning_contracts WHERE program=? UNION ALL SELECT data FROM learning_contract_checks WHERE program=?',(p['id'],p['id'])):
        x=json.loads(row[0]);checked[(x['unit'],x['side'],x['module'],x['producer_module'],x['consumer_module'])]=x
    for x in checked.values():contracts[x['unit']].append(x)
    # Discover cross-module contracts even if a researcher forgot to register a side.
    owned={r['asset']:r['module'] for r in store.db.execute('SELECT asset,module FROM learning_assets WHERE program=?',(p['id'],))}
    revision=store.get_meta('knowledge_head')
    contract_ids=[r[0] for r in store.db.execute("SELECT r.id FROM revision_units r JOIN unit_versions v ON r.hash=v.hash WHERE r.revision=? AND json_extract(v.data,'$.kind')='contract'",(revision,))] if revision else []
    expected_pairs={}
    for uid,u in reference_units(store,contract_ids).items():
        if not _applicable(store,u,p):continue
        endpoints=[]
        for side in ('producers','consumers'):
            endpoints.append({owned.get(r['asset']) for sym in u.get(side,[]) for r in store.lookup_symbols(study.current(store)['run'],sym,names=False,limit=1)}-{None})
        pairs={(first,second) for first in endpoints[0] for second in endpoints[1] if first!=second and (module is None or module in (first,second))}
        if pairs:
            expected_pairs[uid]=pairs
            registered={(x['producer_module'],x['consumer_module']) for x in contracts.get(uid,[])}
            if pairs-registered:blockers.append({'kind':'unverified_cross_module_contract','unit':uid,'producer_modules':sorted(endpoints[0]),'consumer_modules':sorted(endpoints[1]),'missing_pairs':sorted(pairs-registered)})
    if module is not None:contracts={uid:sides for uid,sides in contracts.items() if any(module in (x['producer_module'],x['consumer_module']) for x in sides)}
    from .knowledge import content_hash
    for uid,sides in contracts.items():
        units=reference_units(store,[uid]);u=units.get(uid)
        if not u or u.get('kind')!='contract' or not _applicable(store,u,p):blockers.append({'kind':'unpublished_contract','unit':uid});continue
        if any(x.get('unit_hash')!=content_hash(u) for x in sides):blockers.append({'kind':'changed_contract','unit':uid})
        pairs={(x['producer_module'],x['consumer_module']) for x in sides}
        for pair in pairs:
            if {x['side'] for x in sides if (x['producer_module'],x['consumer_module'])==pair}!={'producer','consumer'}:
                blockers.append({'kind':'one_sided_contract','unit':uid,'producer_modules':[pair[0]],'consumer_modules':[pair[1]]})
        if pairs-expected_pairs.get(uid,set()):blockers.append({'kind':'contract_endpoint_disagreement','unit':uid})
    gaps={}
    for record in reports:
        if module is not None and record['module']!=module:continue
        for gap in record['progress'].get('gaps',[]):gaps[(record['module'],gap['question'])]=(record,gap)
    for record,gap in gaps.values():
        resolved=reference_units(store,gap.get('resolved_by',[]))
        closed=bool(gap.get('resolved_by')) and all(u in resolved and _applicable(store,resolved[u],p) and content_hash(resolved[u])==gap.get('unit_hashes',{}).get(u) for u in gap['resolved_by'])
        if not closed:blockers.append({'kind':'open_gap','task':record['task'],'question':gap['question']})
    checks=[json.loads(r[0]) for r in store.db.execute('SELECT data FROM learning_checks WHERE program=? AND revision=?',(p['id'],revision))]
    from . import curriculum,implementation
    course=curriculum.current(store)
    roles=('coding','test_generation','review','operations') if course else ('coding','test_generation','review')
    if course:
        sem=implementation.audit(store,module)
        if sem['unclosed_items']:blockers.append({'kind':'implementation_explanation','count':sem['unclosed_items'],'examples':sem['examples']})
        f=curriculum.status(store,module)
        if f['unassigned_assets']:blockers.append({'kind':'unassigned_curriculum_assets','count':len(f['unassigned_assets']),'examples':f['unassigned_assets'][:20]})
        unresolved=[r for r in curriculum.feature_status(store,module) if r['state'] not in {'mapped','duplicate','out_of_scope'}]
        if unresolved:blockers.append({'kind':'historical_feature_mapping','count':len(unresolved),'examples':[{'feature_id':r['id'],'name':r['name'],'state':r['state']} for r in unresolved[:20]]})
    needed={(m['module'],role) for m in s['modules'] for role in roles if any(r['semantic'] and r['module']==m['module'] for r in rows)}
    actual={(x['module'],x['role']) for c in checks if c.get('status')=='passed' for x in c['cases'] if x['passed']}
    if needed-actual:blockers.append({'kind':'consumer_use_cases','count':len(needed-actual),'examples':sorted(needed-actual)[:20]})
    basis={'program':p['id'],'scope_module':module,'revision':revision,'status':s,'report_ids':[r['id'] for r in reports if module is None or r['module']==module],
           'contracts':dict(contracts),'check_ids':[c['id'] for c in checks],'blockers':blockers}
    signature=digest(basis)
    accepted=store.get_meta('coverage-acceptance:'+p['id']+(':'+module if module else ''))
    return {'program':p['id'],'scope_module':module,'snapshot':p['snapshot'],'profile':p['profile'],'knowledge_revision':revision,'digest':signature,
            'status':'accepted' if accepted and accepted['digest']==signature and not blockers else 'ready_for_review' if not blockers else 'incomplete',
            'metrics':{'assets':len(rows),'asset_states':dict(Counter(r['state'] for r in rows)),'semantic_assets':sum(r['semantic'] for r in rows),'candidate_states':dict(Counter(v['state'] for v in s['candidates'].values() if module is None or v['module']==module))},'modules_closed':len(s['modules'])-len(incomplete),'modules_total':len(s['modules']),
            'blockers':blockers,'graph_status':store.record('runs',study.current(store)['run'])['status'],'semantic_accuracy':'requires_actual_review','database_execution':'not_run'}


def accept(store,signature,reviewer,notes,module=None):
    require(not study.current(store).get('worker_scope'),'Coverage acceptance must run on the coordinator with the full program')
    require(reviewer and notes,'Actual coverage reviewer and notes required')
    with store.transaction():
        report=audit(store,module)
        require(report['digest']==signature and not report['blockers'],'Coverage changed or still has blockers')
        value={**report,'reviewer':reviewer,'notes':notes,'at':now(),'acceptance_kind':'source_knowledge_coverage_not_runtime_or_model_accuracy'}
        store.set_meta('coverage-acceptance:'+report['program']+(':'+module if module else ''),value);store.event('coverage_accepted',value)
    return value


def verify_uses(store,cases):
    from .retrieval import get_context
    p=current(store);revision=store.get_meta('knowledge_head');require(revision,'Accepted knowledge required for use checks')
    require(isinstance(cases,list) and 1<=len(cases)<=1000,'Provide 1..1000 use cases')
    require(len({c.get('id') for c in cases})==len(cases),'Use case IDs must be unique')
    from .curriculum import current as course_current
    course=course_current(store);rows=[]
    for c in cases:
        require(c.get('id') and c.get('module') in p['modules'] and c.get('role') in {'coding','test_generation','review','operations'},'Invalid use case')
        require(c.get('query') and c.get('required_units'),'Use case needs question and necessary knowledge IDs')
        pack=get_context(store,{'task':c['role'],'query':c['query'],'targets':c.get('targets',[]),'source_snapshot':p['snapshot'],
             'module':c['module'],'build_profile':p['profile'],'index_run':study.current(store)['run'],'knowledge_revision':revision,'token_budget':c.get('token_budget',64000)})
        delivered=set(pack.get('retrieval',{}).get('knowledge_ids',[]))
        view=pack.get('role_context',{})
        from .role_context import REQUIRED
        satisfied=not view.get('missing_required') and all(view.get('sections',{}).get(name) for name in REQUIRED[c['role']])
        # A bounded view can omit redundant rows while all required source-backed
        # fields and exact necessary units are delivered. Clipping is not a
        # missing knowledge requirement, and must not block every large module.
        rows.append({**c,'passed':set(c['required_units'])<=delivered and (not course or satisfied),
                     'required_content_satisfied':satisfied,
                     'delivered_ids':sorted(delivered),'missing_required':view.get('missing_required',[]),'role_status':view.get('status'),'unknowns':pack.get('unknowns',[])})
    value={'program':p['id'],'revision':revision,'cases':rows,'status':'passed' if all(r['passed'] for r in rows) else 'failed',
           'meaning':'Actual context retrieval contract check, not answer semantic accuracy or blind QA','created':now()}
    value['id']=identity('use-check',value)
    with store.transaction():store.db.execute('INSERT INTO learning_checks VALUES(?,?,?,?)',(value['id'],p['id'],revision,canonical(value)))
    return value


def export(store):
    p=current(store);s=status(store);a=audit(store);folder=store.home/'whole'
    assets=_rows(store,p);domains=Counter(r['domain'] for r in assets)
    tasks=[]
    for row in store.db.execute("SELECT id,kind,status,data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? ORDER BY id",(p['snapshot'],p['plan_id'])):
        b=json.loads(row['data'])['bundle']
        tasks.append({'id':row['id'],'kind':row['kind'],'status':row['status'],'module':b.get('module'),'question':b.get('question'),
                      'candidate_id':b.get('candidate_id'),'selected_files':b.get('selected_files',[]),
                      'dependencies':[r[0] for r in store.db.execute('SELECT dependency FROM task_edges WHERE task=? ORDER BY dependency',(row['id'],))]})
    rows=['# 全仓持续学习计划','',f"快照 `{p['snapshot']}`；配置 `{p['profile']}`；知识 `{s['knowledge_revision']}`。",'',
          f"范围：{s['assets']} 项资产、{len(s['modules'])} 个模块；状态：**{a['status']}**。目录归属和任务不是已学知识。",'',
          '配置→全仓盘点→经审阅的机制规划→按模块持续研究→多人回收/反馈→知识审阅→覆盖与使用验收。','',
          '| 模块 | 资产 | 盘点审阅 | 资产状态 | 源码知识闭合 |','| --- | ---: | --- | --- | --- |']
    domain_rows=['| 领域 | 资产 |','| --- | ---: |']+[f"| {d['id']} / {d['title']} | {domains.get(d['id'],0)} |" for d in p['policy']['domains']]
    if domains.get('unclassified'):domain_rows.append(f"| 待确认领域（已有模块归属） | {domains['unclassified']} |")
    rows[7:7]=['','## 领域范围','',*domain_rows,'','## 模块与持续任务','']
    rows += [f"| {m['module']} | {m['assets']} | {m['inventory_reviewed']} | {canonical(m['states'])} | {m['source_knowledge_closed']} |" for m in s['modules']]
    rows += ['', '## 公共机制与跨域工作包','','| ID | 标题 | 主责模块 | 状态 |','| --- | --- | --- | --- |']
    for t in p['templates']:
        state=store.db.execute('SELECT status FROM tasks WHERE id=?',(t['task'],)).fetchone()[0]
        rows.append(f"| {t['id']} | {t['title']} | {t['module']} | {state} / {t['scope_status']} |")
    rows += ['', '## 当前验收缺口','','```json',json.dumps(a['blockers'],ensure_ascii=False,indent=2),'```','',
             '使用 `next` 获取就绪任务，`run` 连接已有Claude按预算执行；提交后由实际审阅者review，`advance`推进下一批。`coverage`不隐藏阻断项，不自动批准知识。']
    atomic_write(folder/'PLAN.md','\n'.join(rows)+'\n')
    atomic_write(folder/'PLAN.json',json.dumps({'program':p,'progress':s,'domains':dict(domains),'tasks':tasks,'audit':a},ensure_ascii=False,indent=2)+'\n')
    body=['<h1>全仓持续学习计划</h1>',f"<p>{s['assets']}项资产 / {len(s['modules'])}模块 / {escape(a['status'])}</p>",'<p><a href="PLAN.md">完整计划</a> · <a href="PLAN.json">结构化计划</a> · <a href="COVERAGE.csv">逐资产覆盖账</a></p>',
          '<table><tr><th>模块</th><th>资产</th><th>盘点通过</th><th>覆盖状态</th><th>模块闭合</th></tr>']
    body += ['<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in (m['module'],m['assets'],m['inventory_reviewed'],canonical(m['states']),m['source_knowledge_closed']))+'</tr>' for m in s['modules']]
    body += ['</table><h2>验收阻断</h2><pre>'+escape(json.dumps(a['blockers'],ensure_ascii=False,indent=2))+'</pre>']
    atomic_write(folder/'index.html','<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><style>body{margin:2rem;font:15px/1.7 system-ui;color:#172637}table{border-collapse:collapse;width:100%}td,th{padding:.5rem;border:1px solid #ccd6de;text-align:left}pre{white-space:pre-wrap}</style>'+''.join(body)+'</html>')
    content=io.StringIO();writer=csv.writer(content);writer.writerow(['asset','module','domain','semantic','state','sha256','reason','units'])
    for r in assets:writer.writerow([r['asset'],r['module'],r['domain'],r['semantic'],r['state'],r['sha256'],(r['disposition'] or {}).get('reason',r.get('reason')),';'.join((r['disposition'] or {}).get('unit_ids',[]))])
    atomic_write(folder/'COVERAGE.csv','\ufeff'+content.getvalue())
    content=io.StringIO();writer=csv.writer(content);writer.writerow(['task','kind','status','module','question','dependencies','files'])
    for t in tasks:writer.writerow([t['id'],t['kind'],t['status'],t['module'],t['question'],';'.join(t['dependencies']),';'.join(t['selected_files'])])
    atomic_write(folder/'WORK-PACKAGES.csv','\ufeff'+content.getvalue())
    return {'plan':str(folder/'PLAN.md'),'html':str(folder/'index.html'),'json':str(folder/'PLAN.json'),'coverage':str(folder/'COVERAGE.csv'),'work_packages':str(folder/'WORK-PACKAGES.csv'),'program':p['id'],'status':a['status']}
