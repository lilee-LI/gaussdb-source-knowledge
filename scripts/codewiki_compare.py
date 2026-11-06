"""Wiki-only readback and source-grounded comparison, using real Claude Code runs."""
import argparse
import json
from pathlib import Path
import re

import codewiki_learning as learning


def message_content(event):
    message=event.get('message',{})
    return message.get('content',[]) if isinstance(message,dict) else []


def parse_json_result(text):
    text=text.strip()
    # A short preamble is not data. Accept exactly one complete JSON fence,
    # preserving the raw model result; never guess between multiple payloads.
    fences=re.findall(r'^```(?:json)?\s*\n(.*?)\n```\s*$',text,re.M|re.S)
    if len(fences)==1 and text.count('```')==2:
        text=fences[0]
    value=json.loads(text)
    if not isinstance(value,dict):raise ValueError('Expected JSON object')
    return value


def parse_run_json(run):
    raw=(run/'result.txt').read_text('utf-8')
    try:return parse_json_result(raw)
    except json.JSONDecodeError:pass
    # Claude can split a final answer at its token limit. The terminal result
    # then contains only the continuation. Rejoin recorded text verbatim only
    # when a synthetic continuation is present; do not invent missing content.
    parts=[];continuations=0
    for line in (run/'transcript.jsonl').read_text('utf-8').splitlines():
        event=json.loads(line);content=message_content(event)
        if event.get('type')=='assistant':
            if any(isinstance(x,dict) and x.get('type')=='tool_use' for x in content):
                parts=[];continuations=0
            else:parts.extend(x['text'] for x in content if isinstance(x,dict) and x.get('type')=='text')
        elif event.get('type')=='user' and event.get('isSynthetic') and any(
                isinstance(x,dict) and x.get('text','').startswith('Output token limit hit. Resume directly') for x in content):
            continuations+=1
    if not continuations:raise ValueError('No valid JSON or recorded continuation')
    combined=parts[0];overlaps=[]
    for part in parts[1:]:
        overlap=0
        # A continuation may restart the incomplete JSON row. Remove only an
        # exact, substantial repeated prefix, never rewrite or complete a row.
        if re.match(r'\s*\{\s*"id"\s*:',part):
            overlap=next((n for n in range(min(len(combined),len(part)),63,-1)
                if combined.endswith(part[:n])),0)
        combined=(combined[:-overlap] if overlap else combined)+part
        overlaps.append(overlap)
    value=parse_json_result(combined)
    (run/'continued-result.txt').write_text(combined,encoding='utf-8')
    learning.write_json(run/'result-recovery.json',{'method':'verbatim_terminal_assistant_parts',
        'parts':len(parts),'synthetic_continuations':continuations,'exact_overlap_characters':overlaps,'raw_result_preserved':True})
    return value


def validate_rows(rows, questions):
    ids=[row['id'] for row in rows]
    expected=[row['id'] for row in questions]
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected):
        raise ValueError('Missing, unexpected or duplicated question IDs')


def check_read_paths(receipt, allowed):
    """Post-run access audit, not a filesystem sandbox."""
    allowed=[Path(p).resolve() for p in allowed]
    violations=[]
    for call in receipt['tool_calls']:
        inp=call.get('input') or {}
        if call['name'] not in ('Read','Grep','Glob','mcp__learning__read_text'):continue
        raw=inp.get('file_path') if call['name'] in ('Read','mcp__learning__read_text') else inp.get('path')
        if not raw:
            violations.append({'tool':call['name'],'reason':'unbounded/default search path'});continue
        p=Path(raw).resolve()
        if not any(p==a or (a.is_dir() and p.is_relative_to(a)) for a in allowed):
            violations.append({'tool':call['name'],'path':str(p)})
    return violations


