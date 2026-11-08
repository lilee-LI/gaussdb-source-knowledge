"""Bounded native Claude sessions over the same task queue; never auto-review."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

from .store import atomic_write,now,require


def claude_executable(explicit=None):
    if explicit:
        path=Path(explicit).expanduser().resolve()
        require(path.is_file(),'Claude executable does not exist')
        require(path.suffix.lower() not in {'.ps1','.cmd','.bat'},'Select the native Claude executable, not a shell wrapper')
        return str(path)
    # npm on Windows installs a shell shim; launch the existing native binary.
    candidates=[shutil.which('claude.exe')]
    if os.name=='nt':
        candidates += [str(Path(os.environ.get('APPDATA',''))/'npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe'),
                       str(Path.home()/'.local/bin/claude.exe')]
    else:candidates += [shutil.which('claude')]
    for item in candidates:
        if item and Path(item).is_file():return str(Path(item).resolve())
    raise ValueError('Install/login to Claude Code on this server, or pass --claude /path/to/native/claude. It is not bundled.')


def run(store,*,worker,module=None,steps=1,timeout=1800,budget=3,executable=None,resume_task=None):
    from . import whole
    from .planner import task_status
    from .project import research_prompt
    require(isinstance(worker,str) and worker.strip(),'Named worker required')
    require(type(steps) is int and 1<=steps<=100 and type(timeout) is int and 10<=timeout<=86400,'Bound steps 1..100 and per-task timeout 10..86400s')
    require(isinstance(budget,(int,float)) and 0<budget<=100,'Per-session budget must be >0 and <=100')
    command=claude_executable(executable)
    mcp=store.home/('worker.mcp.json' if whole.study.current(store).get('worker_scope') else 'researcher.mcp.json')
    require(mcp.is_file(),'Run start or team open --kit to create the local MCP configuration')
    sessions=[];stopped='step_limit'
    for _ in range(steps):
        whole.advance(store)
        continuation=None
        if resume_task:
            t=task_status(store,resume_task);row=store.db.execute('SELECT token,owner,status,deadline FROM tasks WHERE id=?',(resume_task,)).fetchone()
            require(row['owner']==worker and row['status']=='leased' and row['deadline']>time.time(),'Resume requires this worker\'s active, unexpired lease')
            require(t['snapshot']==whole.current(store)['snapshot'] and (module is None or t['bundle'].get('module')==module),'Resume task scope mismatch')
            from .planner import lease
            lease(store,resume_task,worker,action='renew',token=row['token'],seconds=14400)
            continuation=row['token'];next_item={'state':'ready','task':t};resume_task=None
        else:next_item=whole.next_task(store,worker,module)
        if next_item['state']!='ready':stopped=next_item['state'];break
        task=next_item['task'];folder=store.home/'sessions'/(time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
        folder.mkdir(parents=True)
        prompt=research_prompt(task['id'],worker,task['bundle'].get('question') or '盘点模块所有资产、归并机制问题，登记覆盖和后续研究提案。')
        if task['status']=='needs_research':prompt+=' 本任务被实际审阅退回：task_context.review_feedback及其review.notes是必须修正项。领取新租约后回读涉及证据，保留合理规划并明确纠正错误表述，不能原样重复提交；以前租约的阅读不算当前阅读。'
        if task['kind']=='module_survey':
            prompt+=' 本轮是模块盘点：分页列出全部资产与feature_candidates线索，抽样核对范围、入口和设计缺口，将机制问题归并为1到4个proposals（不要逐函数建单）。本轮所有资产先登记disposition=deferred、unit_ids=[]、evidence_refs为实际阅读区间，reason写后续研究问题；不要填写studied、excluded或假知识ID。inventory_complete只表示本轮范围盘点完成，不代表代码学完。本轮不用stage_research_unit，只用stage_progress与progress_digest提交规划，由后续feature_research深入。'
        if continuation:
            prompt+=' 这是同一有效租约的断点续作，不要再次claim或release。当前租约token='+continuation+'；先task_context查看active_drafts和active_progress，复用本租约已读证据与已暂存内容。若草稿已完整，核对后直接finish_research；不要重建整套草稿或输出token。'
        atomic_write(folder/'prompt.txt',prompt)
        args=[command,'-p','--strict-mcp-config','--mcp-config',str(mcp),'--allowedTools','mcp__gaussdb_knowledge__*',
              '--permission-mode','dontAsk','--max-budget-usd',str(budget),'--output-format','stream-json','--verbose','--no-session-persistence']
        begin=time.monotonic();timed_out=False;stopped_after_submission=False
        with (folder/'stdout.jsonl').open('wb') as output,(folder/'stderr.log').open('wb') as errors:
            process=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=output,stderr=errors,cwd=Path(__file__).resolve().parents[2])
            try:
                try:process.communicate(prompt.encode('utf-8'),timeout=2)
                except subprocess.TimeoutExpired:
                    while process.poll() is None:
                        if task_status(store,task['id'])['status']=='submitted':
                            try:process.communicate(timeout=8)
                            except subprocess.TimeoutExpired:
                                stopped_after_submission=True;process.terminate();process.communicate()
                            break
                        remaining=timeout-(time.monotonic()-begin)
                        if remaining<=0:
                            timed_out=True;process.kill();process.communicate();break
                        try:process.communicate(timeout=min(2,remaining))
                        except subprocess.TimeoutExpired:pass
            except BaseException:
                process.kill();process.communicate();raise
        state=task_status(store,task['id']);model=[];cli_version=None
        for line in (folder/'stdout.jsonl').read_text(encoding='utf-8',errors='replace').splitlines():
            try:
                event=json.loads(line)
                message=event.get('message',{})
                cli_version=event.get('claude_code_version') or cli_version
                candidate=(message.get('model') if isinstance(message,dict) else None) or event.get('model')
                if candidate and candidate not in model:model.append(candidate)
            except (ValueError,AttributeError):pass
        result={'task':task['id'],'worker':worker,'module':task['bundle'].get('module'),'created':now(),'seconds':round(time.monotonic()-begin,3),
                'exit_code':process.returncode,'timed_out':timed_out,'task_status':state['status'],'models':model,
                'stopped_after_submission':stopped_after_submission,
                'directory':str(folder),'cli_executable':command,'cli_version':cli_version or 'not_reported_by_cli',
                'review':'not_performed','source_only':True}
        atomic_write(folder/'result.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n');sessions.append(result)
        if (process.returncode!=0 and not stopped_after_submission) or state['status']!='submitted':stopped='session_needs_attention';break
    whole.export(store)
    return {'sessions':sessions,'stopped':stopped,'next':'Review submitted results with review; advance after actual approval. Active/failed leases can be checkpointed/released; no automatic acceptance.'}
