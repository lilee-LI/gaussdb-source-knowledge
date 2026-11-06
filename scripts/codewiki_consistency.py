"""Cross-page correction and source-backed consistency gate for native Wiki batches.

All semantic discovery, edits and review run in real Claude Code sessions.
Python freezes inputs, enumerates affected pages, validates evidence/read coverage,
and prevents a stale/open draft from being accepted as a consistent batch.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import codewiki_learning as learning
import codewiki_compare as compare
PROCESS_PAGES={'learning-tasks.md','reuse-ledger.md','comparison-notes.md'}


def knowledge_files(folder):
    return [p for p in sorted(Path(folder).rglob('*.md')) if p.name not in PROCESS_PAGES and '.codewiki' not in p.parts]


def read_ranges(run):
    """Only successful scoped Read results count, not requested tools or guesses."""
    result={}
    for line in (Path(run)/'transcript.jsonl').read_text('utf-8').splitlines():
        event=json.loads(line)
        for item in event.get('message',{}).get('content',[]):
            if not isinstance(item,dict) or item.get('type')!='tool_result' or item.get('is_error'):continue
            content=item.get('content',[])
            if not isinstance(content,list):continue
            for block in content:
                if block.get('type')!='text':continue
                try:value=json.loads(block['text'])
                except (ValueError,TypeError):continue
                if not isinstance(value,dict) or not {'file','total_lines','start_line','end_line','content'}<=value.keys():continue
                result.setdefault(str(Path(value['file']).resolve()),[]).append((value['start_line'],value['end_line']))
    return result


def covers(ranges,start,end):
    next_line=start
    for low,high in sorted(ranges):
        if low>next_line:break
        next_line=max(next_line,high+1)
        if next_line>end:return True
    return end<start


def evidence_ranges(run):
    """Full Read spans plus exact, actually returned, untruncated search lines.

    A search does not imply the surrounding definition was read. In particular,
    matching_lines/truncated summaries never extend coverage beyond real hits.
    Whole-page reading continues to require read_ranges rather than this union.
    """
    result=read_ranges(run)
    for line in (Path(run)/'transcript.jsonl').read_text('utf-8').splitlines():
        event=json.loads(line)
        for item in event.get('message',{}).get('content',[]):
            if not isinstance(item,dict) or item.get('type')!='tool_result' or item.get('is_error'):continue
            blocks=item.get('content',[])
            if not isinstance(blocks,list):continue
            for block in blocks:
                if block.get('type')!='text':continue
                try:value=json.loads(block['text'])
                except (ValueError,TypeError):continue
                if not isinstance(value,dict) or not {'query','matching_lines','matches','truncated','skipped'}<=value.keys():continue
                for hit in value['matches']:
                    if hit.get('line_truncated') is not False:continue
                    result.setdefault(str(Path(hit['file']).resolve()),[]).append((hit['line'],hit['line']))
    return result


def require_read_pages(run,files):
    ranges=read_ranges(run);missing=[]
    for file in files:
        total=len(file.read_text('utf-8').splitlines())
        if not covers(ranges.get(str(file.resolve()),[]),1,total):missing.append(str(file))
    if missing:raise ValueError('Required Wiki pages not completely read: '+json.dumps(missing,ensure_ascii=False))


def validate_refs(refs,cfg,folder,run=None):
    ranges=evidence_ranges(run) if run else None
    for ref in refs:
        root=ref['root']
        if root not in ('source','context','manual','wiki'):raise ValueError('Invalid evidence root')
        p=learning.safe_child(folder if root=='wiki' else cfg[root],ref['file'])
        count=len(p.read_text('utf-8',errors='replace').splitlines())
        start,end=ref['start_line'],ref['end_line']
        if not 1<=start<=end<=count:raise ValueError('Invalid evidence span')
        if ranges is not None and not covers(ranges.get(str(p.resolve()),[]),start,end):
            raise ValueError('Evidence span was not actually read: '+str(p)+':'+str(start))


def validate_issues(issues,cfg,folder,run=None):
    ids=[x['id'] for x in issues]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate issue IDs')
    for issue in issues:
        if not issue.get('terms') or not issue.get('occurrences'):raise ValueError('Issue needs search terms and real occurrences')
        for term in issue['terms']:
            if not isinstance(term,str) or not term.strip() or len(term)>200:raise ValueError('Invalid literal search term')
        for occurrence in issue['occurrences']:
            ref={'root':'wiki',**occurrence};validate_refs([ref],cfg,folder,run)
        validate_refs(issue.get('source_refs',[]),cfg,folder,run)


def build_impact(folder,issues):
    """Enumerate every matching file. Samples may be bounded; file coverage isn't."""
    pages={p.relative_to(folder).as_posix():p.read_text('utf-8').splitlines() for p in knowledge_files(folder)}
    impact=[]
    for issue in issues:
        files={}
        for name,lines in pages.items():
            hits=[{'line':i,'text':line[:450]} for i,line in enumerate(lines,1) if any(term in line for term in issue['terms'])]
            if hits:files[name]={'hit_count':len(hits),'samples':hits[:2]}
        quotes=[]
        for location in issue['occurrences']:
            name=location['file'];lines=pages[name]
            files.setdefault(name,{'hit_count':0,'samples':[]})
            quotes.append({'file':name,'text':'\n'.join(lines[location['start_line']-1:location['end_line']])})
        impact.append({'id':issue['id'],'files':files,'old_quotes':quotes})
    return impact


