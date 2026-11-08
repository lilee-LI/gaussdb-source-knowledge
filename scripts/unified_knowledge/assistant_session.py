"""Thin current-assistant adapter over native project/tasks/evidence/review APIs.

No Claude SDK, model subprocess, alternative queue or automatic semantic approval.
Opaque lease tokens stay in a private session handle, never in tool output.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sqlite3
import time
import uuid

from . import project,study,whole,planner,service
from .store import Store,atomic_write,digest,read_json,require


def session_id(value):
    require(isinstance(value,str) and re.fullmatch(r'[A-Za-z0-9_-]{1,100}',value),'Use a session ID containing letters/digits/_/- (1..100 characters)')
    return value


def handle_file(home,sid):return Path(home)/'assistant-sessions'/session_id(sid)/'handle.json'


def _save(path,value):
    atomic_write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    try:Path(path).chmod(0o600)
    except OSError:pass


def payload(args):
    if getattr(args,'input',None):
        require(Path(args.input).stat().st_size<=2_000_000,'Split this input into smaller units')
        return read_json(args.input)
    require(getattr(args,'stdin',False),'Supply --input a UTF-8 JSON file, or --stdin')
    value=__import__('sys').stdin.read(2_000_001)
    require(len(value)<=2_000_000,'Split this input into smaller units')
    return json.loads(value.lstrip('\ufeff'))


def initialize(args):
    sid=session_id(args.session or uuid.uuid4().hex)
    if args.paths:
        require(not any((args.source,args.manual,args.home,args.index_db)),'Use --paths or individual material paths')
        path=Path(args.paths).expanduser().resolve();spec=project.settings(path)
    else:
        require(args.source,'Provide --source and optional --manual, or --paths')
        source=Path(args.source).expanduser().resolve()
        manual=Path(args.manual).expanduser().resolve() if args.manual else None
        home=Path(args.home).expanduser().resolve() if args.home else Path.home()/'gaussdb-knowledge'/digest([str(source),str(manual)])[:12]
        spec={'product':args.product,'product_adapter':args.adapter,'source':str(source),'home':str(home)}
        if manual:spec['manual']=str(manual)
        if args.index_db:spec.update(index_db=str(Path(args.index_db).expanduser().resolve()),graph_storage='reference')
        path=home/'assistant-paths.json'
        # Preflight before creating files, including overlap/graph compatibility.
        project.check({**spec,'repository_roots':{}})
        require(not path.exists() or read_json(path)==spec,'This workspace already has different paths; use a new --home or edit its configuration explicitly')
        _save(path,spec);spec=project.settings(path)
    result=project.start(spec,args.refresh)
    file=handle_file(spec['home'],sid);old=read_json(file) if file.is_file() else None
    worker=args.worker or (old or {}).get('worker') or 'claude-'+sid[:20]
    require(not old or old['worker']==worker,'Session worker identity changed; choose a different session ID')
    require(not old or old['snapshot']==result['source_snapshot'],'Materials changed; use a new session ID to preserve the previous handle')
    value=old or {'schema':'current-assistant-session/v1','session':sid,'worker':worker,'snapshot':result['source_snapshot'],'paths':str(path),'active':None}
    _save(file,value)
    return {'session':sid,'worker':worker,'paths':str(path),'home':spec['home'],'mode':result['mode'],
            'plan':result['whole_plan'],'execution':'current_assistant_session','nested_model_process':False,
            'next':'Use modules, then next --module <exact module ID>. Keep this session and paths in subsequent calls.'}


def _handle(store,args,required=True):
    require(args.session,'Use the session returned by init (or the current Claude session ID)')
    path=handle_file(store.home,args.session)
    require(path.is_file(),'Initialize this session with --paths ... --session ... init')
    value=read_json(path);p=study.current(store)
    require(value['snapshot']==p['snapshot'],'Session belongs to another source snapshot; initialize a new session')
    require(value.get('active') or not required,'No active task; use next')
    return path,value


def _credentials(store,args):
    path,h=_handle(store,args)
    a=h['active'];planner._check_lease(store,a['task'],h['worker'],a['token'])
    return path,h,{'task':a['task'],'worker':h['worker'],'token':a['token']}


def _context(store,tid):
    value=planner.task_context(store,tid)
    run=store.record('runs',value['run']);source_only=run.get('mode') in {'source_only','inventory'}
    value['capabilities']={'frozen_source_and_manuals':True,'compiler_graph':not source_only,'source_only':source_only}
    value['execution']='current_assistant_session'
    value['next_actions']=['assets / candidates / read / search','unit / progress','submit; then stop at awaiting_review']
    if source_only:
        value['source_only_guidance']='Use source_refs with claim/mechanism/feature/responsibility/test_obligation and flow data_stage/state_transition. No compiler-confirmed symbols, call steps or symbol-endpoint contracts; record those as unverified. Do not run index/build/TU parsing.'
    return value


def next_task(store,args):
    path,h=_handle(store,args,False)
    active=h.get('active')
    if active:
        current=planner.task_status(store,active['task'])
        require(current['status']=='accepted' or not args.module or current['bundle'].get('module')==args.module,
                'This session already has an active task in another module; submit/review or release it before switching')
        row=store.db.execute('SELECT status,token,owner,deadline FROM tasks WHERE id=?',(active['task'],)).fetchone()
        if row and row['status']=='leased':
            require(row['owner']==h['worker'] and row['token']==active['token'],'This handle was superseded; it cannot reclaim another lease')
            if row['deadline']<time.time():
                leased=planner.lease(store,active['task'],h['worker'],seconds=14400)
                h['active']={'task':active['task'],'token':leased['token'],'attempt':leased['attempt']};_save(path,h)
                return {'state':'reclaimed','evidence_must_be_reread':True,'task':_context(store,active['task'])}
            planner.lease(store,active['task'],h['worker'],action='renew',token=active['token'],seconds=14400)
            return {'state':'resumed','task':_context(store,active['task'])}
        if row and row['status']=='submitted':return {'state':'awaiting_review','task':active['task'],'next':'Review the submitted research; it is not accepted knowledge yet.'}
        if row and row['status'] in {'queued','needs_research'}:
            leased=planner.lease(store,active['task'],h['worker'],seconds=14400)
            h['active']={'task':active['task'],'token':leased['token'],'attempt':leased['attempt']};_save(path,h)
            return {'state':'reclaimed','evidence_must_be_reread':True,'task':_context(store,active['task'])}
        h['active']=None
        _save(path,h)
    whole.advance(store,max_tasks=8)
    chosen=whole.next_task(store,h['worker'],args.module)
    if chosen['state']!='ready':return chosen
    tid=chosen['task']['id'];leased=planner.lease(store,tid,h['worker'],seconds=14400)
    h['active']={'task':tid,'token':leased['token'],'attempt':leased['attempt']};_save(path,h)
    return {'state':'claimed','task':_context(store,tid)}


def execute(args):
    if args.action=='init':return initialize(args)
    require(args.paths,'Use --paths returned by init')
    spec=project.settings(Path(args.paths));home=Path(spec['home'])
    require((home/'knowledge.sqlite3').is_file(),'Initialize the workspace first')
    with Store(home) as store:
        plan=study.current(store)
        if args.action=='materials':
            require(args.offset>=0 and 1<=args.limit<=200,'Read 1..200 material entries per page')
            where="snapshot=? AND kind=? AND instr(lower(key),lower(?))>0"
            values=(plan['snapshot'],args.kind,args.query or '')
            total=store.db.execute('SELECT count(*) FROM assets WHERE '+where,values).fetchone()[0]
            rows=store.db.execute('SELECT key,kind,status,data FROM assets WHERE '+where+' ORDER BY key LIMIT ? OFFSET ?',(*values,args.limit,args.offset)).fetchall()
            return {'total':total,'items':[{'asset':r['key'],'kind':r['kind'],'status':r['status'],'bytes':json.loads(r['data']).get('bytes')} for r in rows],
                    'next_offset':args.offset+len(rows) if args.offset+len(rows)<total else None}
        if args.action=='modules':
            require(args.offset>=0 and 1<=args.limit<=200,'Read 1..200 modules per page')
            rows=[];query=(args.query or '').casefold()
            aliases=plan.get('product_adapter',{}).get('aliases',{})
            terms={query}|{key.casefold() for key,values in aliases.items() if query in [v.casefold() for v in values]}
            for name,info in sorted(plan['modules'].items()):
                if query and not any(t in name.casefold() for t in terms):continue
                row=store.db.execute('SELECT status FROM tasks WHERE id=?',(info['task'],)).fetchone()
                rows.append({'module':name,'assets':len(info['files']),'survey_task':info['task'],'status':row[0]})
            return {'total':len(rows),'items':rows[args.offset:args.offset+args.limit],'next_offset':args.offset+args.limit if args.offset+args.limit<len(rows) else None}
        if args.action=='plan':return whole.export(store)
        if args.action=='next':return next_task(store,args)
        if args.action=='status':
            _,h=_handle(store,args,False)
            state=planner.task_status(store,h['active']['task']) if h.get('active') else None
            return {'session':h['session'],'worker':h['worker'],'snapshot':plan['snapshot'],'run':plan['run'],'knowledge_revision':store.get_meta('knowledge_head'),
                    'active_task':{'id':state['id'],'status':state['status'],'attempt':state['attempt']} if state else None}
        if args.action=='review':
            _,h=_handle(store,args,False)
            tid=args.task or (h.get('active') or {}).get('task');require(tid,'Provide --task')
            t=planner.task_status(store,tid)
            # This actor is tied to the current session; do not invent reviewer aliases.
            reviewer=h['worker'];mode='self_reviewed' if t.get('result',{}).get('worker')==reviewer else 'independent_review'
            if args.accept or args.reject:
                require(mode!='self_reviewed' or args.self_review,'Same session authored this result; explicit --self-review is required and remains self_reviewed')
            result=project.review_step(store,argparse.Namespace(task=tid,reviewer=reviewer,notes=args.notes,
                    accept=args.accept,return_for_research=args.reject))
            return {**result,'review_mode':mode,'reviewer':reviewer,'human_expert_review':False}
        if args.action=='wiki':
            from .reader_wiki import export_wiki
            return export_wiki(store)
        if args.action=='coverage':return whole.audit(store,args.module)
        if args.action=='advance':return whole.advance(store,args.limit)
        if args.action=='ask':
            from .retrieval import get_context
            return get_context(store,{'task':args.role,'query':args.question,'source_snapshot':plan['snapshot'],'build_profile':plan['profile'],'index_run':plan['run'],'token_budget':args.budget})
        path,h,credentials=_credentials(store,args)
        if args.action=='context':return _context(store,credentials['task'])
        if args.action=='assets':
            module=planner.task_status(store,credentials['task'])['bundle'].get('module')
            require(module,'This is a repository scope task; use its selected_files in context')
            return whole.module_assets(store,module,args.offset,args.limit)
        if args.action=='candidates':
            from .catalog import listing
            module=planner.task_status(store,credentials['task'])['bundle'].get('module')
            return listing(store,plan,module=module,offset=args.offset,limit=args.limit)
        if args.action=='read':return whole.read_source(store,**credentials,asset=args.asset,start=args.start,lines=args.lines)
        if args.action=='search':return whole.search_source(store,**credentials,query=args.query,asset_patterns=args.asset,limit=args.limit,offset=args.offset,line_offset=args.line_offset)
        if args.action=='drafts':return planner.read_research_drafts(store,**credentials,ids=args.id,offset=args.offset,limit=args.limit)
        if args.action in {'symbols','graph'}:
            if _context(store,credentials['task'])['capabilities']['source_only']:
                return {'available':False,'reason':'Source-only workspace; use frozen source search/read and record compiler facts as unverified.'}
            if args.action=='symbols':return service.invoke(store,'lookup_symbols',{'run':plan['run'],'query':args.query,'limit':args.limit})
            return service.invoke(store,'query_graph',{'run':plan['run'],'targets':args.target,'direction':'both','depth':1,'limit':args.limit,'kinds':['CALLS']})
        if args.action=='unit':
            unit=payload(args)
            if _context(store,credentials['task'])['capabilities']['source_only']:
                require(not unit.get('symbol_refs') and unit.get('kind')!='contract' and not any(s.get('kind')=='call' for s in unit.get('steps',[])),
                        'Source-only evidence has no compiler symbol IDs; use source-backed claims/mechanisms or data/state stages, and retain contract/call validation as gaps')
            return planner.stage_research_unit(store,**credentials,unit=unit,previous_hash=args.previous_hash)
        if args.action=='progress':return whole.stage_progress(store,**credentials,report=payload(args),previous_digest=args.previous_digest)
        if args.action=='submit':
            row=planner._check_lease(store,**credentials);attempt=str(row['attempt'])
            drafts=store.get_meta('research_drafts:'+credentials['task']+':'+attempt,{})
            progress=store.get_meta('progress-draft:'+credentials['task']+':'+attempt)
            result=planner.finish_research(store,**credentials,coverage=payload(args),drafts_digest=digest(drafts),progress_digest=digest(progress) if progress else None)
            with store.transaction():
                store.event('assistant_session_submit',{'session':h['session'],'worker':h['worker'],
                    'task':credentials['task'],'result_digest':result['result_digest'],'execution':'current_assistant_session'})
            return {**result,'execution':'current_assistant_session','next':'Stop research. The committed result is awaiting actual review.'}
        if args.action in {'renew','release','checkpoint'}:
            result=planner.lease(store,**credentials,action=args.action,seconds=14400,checkpoint=payload(args) if args.action=='checkpoint' else None)
            if args.action=='release':h['active']=None;_save(path,h)
            return {'task':result['id'],'status':result['status'],'attempt':result['attempt'],'deadline':result['deadline']}
    raise ValueError('Unknown current-session action')


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--paths',type=Path);p.add_argument('--session',default=os.environ.get('CLAUDE_SESSION_ID'))
    sub=p.add_subparsers(dest='action',required=True)
    a=sub.add_parser('init');a.add_argument('--source',type=Path);a.add_argument('--manual',type=Path);a.add_argument('--home',type=Path)
    a.add_argument('--index-db',type=Path);a.add_argument('--product',default='GaussDB');a.add_argument('--adapter',default='gaussdb')
    a.add_argument('--worker');a.add_argument('--refresh',action='store_true')
    a=sub.add_parser('materials');a.add_argument('--kind',choices=['document','source','method'],default='document')
    a.add_argument('--query');a.add_argument('--offset',type=int,default=0);a.add_argument('--limit',type=int,default=30)
    for name in ('modules','assets','candidates','drafts','advance'):
        a=sub.add_parser(name);a.add_argument('--offset',type=int,default=0);a.add_argument('--limit',type=int,default=10 if name in {'drafts','advance'} else 30)
        if name=='modules':a.add_argument('--query')
        if name=='drafts':a.add_argument('--id',action='append')
    for name in ('plan','status','context','wiki','next','coverage','renew','release'):
        a=sub.add_parser(name)
        if name in {'next','coverage'}:a.add_argument('--module')
    a=sub.add_parser('read');a.add_argument('--asset',required=True);a.add_argument('--start',type=int,default=1);a.add_argument('--lines',type=int,default=200)
    a=sub.add_parser('search');a.add_argument('--query',required=True);a.add_argument('--asset',action='append');a.add_argument('--limit',type=int,default=30)
    a.add_argument('--offset',type=int,default=0);a.add_argument('--line-offset',type=int,default=0)
    for name in ('unit','progress','submit','checkpoint'):
        a=sub.add_parser(name);source=a.add_mutually_exclusive_group(required=True);source.add_argument('--input',type=Path);source.add_argument('--stdin',action='store_true')
        if name=='unit':a.add_argument('--previous-hash')
        if name=='progress':a.add_argument('--previous-digest')
    for name in ('symbols','graph'):
        a=sub.add_parser(name);a.add_argument('--limit',type=int,default=20)
        if name=='symbols':a.add_argument('--query',required=True)
        else:a.add_argument('--target',action='append',required=True)
    a=sub.add_parser('ask');a.add_argument('--role',choices=['coding','test_generation','review','operations'],default='coding');a.add_argument('--question',required=True);a.add_argument('--budget',type=int,default=32768)
    a=sub.add_parser('review');a.add_argument('--task');decision=a.add_mutually_exclusive_group();decision.add_argument('--accept');decision.add_argument('--reject')
    a.add_argument('--notes');a.add_argument('--self-review',action='store_true')
    return p


def main(argv=None):
    try:
        value=execute(parser().parse_args(argv));print(json.dumps(value,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error) as error:
        print(json.dumps({'error':str(error)},ensure_ascii=False),file=__import__('sys').stderr);return 1
