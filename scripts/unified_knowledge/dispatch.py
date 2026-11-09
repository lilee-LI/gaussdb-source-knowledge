"""Native-host worker dispatch over existing tasks, leases and review state.

This module never starts an LLM/client.  The host's Agent tool executes the safe
handoffs.  Lease secrets live only in the normal private session handles.
"""
from contextlib import contextmanager
import json
from pathlib import Path
import sys
import time
import uuid

from . import planner, study, whole
from .store import identity, now, read_json, require


def _batch_key(value):
    require(isinstance(value,str) and value.startswith('learning-batch:') and len(value)<100,'Invalid learning batch ID')
    return 'dispatch:'+value


def _batch(store,value):
    item=store.get_meta(_batch_key(value))
    require(item,'Learning batch not found')
    p=study.current(store)
    require((item['snapshot'],item['run'],item['plan'])==(p['snapshot'],p['run'],p['id']),'Learning batch belongs to another snapshot/plan')
    return item


def resolve_modules(store,modules):
    """Resolve exact scopes, path prefixes and adapter aliases as module groups."""
    p=study.current(store);available=sorted(p['modules'])
    require(isinstance(modules,(list,tuple)) and modules and all(isinstance(x,str) and x.strip() for x in modules),'Select one or more modules')
    aliases=p.get('product_adapter',{}).get('aliases',{})
    selected=set()
    for raw in modules:
        term=raw.strip().replace('\\','/').rstrip('/');lower=term.casefold()
        if term in p['modules']:matches=[term]
        else:
            terms={lower}
            for key,values in aliases.items():
                if lower==key.casefold() or lower in {str(v).casefold() for v in values}:terms.add(key.casefold())
            matches=[name for name in available if any(
                name.casefold().startswith(t+'/') or name.casefold().endswith('/'+t)
                or '/'+t+'/' in name.casefold() for t in terms)]
        require(matches,'Unknown module scope: '+raw)
        selected.update(matches)
    if p.get('worker_scope'):
        require(selected<={p['worker_scope']},'Member kit is scoped to one assigned module')
    return sorted(selected)


def _scope(store,batch):
    p=study.current(store)
    tasks={r['id']:json.loads(r['data']) for r in store.db.execute(
        "SELECT id,data FROM tasks WHERE snapshot=? AND run=? AND json_extract(data,'$.bundle.plan_id')=?",
        (p['snapshot'],p['run'],p['id']))}
    allowed={tid for tid,t in tasks.items() if t['bundle'].get('module') in batch['modules']}
    if batch['include_dependencies']:
        edges={}
        for r in store.db.execute("SELECT e.task,e.dependency FROM tasks t JOIN task_edges e ON e.task=t.id "
                "WHERE t.snapshot=? AND t.run=? AND json_extract(t.data,'$.bundle.plan_id')=?",
                (p['snapshot'],p['run'],p['id'])):
            edges.setdefault(r['task'],set()).add(r['dependency'])
        todo=list(allowed)
        while todo:
            for dep in edges.get(todo.pop(),()):
                if dep in tasks and dep not in allowed:allowed.add(dep);todo.append(dep)
    effective={tasks[t]['bundle'].get('module') for t in allowed}-{None}
    return tasks,sorted(allowed),sorted(effective-set(batch['modules']))


def _actor(store,worker):return store.get_meta('dispatch-actor:'+worker)


def candidate_allowed(store,worker,task_value):
    """Ordinary workers keep native permissions; delegates use exact task grants."""
    current=study.current(store) if store.get_meta('study_head') else {}
    bundle=task_value.get('bundle',{})
    if current.get('worker_scope') and bundle.get('plan_id')==current.get('id'):
        if bundle.get('module')!=current['worker_scope']:return False
    auth=_actor(store,worker)
    if not auth:return True
    batch=store.get_meta('dispatch:'+auth.get('batch',''),{})
    return bool(auth.get('active') and batch and not batch.get('closed')
        and (auth.get('snapshot'),auth.get('run'),auth.get('plan'))==
            (current.get('snapshot'),current.get('run'),current.get('id'))
        and auth.get('snapshot')==task_value.get('snapshot')
        and auth.get('run')==task_value.get('run')
        and auth.get('plan')==task_value.get('bundle',{}).get('plan_id')
        and task_value.get('id') in auth.get('allowed_tasks',[]))


def authorized_delegate(store,worker,principal,task_value):
    auth=_actor(store,worker)
    return bool(auth and auth.get('principal_worker')==principal and candidate_allowed(store,worker,task_value))