def audit_scoped_reads(receipt,allowed,run):
    """A denied MCP request is recorded separately from an actual outside read."""
    denied=set()
    for line in (Path(run)/'transcript.jsonl').read_text('utf-8').splitlines():
        event=json.loads(line)
        for item in message_content(event):
            if isinstance(item,dict) and item.get('type')=='tool_result' and item.get('is_error') is True and item.get('content')=='Error executing tool read_text: File is outside the configured evidence list':
                denied.add(item['tool_use_id'])
    blocked=[]
    for call in receipt['tool_calls']:
        violations=check_read_paths({'tool_calls':[call]},allowed)
        if not violations:continue
        if call['name']=='mcp__learning__read_text' and call['id'] in denied:blocked.extend(violations)
        else:raise ValueError('Successful or unconfirmed outside read: '+str(violations))
    return {'successful_outside_reads':0,'denied_attempts':blocked}


def readback(work, group, questions_path, attempt=1):
    cfg=learning.read_json(work/'config.json')
    spec=learning.read_json(questions_path)
    folder=work/group
    before=learning.inventory(folder,True)
    if not before:raise ValueError('No Wiki pages')
    knowledge_files=[name for name in before if Path(name).name not in ('learning-tasks.md','reuse-ledger.md','comparison-notes.md')]
    prompt=f'''你在全新 Claude Code 会话中做 Wiki-only 问答验证。仅可读取 {folder} 下的 Markdown。
实际知识正文清单：{json.dumps(knowledge_files,ensure_ascii=False)}。只读清单里的文件；禁止读取 learning-tasks/reuse-ledger 等过程记录。不要猜测未存在的页面名。一次缺失结果即停止尝试该路径。
不可读取源码、手册原件、其他组、模型运行记录、旧核验报告或评分材料。不要凭模型常识补全。
先实际读取所有知识正文，再回答以下固定问题。
每题必须给文档路径和实际行号；正文不能支持的部分明确未知。文档相互矛盾时保留两种说法及出处，不用自己的源码知识纠正。
输出严格 JSON，格式 {{"answers":[{{"id":"Q01","answer":"中文回答","citations":[{{"file":"相对于给定目录的路径.md","start_line":1,"end_line":10}}],"gaps":["正文没有说明的内容"]}}]}}。
全部 {len(spec['questions'])} 题每题都保留，无依据时 answer 明确未回答且 citations 空。每题回答以必要的 120–220 中文字为宜。只读工具，最后返回 JSON，不写文件。
问题：{json.dumps(spec['questions'],ensure_ascii=False)}
'''
    suffix='' if attempt==1 else f'-{attempt:02d}'
    label='readback-'+group+suffix
    previous=work/('readback-'+group+'.json')
    if previous.exists():
        if attempt==1:raise ValueError('Readback already exists; use a new attempt and preserve history')
        archive=work/'history'/('readback-'+group+'-before'+suffix+'.json')
        archive.parent.mkdir(exist_ok=True)
        if archive.exists():raise ValueError('Attempt history already exists')
        archive.write_bytes(previous.read_bytes())
    receipt=learning.execute(cfg,work,label,prompt,search_scopes={'wiki':{
        'root':str(folder),'files':[str(folder/name) for name in knowledge_files]}})
    accept_readback(work,group,questions_path,label,before)