def remaining_quotes(folder,impact):
    result=[]
    for item in impact:
        for old in item['old_quotes']:
            for p in knowledge_files(folder):
                text=p.read_text('utf-8');needle=old['text']
                if not needle.strip():continue
                offset=0
                while (at:=text.find(needle,offset))>=0:
                    number=text.count('\n',0,at)+1;name=p.relative_to(folder).as_posix()
                    key=hashlib.sha256(f"{item['id']}:{name}:{number}:{needle}".encode()).hexdigest()[:16]
                    result.append({'id':key,'issue':item['id'],'file':name,'line':number,'quote':needle})
                    offset=at+len(needle)
    return result


def gate_result(review,issues,stale):
    expected={x['id'] for x in issues};rows=review['issues']
    if len(rows)!=len(expected) or {x['id'] for x in rows}!=expected:raise ValueError('Incomplete issue review')
    checks=review.get('remaining_quotes',[])
    if len(checks)!=len(stale) or {x['id'] for x in checks}!={x['id'] for x in stale}:raise ValueError('Unreviewed remaining quote')
    if any(x['disposition'] not in ('obsolete','historical_or_negated','unrelated') for x in checks):raise ValueError('Invalid quote disposition')
    return all(x['resolved'] is True for x in rows) and not review.get('new_issues') and not any(x['disposition']=='obsolete' for x in checks)


def validate_repair_updates(updates,issues,impact,folder):
    if len(updates)!=len(issues) or {x['id'] for x in updates}!={x['id'] for x in issues}:raise ValueError('Incomplete repair ledger')
    for update in updates:
        expected=set(next(x for x in impact if x['id']==update['id'])['files'])
        actual=[x['file'] for x in update['files']]
        if len(actual)!=len(set(actual)) or not expected<=set(actual):raise ValueError('Affected file not accounted for')
        if any(x['action'] not in ('corrected','already_consistent','not_applicable') for x in update['files']):raise ValueError('Unknown repair action')
        if not learning.safe_child(folder,update['owner']).is_file():raise ValueError('Missing canonical owner page')


def assert_gate(work):
    work=Path(work);learning.verify_inputs(work)
    state=learning.read_json(work/'state.json');gate=state.get('consistency',{})
    if gate.get('status')!='passed':raise ValueError('Consistency gate has not passed')
    if learning.inventory(work/'D-consistent',True)!=gate['pages']:raise ValueError('Wiki changed after consistency review')
    if learning.inventory(work/'C-specialist',True)!=gate['upstream_pages']:raise ValueError('Upstream Wiki changed after consistency review')
    return gate