@contextmanager
def _lock(store,key):
    """Short durable mutex; native lease transactions remain non-nested."""
    token=uuid.uuid4().hex;deadline=time.monotonic()+30
    while True:
        acquired=False
        with store.transaction():
            previous=store.get_meta(key)
            if not previous or previous['expires']<time.time():
                store.set_meta(key,{'owner':token,'expires':time.time()+90});acquired=True
        if acquired:break
        require(time.monotonic()<deadline,'Dispatcher is busy; retry this same batch')
        time.sleep(.025)
    try:yield
    finally:
        with store.transaction():
            current=store.get_meta(key)
            if current and current.get('owner')==token:store.db.execute('DELETE FROM meta WHERE key=?',(key,))


def _handle(store,sid):
    from .assistant_session import handle_file
    path=handle_file(store.home,sid)
    require(path.is_file(),'Initialize the parent assistant session first')
    h=read_json(path)
    require(h['snapshot']==study.current(store)['snapshot'],'Session belongs to another source snapshot')
    return path,h


def _save_handle(store,h):
    from .assistant_session import handle_file,_save
    _save(handle_file(store.home,h['session']),h)


def _task_view(store,tid):
    row=store.db.execute('SELECT data,status,attempt,deadline,owner FROM tasks WHERE id=?',(tid,)).fetchone()
    require(row,'Task missing')
    t={**json.loads(row['data']),**{k:row[k] for k in ('status','attempt','deadline','owner')}}
    return {k:t.get(k) for k in ('id','kind','status','attempt','deadline','owner')}|{
        'module':t['bundle'].get('module'),'question':t['bundle'].get('question')}


def _safe_child(store,batch,slot):
    _,h=_handle(store,slot['session']);active=h.get('active');t=None;state='idle'
    if active:
        t=_task_view(store,active['task'])
        if t['status']=='leased':
            row=store.db.execute('SELECT owner,token FROM tasks WHERE id=?',(active['task'],)).fetchone()
            state='superseded' if row['owner']!=slot['worker'] or row['token']!=active['token'] else (
                'running' if t['deadline']>time.time() else 'expired')
        elif t['status']=='submitted':state='awaiting_review'
        elif t['status']=='needs_research':state='needs_research'
        else:state=t['status']
    return {'session':slot['session'],'worker':slot['worker'],'task':t,'state':state,
        'native_agent_id':slot.get('native_agent_id'),'paths':batch.get('paths'),'home':str(store.home),
        'context_command':[sys.executable,str(Path(__file__).resolve().parents[1]/'claude_session.py'),
            *(['--paths',batch['paths']] if batch.get('paths') else ['--home',str(store.home)]),
            '--session',slot['session'],'context']}


def _principal_counts(store,principal):
    plan=study.current(store)
    owners={principal}
    for row in store.db.execute("SELECT value FROM meta WHERE key LIKE 'dispatch-actor:%'"):
        actor=json.loads(row[0])
        if actor.get('principal_worker')==principal:owners.add(actor['worker'])
    pending=active=0
    for row in store.db.execute("SELECT owner,status,deadline FROM tasks WHERE snapshot=? AND run=? "
            "AND json_extract(data,'$.bundle.plan_id')=? AND status IN ('leased','submitted')",
            (plan['snapshot'],plan['run'],plan['id'])):
        if row['owner'] not in owners:continue
        if row['status']=='submitted':pending+=1
        elif row['deadline'] and row['deadline']>time.time():active+=1
    return active,pending


def begin(store,parent_session,paths,modules,parallel=3,include_dependencies=True):
    require(type(parallel) is int and 1<=parallel<=16,'Parallel workers must be 1..16')
    require(type(include_dependencies) is bool,'include_dependencies must be boolean')
    _,parent=_handle(store,parent_session);p=study.current(store)
    require(not _actor(store,parent['worker']),'Delegated children cannot create another batch; use the original parent session')
    selected=resolve_modules(store,modules)
    for module in selected:
        assignment=store.get_meta('assignment:'+p['id']+':'+module,{})
        require(not assignment or assignment['worker']==parent['worker'],'Selected module belongs to another principal worker')
    if paths:
        from .project import settings
        require(Path(paths).is_file(),'Parent paths configuration does not exist')
        require(Path(settings(Path(paths))['home']).resolve()==store.home.resolve(),
            'Parent paths configuration belongs to another workspace')
    with _lock(store,'dispatch-parent-lock:'+parent_session):
        previous=store.get_meta('dispatch-parent:'+parent_session)
        old=store.get_meta('dispatch:'+previous,{}) if previous else {}
        if old and not old.get('closed'):
            require(old['modules']==selected and old['include_dependencies']==include_dependencies,
                    'Close the current batch before selecting another scope')
            require(old['parallel']==parallel,'Close the current batch before changing parallel workers')
            bid=old['id']
        else:
            bid=identity('learning-batch',[p['id'],parent_session,uuid.uuid4().hex])
            item={'schema':'native-learning-batch/v1','id':bid,'parent_session':parent_session,
                'principal_worker':parent['worker'],'snapshot':p['snapshot'],'run':p['run'],'plan':p['id'],
                'modules':selected,'include_dependencies':include_dependencies,'parallel':parallel,
                'paths':str(Path(paths).resolve()) if paths else None,'created':now(),'closed':False,'children':[]}
            for index in range(parallel):
                sid='child-'+uuid.uuid4().hex;worker='delegate-'+uuid.uuid4().hex
                child={'slot':index,'session':sid,'worker':worker}
                item['children'].append(child)
                _save_handle(store,{'schema':'current-assistant-session/v1','session':sid,'worker':worker,
                    'snapshot':p['snapshot'],'paths':item['paths'],'active':None,'parent_session':parent_session,'batch':bid})
            with store.transaction():
                store.set_meta('dispatch:'+bid,item);store.set_meta('dispatch-parent:'+parent_session,bid)
                store.event('learning_batch_created',{'batch':bid,'principal':parent['worker'],'modules':selected,'parallel':parallel})
    return next_batch(store,bid)