def accept_readback(work,group,questions_path,label,before=None):
    """Validate a successful retained response without regenerating its content."""
    run=learning.safe_child(work/'runs',label)
    if not label.startswith('readback-'+group):raise ValueError('Run does not match group')
    learning.verify_inputs(work)
    folder=work/group;spec=learning.read_json(questions_path)
    current=learning.inventory(folder,True)
    if group=='D-consistent':
        from codewiki_consistency import assert_gate
        assert_gate(work)
    elif group!='A-original':
        stage='enhanced' if group=='B-enhanced' else 'specialist'
        expected=learning.read_json(work/'state.json')['stages'][stage]['pages']
        if current!=expected:raise ValueError('Frozen Wiki changed before acceptance')
    before=before or current
    knowledge_files=[name for name in before if Path(name).name not in ('learning-tasks.md','reuse-ledger.md','comparison-notes.md')]
    receipt=learning.read_json(run/'receipt.json')
    if receipt['exit_code'] or receipt.get('timed_out') or receipt.get('is_error') or receipt.get('subtype')!='success':
        raise ValueError('Cannot accept unsuccessful readback')
    violations=check_read_paths(receipt,[folder/name for name in knowledge_files])
    if violations:
        learning.write_json(work/'runs'/label/'access-violations.json',violations)
        raise ValueError('Wiki-only boundary breached; cannot count this readback')
    if learning.read_json(work/'config.json').get('scoped_read'):
        from codewiki_consistency import require_read_pages
        require_read_pages(run,[folder/name for name in knowledge_files])
    value=parse_run_json(work/'runs'/label)
    repair_path=run/'citation-repair.json'
    if repair_path.exists():
        repair=learning.read_json(repair_path)
        if learning.sha(run/'result.txt')!=repair['original_result_sha256']:raise ValueError('Original answer changed after citation repair')
        repair_run=learning.safe_child(work/'runs',repair['receipt_run'])
        receipt_fix=learning.read_json(repair_run/'receipt.json')
        if receipt_fix.get('subtype')!='success' or receipt_fix.get('is_error'):raise ValueError('No successful citation repair receipt')
        if parse_run_json(repair_run)['fixes']!=repair['fixes']:raise ValueError('Citation repair differs from actual Claude response')
        audit_scoped_reads(receipt_fix,[folder/name for name in knowledge_files],repair_run)
        from codewiki_consistency import validate_refs
        for fixed_row in repair['fixes']:
            validate_refs([{'root':'wiki',**r} for r in fixed_row['citations']],learning.read_json(work/'config.json'),folder,repair_run)
        fixed={row['id']:row['citations'] for row in repair['fixes']}
        for row in value['answers']:
            if row['id'] in fixed:row['citations']=fixed[row['id']]
        value['citation_repair_receipt']=repair['receipt_run']
    validate_rows(value['answers'],spec['questions'])
    for row in value['answers']:
        for citation in row['citations']:
            if citation['file'] not in knowledge_files:raise ValueError('Citation is not knowledge prose')
            target=learning.safe_child(folder,citation['file'])
            if target.suffix!='.md' or not target.is_file():raise ValueError('Invalid Wiki citation')
            count=len(target.read_text(encoding='utf-8').splitlines())
            if not 1<=citation['start_line']<=citation['end_line']<=count:
                raise ValueError('Invalid citation line range: '+row['id'])
    if learning.inventory(folder,True)!=before:raise ValueError('Wiki modified during readback')
    value.update(group=group,pages=before,questions_sha256=learning.sha(questions_path),
        execution='claude_code',source_access=False,runtime_validation='not_run',receipt_run=label)
    learning.write_json(work/('readback-'+group+'.json'),value)
    print(json.dumps({'group':group,'answers':len(value['answers']),'access_audit':'passed'}))


def repair_readback_citations(work,group,label,attempt=1):
    """A separate Claude session repairs invalid locations only; answers are immutable."""
    from codewiki_consistency import validate_refs
    cfg=learning.read_json(work/'config.json');cfg['scoped_read']=True
    run=learning.safe_child(work/'runs',label);folder=work/group
    value=parse_run_json(run);pages=[folder/name for name in learning.inventory(folder,True)
        if Path(name).name not in ('learning-tasks.md','reuse-ledger.md','comparison-notes.md')]
    invalid=[]
    for row in value['answers']:
        for ref in row['citations']:
            path=learning.safe_child(folder,ref['file'])
            if path not in pages or not 1<=ref['start_line']<=ref['end_line']<=len(path.read_text('utf-8').splitlines()):
                invalid.append(row);break
    if not invalid:raise ValueError('No invalid citations to repair')
    repair_label=label+'-citation-repair'+('' if attempt==1 else f'-{attempt:02d}');repair_run=work/'runs'/repair_label
    prompt=f'''只修复以下已生成答案的引用定位，不重新作答或改变判断。只能阅读 {folder} 的知识正文，不能读源码或其它组。
实际文件清单 {json.dumps([str(p) for p in pages],ensure_ascii=False)}。
这些行号超出文件范围；可能误用了文章提到的源码行号。请实际读 Wiki 的行号，找到支持答案的位置。原文无法支持则引用留空，不虚造。
原答案（保持原样，不输出改写）：{json.dumps(invalid,ensure_ascii=False)}。
返回严格 JSON {{"fixes":[{{"id":"H01","citations":[{{"file":"driver.md","start_line":1,"end_line":5}}]}}]}}。只输出给定ID的定位。
每个输出引用都必须在本轮用 mcp__learning__read_text 读到完整引用行段；search_text 命中不能代替阅读，不引用本轮未打开的页面。
'''
    receipt=learning.read_json(repair_run/'receipt.json') if (repair_run/'receipt.json').exists() else learning.execute(cfg,work,repair_label,prompt,search_scopes={'wiki':{'root':str(folder),'files':[str(p) for p in pages]}})
    if receipt['subtype']!='success' or receipt.get('is_error'):raise ValueError('Citation repair failed')
    audit_scoped_reads(receipt,pages,repair_run);fixed=parse_run_json(repair_run)
    if len(fixed['fixes'])!=len(invalid) or {x['id'] for x in fixed['fixes']}!={x['id'] for x in invalid}:raise ValueError('Citation-only repair changed question set')
    for row in fixed['fixes']:validate_refs([{'root':'wiki',**r} for r in row['citations']],cfg,folder,repair_run)
    fixed.update(original_result_sha256=learning.sha(run/'result.txt'),receipt_run=repair_label,
        answers_unchanged=True,reason='invalid Wiki line references only; no semantic resampling')
    learning.write_json(run/'citation-repair.json',fixed)
    return fixed