def execute_json(cfg,work,label,prompt,scopes,use_mcp=False):
    run=work/'runs'/label
    if (run/'receipt.json').exists():
        receipt=learning.read_json(run/'receipt.json')
        if receipt.get('subtype')!='success' or receipt.get('is_error') or receipt['exit_code']:raise ValueError('Failed phase retained; use a new attempt/trial: '+label)
    else:receipt=learning.execute(cfg,work,label,prompt,use_mcp,scopes)
    allowed=[]
    for scope in scopes.values():allowed.extend(Path(p) for p in scope.get('files',[scope['root']]))
    access=compare.audit_scoped_reads(receipt,allowed,run)
    learning.write_json(run/'access-audit.json',access)
    return compare.parse_run_json(run),receipt


def run_consistency(work,max_rounds=2,seeds=None):
    if max_rounds<1:raise ValueError('At least one consistency round is required')
    work=Path(work).resolve();cfg=learning.read_json(work/'config.json');cfg['scoped_read']=True
    state=learning.read_json(work/'state.json');learning.verify_inputs(work)
    if state.get('consistency',{}).get('status')=='passed':return assert_gate(work)
    if 'specialist' not in state['stages']:raise ValueError('Specialist draft must exist')
    upstream=work/'C-specialist';folder=work/'D-consistent';meta=work/'consistency';meta.mkdir(exist_ok=True)
    before=learning.inventory(upstream,True)
    if before!=state['stages']['specialist']['pages']:raise ValueError('Specialist draft is not frozen')
    if not folder.exists():
        folder.mkdir()
        for p in upstream.rglob('*.md'):
            target=folder/p.relative_to(upstream);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    prior=state.get('consistency',{})
    if prior.get('upstream_pages') and prior['upstream_pages']!=before:raise ValueError('Upstream changed during consistency work')
    state['consistency']={**prior,'status':'in_progress','upstream_pages':before,'rounds':prior.get('rounds',[]),'release_approved':False}
    state['status']='consistency_in_progress'
    learning.write_json(work/'state.json',state)
    scope={k:{'root':cfg[k]} for k in ('source','context','manual')}
    scope['wiki']={'root':str(folder),'files':[str(p) for p in knowledge_files(folder)]}
    issue_schema='{"id":"I01","claim":"待修正的断言","correction":"有前提的新表述或明确未知","terms":["字面检索词"],"occurrences":[{"file":"driver.md","start_line":1,"end_line":4}],"source_refs":[{"root":"source/context/manual","file":"相对路径","start_line":1,"end_line":8}]}'
    seed_note=''
    if seeds:
        seeds=Path(seeds).resolve();scope['leads']={'root':str(seeds.parent),'files':[str(seeds)]}
        seed_note=f'先前调查可作线索：{seeds}。不是标准答案，必须重新回查相关源码；不能读取评测问题或答案。'
    prompt=f'''先读所有知识正文：{json.dumps(scope['wiki']['files'],ensure_ascii=False)}。这是整合纠错，不重写全部模块。
源码 {cfg['source']}；上下文 {cfg['context']}；手册 {cfg['manual']}。{seed_note}
找同一事实跨页面不一致、错误或无证据的绝对保证，特别关注公式/计数、相似参数不同分支、宏条件、错误路径、错误与根因、种子与计划及诊断规则。原文正确的保留；不靠增加篇幅“提升”。
用 scoped read 实际读全知识正文，再检索和读引用代码。每个问题给当前原文真实行范围（尽量只选含问题的句子），以及可用于查找其它受影响页面的2-4个字面词。只读，不修改。
返回严格 JSON {{"issues":[{issue_schema}],"scope_limits":["..."]}}。合并同一事实的重复问题，尽量不超过12项；无问题可空。每项correction限150中文字。保留源码/手册版本边界、not_run。
'''
    if (meta/'issues-initial.json').exists():
        # Original findings refer to pre-repair prose. Never rebase them on edited text.
        detected=learning.read_json(meta/'issues-initial.json')
        if detected!=compare.parse_run_json(work/'runs/consistency-discover'):raise ValueError('Discovery artifact changed')
    else:
        detected,_=execute_json(cfg,work,'consistency-discover',prompt,scope)
        require_read_pages(work/'runs/consistency-discover',knowledge_files(folder))
        validate_issues(detected['issues'],cfg,folder,work/'runs/consistency-discover')
        learning.write_json(meta/'issues-initial.json',detected)
    issues=detected['issues']
    for round_no in range(1,max_rounds+1):
        prefix=f'consistency-{round_no:02d}';round_dir=meta/f'round-{round_no:02d}';round_dir.mkdir(exist_ok=True)
        if (round_dir/'review.json').exists():
            reviewed=learning.read_json(round_dir/'review.json')
            if reviewed!=compare.parse_run_json(work/'runs'/(prefix+'-review')):raise ValueError('Completed review artifact changed')
            if not any(r['round']==round_no for r in state['consistency']['rounds']):raise ValueError('Incomplete round checkpoint')
            issues=reviewed.get('new_issues',[])
            continue
        if (round_dir/'impact.json').exists():
            impact=learning.read_json(round_dir/'impact.json')
            if learning.read_json(round_dir/'issues.json')!={'issues':issues}:raise ValueError('Round issues changed')
        else:
            impact=build_impact(folder,issues);learning.write_json(round_dir/'issues.json',{'issues':issues})
            learning.write_json(round_dir/'impact.json',impact)
        scopes={k:{'root':cfg[k]} for k in ('source','context','manual')}
        scopes['wiki']={'root':str(folder)}
        scopes['review_material']={'root':str(round_dir)}
        methods=[learning.PROJECT/'integrations/codewiki/consistency-learning.md',Path(cfg['module_tree'])]
        scopes['methods']={'root':str(learning.PROJECT.parent),'files':[str(p) for p in methods]}
        if issues:
            prompt=f'''修订整合稿 {folder}，原 C 组不能修改。必须实际读取 {methods[0]}、{round_dir/'issues.json'}、{round_dir/'impact.json'}。
实际源码 {cfg['source']}、上下文 {cfg['context']}、手册 {cfg['manual']}。analyze_repo(repo_path={cfg['source']},output_dir={folder})，save_module_tree 使用 {cfg['module_tree']}，用 CodeWiki write_doc_file/edit_doc_file 修订。
逐问题核对证据，为事实指定一个现有页面作为主要说明；修订所有受影响的机制页、示例、专题和诊断规则，其他页面可链接引用。impact列出所有词法命中的文件，不表示它们全部有错；逐文件实际读后分别纠正或说明已一致/不适用。
公式、最小输入按调用次序手算；参数分别核消费者；没有完整异常链就撤回无条件保证；错误检测状态不能推导唯一上游原因。不要把未证内容删除到只剩空话，保留局部已证机制及具体边界。手册版本不能合并推断为产品等价。
不读测试题或评分记录。只通过 CodeWiki 修改 D 组 Markdown，保留原文外的研究记录；不得把问题清单当已修复证明。完成后回读涉及页面并 close_session。
最终返回简短 JSON {{"issue_updates":[{{"id":"I01","owner":"fitness.md","files":[{{"file":"driver.md","action":"corrected/already_consistent/not_applicable","reason":"限40字"}}]}}],"unresolved":["..."]}}。每个问题的 files 必须覆盖 impact 中该问题的完整文件集合。不要在最终响应重复文章。
'''
            repair,receipt=execute_json(cfg,work,prefix+'-repair',prompt,scopes,True)
            if not receipt['tool_counts'].get('mcp__codewiki__close_session'):raise ValueError('Repair did not close native session')
            validate_repair_updates(repair['issue_updates'],issues,impact,folder)
            learning.write_json(round_dir/'repair-ledger.json',repair)
        stale=remaining_quotes(folder,impact);learning.write_json(round_dir/'remaining-quotes.json',stale)
        frozen=learning.inventory(folder,True);files=knowledge_files(folder)
        freeze_file=round_dir/'repaired-pages.json'
        if freeze_file.exists() and learning.read_json(freeze_file)!=frozen:raise ValueError('Draft changed while review was pending')
        if not freeze_file.exists():learning.write_json(freeze_file,frozen)
        scopes['wiki']={'root':str(folder),'files':[str(p) for p in files]}
        prompt=f'''独立检查修订后的知识稿，不修改。先完整读取所有正文：{json.dumps([str(p) for p in files],ensure_ascii=False)}。
再读问题 {round_dir/'issues.json'}、完整影响范围 {round_dir/'impact.json'}、残留原句 {round_dir/'remaining-quotes.json'}。
对每项问题实际回查相关源码和手册，确认所有受影响页面都一致，不把记录写“已修”当证据。检查主要说明、引用、示例、诊断规则有无旧结论，新增确定性断言是否过强。特别检查“局部机制正确+无条件额外保证”的组合，不能以主体正确放过错误保证。
逐条检查残留原句：obsolete（当前仍在断言错误）、historical_or_negated（明确反例/否定）、unrelated；每个id必须有结论。未残留原词不等于语义正确，仍检查所有正文。只读。
输出严格 JSON {{"issues":[{{"id":"I01","resolved":true,"reason":"限100字","evidence":[{{"root":"wiki/source/context/manual","file":"相对路径","start_line":1,"end_line":8}}]}}],"remaining_quotes":[{{"id":"给定ID","disposition":"obsolete/historical_or_negated/unrelated","reason":"..."}}],"new_issues":[{issue_schema}],"limitations":["..."]}}。
每个输出引用行段都要在本轮通过 read_text 实际读取；搜索命中只用于定位，不凭符号摘要猜测全文。讨论不可达性必须写清入口不变量与异常/损坏状态边界，讨论期望次数必须明确哪些随机变量在循环内重新抽取。
如果问题未解决，resolved=false并在new_issues中用新ID给出当前真实位置、检索词与证据，供下一轮修订。每个已解决问题至少引一处修订后的wiki与一处实际读过的source/context证据。不能靠多数投票或文章长度通过。
'''
        review,_=execute_json(cfg,work,prefix+'-review',prompt,scopes)
        if learning.inventory(folder,True)!=frozen:raise ValueError('Reviewer changed frozen Wiki')
        require_read_pages(work/'runs'/ (prefix+'-review'),files)
        for row in review['issues']:
            if row['resolved'] and not {'wiki'}<= {r['root'] for r in row['evidence']}:raise ValueError('Resolved issue lacks revised prose evidence')
            if row['resolved'] and not {'source','context'} & {r['root'] for r in row['evidence']}:raise ValueError('Resolved issue lacks implementation evidence')
            validate_refs(row['evidence'],cfg,folder,work/'runs'/(prefix+'-review'))
        validate_issues(review.get('new_issues',[]),cfg,folder,work/'runs'/(prefix+'-review'))
        passed=gate_result(review,issues,stale)
        learning.write_json(round_dir/'review.json',review)
        state['consistency']['rounds'].append({'round':round_no,'issues':len(issues),'remaining_quotes':len(stale),'passed':passed,'review':str(round_dir/'review.json')})
        state['consistency'].update(status='passed' if passed else 'open',pages=frozen,
            review_receipt=str(work/'runs'/(prefix+'-review')/'receipt.json'),runtime_validation='not_run')
        state['status']='consistency_passed' if passed else 'consistency_open'
        learning.write_json(work/'state.json',state)
        if passed:
            assert_gate(work)
            print(json.dumps({'consistency':'passed','round':round_no,'pages':len(frozen),'release_approved':False}));return state['consistency']
        issues=review.get('new_issues',[])
        if not issues:raise ValueError('Open review has no actionable issues; cannot silently continue')
    print(json.dumps({'consistency':'open','rounds':max_rounds,'release_approved':False}))
    return state['consistency']


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('run','check'))
    parser.add_argument('--work',required=True,type=Path);parser.add_argument('--max-rounds',type=int,default=2);parser.add_argument('--seeds',type=Path)
    args=parser.parse_args()
    if args.action=='check':print(json.dumps(assert_gate(args.work),ensure_ascii=False));return
    result=run_consistency(args.work,args.max_rounds,args.seeds)
    if result['status']!='passed':raise SystemExit(2)


if __name__=='__main__':main()