def next_batch(store,batch_id):
    with _lock(store,'dispatch-lock:'+batch_id):
        batch=_batch(store,batch_id);require(not batch['closed'],'Learning batch is closed')
        whole.advance(store,max_tasks=max(8,batch['parallel']*2))
        _,allowed,extra=_scope(store,batch);handoffs=[]
        with store.transaction():
            for slot in batch['children']:
                store.set_meta('dispatch-actor:'+slot['worker'],{'worker':slot['worker'],'active':True,
                    'batch':batch_id,'principal_worker':batch['principal_worker'],'parent_session':batch['parent_session'],
                    'snapshot':batch['snapshot'],'run':batch['run'],'plan':batch['plan'],'allowed_tasks':allowed})
        cap=whole.current(store)['policy'].get('max_pending_per_worker',4)
        for slot in batch['children']:
            active_count,pending=_principal_counts(store,batch['principal_worker'])
            _,h=_handle(store,slot['session']);a=h.get('active')
            old=_task_view(store,a['task']) if a else None
            if old and old['status']=='submitted':continue
            if old and old['status']=='leased' and old['deadline']>time.time():continue
            if active_count>=batch['parallel'] or active_count+pending>=cap:break
            # A prior attempt can only be resumed/reclaimed through the native lease.
            target=None
            if old and old['id'] in allowed and old['status'] in {'leased','queued','needs_research'}:
                target=old['id']
            else:
                h['active']=None;_save_handle(store,h)
                selected=whole.next_task(store,slot['worker'])
                if selected['state']=='ready':target=selected['task']['id']
            if not target:continue
            try:leased=planner.lease(store,target,slot['worker'],seconds=14400)
            except ValueError as error:
                # Competing ordinary workers may claim between selection and lease.
                if any(message in str(error) for message in ('claimable','dependencies','knowledge prerequisites')):continue
                raise
            h['active']={'task':target,'token':leased['token'],'attempt':leased['attempt']};_save_handle(store,h)
            handoff=_safe_child(store,batch,slot)
            handoff.update(dispatch='new_attempt' if old and old['id']==target else 'new',
                evidence_must_be_reread=True,
                instructions='Use this child session and context command in the host Agent tool. Do not init another identity. Read task/context/drafts, research and submit, then stop for real review.')
            handoffs.append(handoff)
        with store.transaction():
            store.event('learning_batch_dispatch',{'batch':batch_id,'tasks':[x['task']['id'] for x in handoffs]})
        result=status(store,batch_id)
        result['handoffs']=handoffs;result['dependency_modules']=extra
        result['next']='Spawn only new handoffs with the current host Agent tool. Existing running children must be resumed, not duplicated. Submitted tasks await real review.'
        return result