def judge(work, questions_path,reuse=False):
    cfg=learning.read_json(work/'config.json');spec=learning.read_json(questions_path)
    mapping={'S1':'C-specialist','S2':'A-original','S3':'B-enhanced'}
    # Order is masked, but the language/content may reveal the provenance. No blind-review claim.
    packet={'questions':spec,'sets':{key:learning.read_json(work/('readback-'+group+'.json'))['answers']
                                 for key,group in mapping.items()}}
    if reuse:
        if learning.read_json(work/'judge-packet.json')!=packet:raise ValueError('Judge inputs changed')
    else:
        learning.write_json(work/'judge-packet.json',packet)
        learning.write_json(work/'judge-mapping.json',mapping)
    prompt=f'''你是新的 Claude Code 审阅会话，实际读源码核对三组 Wiki-only 回答，不评价文章长短。
先读 {work/'judge-packet.json'}，其 S1/S2/S3 顺序不表示优劣；不得读取 judge-mapping、生成提示、旧评测或其他运行日志。
源码核心 {cfg['source']}、外部上下文 {cfg['context']}；版本 {cfg['revision']}；手册 {cfg['manual']}，读取 manifest 确认版本边界。
实际 Read/Grep 实现来确定行为，源码注释不是行为证明。相等比较、小输入、编译宏、异常路径、外部绑定、现网观测要逐一检查。不要为了填满评分而猜测未读实现。
先按符号用 Grep 定位定义，再 Read 相应范围；判断“定义未提供”前必须检索整个给定材料范围，不凭猜测的行号确定缺失。
对每组每题输出 accuracy：supported（回答中实质性断言有材料支持且关键限制正确）、incorrect（有明确错误）、unsupported（未证实的实质性断言）、missing（没有实质性回答）。存在明确错误优先 incorrect。
depth 0–3：0未回答，1概念/结论，2机制和条件，3机制/条件/关键边界或反例充分。有效深度只在 accuracy=supported 时记该分；其他类别计零。正确承认未知可以保留为 supported，但不能当完整解答拿满分。
为每条给 reason、主要正确/错误点，以及实际读过的 evidence 引用：root=source/context/manual，file=相对路径，start_line/end_line；不可虚构行号。
额外记录文稿回答中的矛盾或危险诊断建议；固定问题样本不代表所有文章准确率。纯源码审查不运行数据库。
返回严格 JSON：{{"reviews":[{{"id":"Q01","set":"S1","accuracy":"supported","depth":2,"reason":"...","evidence":[{{"root":"source","file":"src/...","start_line":1,"end_line":9}}]}}],"limitations":["..."],"critical_findings":["..."]}}。
总共 24×3=72 条，不能遗漏。只使用 Read/Grep/Glob；最后返回 JSON，不写文件。
'''
    receipt=learning.read_json(work/'runs/source-review/receipt.json') if reuse else learning.execute(cfg,work,'source-review',prompt)
    if receipt['exit_code'] or receipt.get('is_error') or receipt.get('subtype')!='success':raise ValueError('Incomplete source review')
    allowed=[work/'judge-packet.json',Path(cfg['source']),Path(cfg['context']),Path(cfg['manual'])]
    access=audit_access_with_missing_reads(receipt,allowed,work/'runs/source-review')
    value=parse_run_json(work/'runs/source-review')
    for key in mapping:
        validate_rows([x for x in value['reviews'] if x['set']==key],spec['questions'])
    for row in value['reviews']:
        if row['set'] not in mapping or row['accuracy'] not in spec['accuracy_labels'] or type(row['depth']) is not int or not 0<=row['depth']<=3:
            raise ValueError('Invalid score')
        if row['accuracy']=='supported' and not row['evidence']:
            raise ValueError('Supported answer needs material evidence')
        for ref in row['evidence']:
            if ref['root'] not in ('source','context','manual'):raise ValueError('Invalid evidence root')
            p=learning.safe_child(cfg[ref['root']],ref['file'])
            count=len(p.read_text(encoding='utf-8',errors='replace').splitlines())
            if not 1<=ref['start_line']<=ref['end_line']<=count:raise ValueError('Invalid evidence line range')
    value.update(mode='fresh_session_same_model_source_review',runtime_validation='not_run',access_audit=access)
    learning.write_json(work/'source-review.json',value)
    state=learning.read_json(work/'state.json')
    state.setdefault('evaluations',{})['question_review']={'result':'source-review.json',
        'scope':'fixed_question_answers_only','rows':len(value['reviews']),
        'release_approved':False,'runtime_validation':'not_run'}
    learning.write_json(work/'state.json',state)
    print(json.dumps({'reviewed':len(value['reviews']),'access_audit':'passed'}))


def audit_claims(work):
    cfg=learning.read_json(work/'config.json')
    groups=['A-original','B-enhanced','C-specialist']
    topics=['子代等值替换的比较条件','ERX 平均边数在最小输入规模的适用性',
            '规划总耗时与候选数量、单次估价工作量的关系','阈值所计项目与 SQL 基表数量的关系',
            '正常清理与 ERROR 后状态/内存恢复的区别','相同 seed 的复现前提与随机数实现绑定',
            '断言宏启用/禁用的语义及所检查不变量','计划估计代价与实际耗时/全局最优的区别']
    prompt=f'''你用 Claude Code 做原始 Wiki 的定向断言审计。问答模型可能会自行化解文稿矛盾，所以需要直接审原文。
仅可读取三个目录 {json.dumps([str(work/g) for g in groups],ensure_ascii=False)} 下的 Markdown，以及源码 {cfg['source']}、上下文 {cfg['context']}。
仅审知识正文，禁止读取 learning-tasks.md/reuse-ledger.md 等过程记录，不能把记录里引用的历史错误当成当前正文的断言。
不要读取其他评测、旧报告、生成提示或回读答案。先定位每个主题的相关原文，再读源码确认，不能只看摘要。
源码定位先用 Grep 搜索符号，再 Read；未在一个窗口读到不能判为实现不存在。
审计主题：{json.dumps(topics,ensure_ascii=False)}。每个组每主题一条，共 24 条。
输出严格 JSON {{"checks":[{{"group":"A-original","topic":"上述主题原文","status":"supported/incorrect/unsupported/mixed/missing","quote":"实际原文关键句，保留有问题的断言，不替它修正","page":"相对路径.md","start_line":1,"end_line":3,"finding":"判定和原因","source_refs":[{{"root":"source/context","file":"src/...","start_line":1,"end_line":5}}]}}],"limits":["..."]}}。
mixed 表示同组多处陈述矛盾；missing 时 quote/page 可为空且行号为0。其他情况下 page/行号必须真实。
有依据的局部机制不能支撑无条件性能承诺或异常恢复承诺。是针对这些主题的定向审计，不是全文所有断言准确率。只读工具，不执行数据库。
'''
    scopes={k:{'root':cfg[k]} for k in ('source','context')}
    for group in groups:
        scopes[group]={'root':str(work/group),'files':[str(p) for p in (work/group).rglob('*.md')
            if p.name not in ('learning-tasks.md','reuse-ledger.md')]}
    receipt=learning.execute(cfg,work,'claim-audit',prompt,search_scopes=scopes)
    violations=check_read_paths(receipt,[*(work/g for g in groups),Path(cfg['source']),Path(cfg['context'])])
    if violations:
        learning.write_json(work/'runs/claim-audit/access-violations.json',violations)
        raise ValueError('Claim audit access boundary breached')
    value=parse_run_json(work/'runs/claim-audit')
    seen=set()
    for row in value['checks']:
        key=(row['group'],row['topic'])
        if key in seen or row['group'] not in groups or row['topic'] not in topics:raise ValueError('Invalid/duplicate claim audit row')
        seen.add(key)
        if row['status'] not in ('supported','incorrect','unsupported','mixed','missing'):raise ValueError('Invalid claim audit status')
        if row['status']!='missing':
            p=learning.safe_child(work/row['group'],row['page'])
            lines=p.read_text(encoding='utf-8').splitlines()
            if not 1<=row['start_line']<=row['end_line']<=len(lines):raise ValueError('Invalid raw Wiki citation')
        for ref in row['source_refs']:
            if ref['root'] not in ('source','context'):raise ValueError('Invalid source root')
            p=learning.safe_child(cfg[ref['root']],ref['file'])
            count=len(p.read_text(encoding='utf-8',errors='replace').splitlines())
            if not 1<=ref['start_line']<=ref['end_line']<=count:raise ValueError('Invalid source lines')
    if len(seen)!=len(groups)*len(topics):raise ValueError('Missing claim audit rows')
    value['sampling']='targeted_known-risk_topics; not exhaustive or random'
    learning.write_json(work/'claim-audit.json',value)
    print(json.dumps({'claim_checks':len(seen),'access_audit':'passed'}))