def status(store,batch_id):
    batch=_batch(store,batch_id);tasks,allowed,extra=_scope(store,batch)
    children=[_safe_child(store,batch,s) for s in batch['children']]
    # Read state columns only. Copying every historical research result makes a
    # status request grow with the knowledge corpus rather than the task ledger.
    rows={r['id']:r for r in store.db.execute("SELECT id,status,owner,deadline,attempt FROM tasks WHERE snapshot=? AND run=? "
        "AND json_extract(data,'$.bundle.plan_id')=?",(batch['snapshot'],batch['run'],batch['plan']))}
    dependencies={}
    for row in store.db.execute("SELECT e.task,e.dependency,d.status FROM tasks t JOIN task_edges e ON e.task=t.id "
            "LEFT JOIN tasks d ON e.dependency=d.id WHERE t.snapshot=? AND t.run=? "
            "AND json_extract(t.data,'$.bundle.plan_id')=?",(batch['snapshot'],batch['run'],batch['plan'])):
        dependencies.setdefault(row['task'],{})[row['dependency']]=row['status']
    states=[{**tasks[tid],**dict(rows[tid]),'dependencies':sorted(dependencies.get(tid,{})),
        'dependency_states':dependencies.get(tid,{})} for tid in allowed]
    counts={}
    for task in states:counts[task['status']]=counts.get(task['status'],0)+1
    from . import curriculum
    blockers=[]
    for task in states:
        if task['status'] not in {'queued','needs_research','leased'}:continue
        if task['status']=='leased' and task.get('deadline',0)>time.time():continue
        reasons=[{'kind':'task_dependency','task':dep,'status':dep_state}
            for dep,dep_state in task['dependency_states'].items() if dep_state!='accepted']
        reasons+=curriculum.prerequisites(store,task)
        order=store.get_meta('assignment:'+batch['plan']+':'+str(task['bundle'].get('module')), {})
        if order and order['worker']!=batch['principal_worker']:
            reasons.append({'kind':'assigned_to_another_principal','worker':order['worker']})
        if reasons and len(blockers)<30:blockers.append({'task':task['id'],'reasons':reasons})
    active,pending=_principal_counts(store,batch['principal_worker'])
    _,inventories,_=whole._report_state(store,whole.current(store))
    def published(task):
        if task['status']!='accepted':return False
        if task['kind']=='module_survey':
            report=inventories.get(task['bundle'].get('module'))
            return bool(report and report['task']==task['id'])
        return whole._task_published(store,task['id'])
    state='closed' if batch['closed'] else 'in_progress' if any(c['state']=='running' for c in children) else (
        'awaiting_review' if any(t['status']=='submitted' for t in states) else
        'complete' if states and all(published(t) for t in states) else 'ready_or_blocked')
    return {'schema':batch['schema'],'batch':batch_id,'state':state,'parent_session':batch['parent_session'],
        'principal_worker':batch['principal_worker'],'selected_modules':batch['modules'],'dependency_modules':extra,
        'parallel':batch['parallel'],'max_open_tasks':whole.current(store)['policy'].get('max_pending_per_worker',4),
        'principal_active_tasks':active,'principal_pending_review':pending,'task_states':counts,
        'children':children,'blockers':blockers,'resume_candidates':[x for x in children if x['state'] in {'running','expired','needs_research'}],
        'execution':'current_host_native_subagents','model_process_started':False,'automatic_acceptance':False}


def close(store,batch_id,release=False):
    require(type(release) is bool,'release must be boolean')
    with _lock(store,'dispatch-lock:'+batch_id):
        batch=_batch(store,batch_id);released=[]
        if release:
            for slot in batch['children']:
                _,h=_handle(store,slot['session']);a=h.get('active')
                if not a:continue
                row=store.db.execute('SELECT status,owner,token,deadline FROM tasks WHERE id=?',(a['task'],)).fetchone()
                if row and row['status']=='leased' and row['owner']==slot['worker'] and row['token']==a['token'] and row['deadline']>time.time():
                    planner.lease(store,a['task'],slot['worker'],action='release',token=a['token'])
                    released.append(a['task']);h['active']=None;_save_handle(store,h)
        with store.transaction():
            batch['closed']=True;batch['closed_at']=now();store.set_meta('dispatch:'+batch_id,batch)
            for slot in batch['children']:
                auth=_actor(store,slot['worker'])
                if auth:auth['active']=False;store.set_meta('dispatch-actor:'+slot['worker'],auth)
            store.event('learning_batch_closed',{'batch':batch_id,'released':released,'acceptance':'not_granted'})
    return {**status(store,batch_id),'released_tasks':released,
        'next':'The host should stop native agents for released tasks. Submitted results remain pending real review; close never accepts knowledge.'}


def attach_agent(store,batch_id,child_session,native_agent_id):
    """Remember a host-provided Agent ID, so a later host can request resume."""
    require(isinstance(native_agent_id,str) and 1<=len(native_agent_id)<=200,'Provide the actual host Agent ID')
    with _lock(store,'dispatch-lock:'+batch_id):
        batch=_batch(store,batch_id);require(not batch['closed'],'Learning batch is closed')
        slot=next((s for s in batch['children'] if s['session']==child_session),None)
        require(slot is not None,'Child session is outside this batch')
        old=slot.get('native_agent_id')
        if old and old!=native_agent_id:
            slot.setdefault('agent_history',[]).append({'id':old,'replaced':now()})
        slot['native_agent_id']=native_agent_id
        with store.transaction():
            store.set_meta('dispatch:'+batch_id,batch)
            store.event('learning_agent_attached',{'batch':batch_id,'child':child_session,'native_agent_id':native_agent_id})
    return {'batch':batch_id,'child_session':child_session,'native_agent_id':native_agent_id,'automatic_acceptance':False}