def audit_access_with_missing_reads(receipt,allowed,run):
    """Only a recorded, exact file-not-found error can exempt an attempted Read.

    Failed attempts remain in the audit. This is not used to loosen Wiki-only
    readback checks; an out-of-scope successful or ambiguous read still fails.
    """
    missing=set()
    for line in (run/'transcript.jsonl').read_text('utf-8').splitlines():
        event=json.loads(line)
        for item in message_content(event):
            if isinstance(item,dict) and item.get('type')=='tool_result' and item.get('is_error') is True:
                text=item.get('content','')
                if isinstance(text,str) and re.fullmatch(r'File does not exist\.(?: Note: your current working directory is [^\r\n]+\.)?',text):
                    missing.add(item.get('tool_use_id'))
    failed=[]
    for call in receipt['tool_calls']:
        violations=check_read_paths({'tool_calls':[call]},allowed)
        if not violations:continue
        if call['name']=='Read' and call['id'] in missing:failed.extend(violations)
        else:raise ValueError('Audit read outside assigned evidence')
    return {'successful_out_of_scope_reads':0,'confirmed_file_not_found_attempts':failed}


def audit_diagnosis(work,reuse=False):
    """Review every candidate recommendation separately from handbook Q&A."""
    cfg=learning.read_json(work/'config.json');folder=work/'C-specialist'
    knowledge=[p for p in folder.rglob('*.md') if p.name not in ('learning-tasks.md','reuse-ledger.md')]
    prompt=f'''用全新 Claude Code 会话审查 {folder/'diagnosis.md'} 的全部九条 RC 规则候选和相应场景卡，实际读源码，不改文稿。
可读 C 组知识正文 {json.dumps([str(p) for p in knowledge],ensure_ascii=False)}、源码 {cfg['source']}、上下文 {cfg['context']}、手册 {cfg['manual']}。不可读其他组、评测答案或过程记录。
逐条检查：触发条件能否被观察；是否从必要条件错误推出充分条件；检测位置能否推出唯一上游生产者；参数建议对基准值究竟增大还是减小开销；阴性对照能否排除其他路径；阈值究竟是哪层 joinlist；随机数和构建条件是否已闭合。不能因为标了候选/未知就放过明确错误。
每条回查相关实现，并给最小反例或必须增加的前提。特别区分“应修订规则文字”和“需运行验证”，源码明确反证的陈述不能只写待实验。
严格 JSON：{{"rules":[{{"id":"RC-1","status":"supported/incorrect/unsupported/mixed","finding":"判定及相关场景问题","correction":"建议如何收窄（不实际修改）","evidence":[{{"root":"source/context/manual","file":"相对路径","start_line":1,"end_line":5}}]}}],"release_recommendation":"...","limitations":["..."]}}。
九条完整覆盖。最后返回 JSON；source_only，不执行 SQL。'''
    scopes={k:{'root':cfg[k]} for k in ('source','context','manual')}
    scopes['wiki']={'root':str(folder),'files':[str(p) for p in knowledge]}
    run=work/'runs/diagnosis-audit'
    receipt=learning.read_json(run/'receipt.json') if reuse else learning.execute(cfg,work,'diagnosis-audit',prompt,search_scopes=scopes)
    if receipt['exit_code'] or receipt.get('is_error') or receipt.get('subtype')!='success':raise ValueError('Incomplete diagnosis audit')
    learning.verify_inputs(work)
    if learning.inventory(folder,True)!=learning.read_json(work/'state.json')['stages']['specialist']['pages']:
        raise ValueError('C changed after generation freeze')
    access=audit_access_with_missing_reads(receipt,[*knowledge,*(Path(cfg[k]) for k in ('source','context','manual'))],run)
    value=parse_run_json(work/'runs/diagnosis-audit')
    validate_rows(value['rules'],[{'id':f'RC-{i}'} for i in range(1,10)])
    for row in value['rules']:
        if row['status'] not in ('supported','incorrect','unsupported','mixed'):raise ValueError('Invalid rule status')
        for ref in row['evidence']:
            if ref['root'] not in ('source','context','manual'):raise ValueError('Invalid evidence root')
            p=learning.safe_child(cfg[ref['root']],ref['file'])
            if not 1<=ref['start_line']<=ref['end_line']<=len(p.read_text('utf-8',errors='replace').splitlines()):
                raise ValueError('Invalid evidence lines')
    value.update(runtime_validation='not_run',release_approved=False,access_audit=access)
    learning.write_json(work/'diagnosis-audit.json',value)
    print(json.dumps({'rules':len(value['rules']),'release_approved':False}))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('readback','accept-readback','repair-citations','judge','accept-judge','audit-claims','audit-diagnosis','accept-diagnosis'))
    p.add_argument('--work',required=True,type=Path);p.add_argument('--questions',type=Path)
    p.add_argument('--group',choices=('A-original','B-enhanced','C-specialist','D-consistent'))
    p.add_argument('--attempt',type=int,default=1)
    p.add_argument('--run',help='Existing successful readback run to validate')
    a=p.parse_args()
    if a.action=='audit-claims':return audit_claims(a.work.resolve())
    if a.action=='audit-diagnosis':return audit_diagnosis(a.work.resolve())
    if a.action=='accept-diagnosis':return audit_diagnosis(a.work.resolve(),True)
    if a.action=='repair-citations':
        if not a.group or not a.run:p.error('--group and --run required')
        return repair_readback_citations(a.work.resolve(),a.group,a.run,a.attempt)
    if not a.questions:p.error('--questions required')
    if a.action=='accept-readback':
        if not a.group or not a.run:p.error('--group and --run required')
        return accept_readback(a.work.resolve(),a.group,a.questions.resolve(),a.run)
    if a.action=='readback':
        if not a.group:p.error('--group required')
        readback(a.work.resolve(),a.group,a.questions.resolve(),a.attempt)
    else:judge(a.work.resolve(),a.questions.resolve(),a.action=='accept-judge')


if __name__=='__main__':main()
