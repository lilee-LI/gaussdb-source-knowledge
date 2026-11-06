"""Bounded native CodeWiki -> specialist integration, executed by Claude Code.

This adapter manages immutable inputs and real process receipts. It does not
certify semantics, configure credentials, or promote a draft to customer release.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

PROJECT = Path(__file__).resolve().parents[1]
RUNNER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
MCP_TOOLS = ('analyze_repo', 'read_code_components', 'write_doc_file', 'edit_doc_file',
             'save_module_tree', 'get_processing_order', 'get_prompt', 'close_session', 'get_module_tree')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(root, markdown_only=False):
    root = Path(root)
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and '.codewiki' not in p.parts and '__pycache__' not in p.parts
            and (not markdown_only or p.suffix == '.md')}


def safe_child(root, name):
    target = (Path(root) / name).resolve()
    if not target.is_relative_to(Path(root).resolve()) or target == Path(root).resolve():
        raise ValueError('Artifact path escapes output directory')
    return target


def prepare(config_file):
    cfg = read_json(config_file)
    cfg.setdefault('scoped_read', True)
    work = Path(cfg['work']).resolve()
    if work.exists():
        raise ValueError('Use a new work directory; previous trials are immutable')
    for key in ('source', 'context', 'manual', 'baseline', 'vendor', 'mcp_python', 'claude', 'scope_file', 'module_tree'):
        if not Path(cfg[key]).exists():
            raise ValueError('Missing input: ' + key)
    for key in ('source','context','manual','baseline','vendor'):
        original=Path(cfg[key]).resolve()
        if work.is_relative_to(original) or original.is_relative_to(work):
            raise ValueError('Work directory must be separate from inputs: '+key)
    if not list(Path(cfg['baseline']).rglob('*.md')):
        raise ValueError('Baseline has no Markdown documents')
    work.mkdir(parents=True)
    write_json(work / 'config.json', cfg)
    (work / 'runs').mkdir()
    for group in ('A-original', 'B-enhanced', 'C-specialist'):
        (work / group).mkdir()
    for p in Path(cfg['baseline']).rglob('*.md'):
        if p.name not in cfg.get('exclude_baseline_pages', []):
            dest = work / 'A-original' / p.relative_to(cfg['baseline'])
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dest)
    inputs = {key: {'root': cfg[key], 'files': inventory(cfg[key], key == 'baseline')}
              for key in ('source', 'context', 'manual', 'baseline')}
    inputs['A-original'] = {'root': str(work / 'A-original'), 'files': inventory(work / 'A-original')}
    write_json(work / 'input-lock.json', inputs)
    shutil.copyfile(PROJECT / 'integrations/codewiki/enhanced-learning.md', work / 'enhanced-learning.md')
    write_json(work / 'method-lock.json', {'enhanced-learning.md': sha(work / 'enhanced-learning.md'),
        'driver': sha(__file__), 'codewiki_cpp': sha(Path(cfg['vendor']) / 'codewiki/src/be/dependency_analyzer/analyzers/cpp.py')})
    write_json(work / 'state.json', {'schema': 'codewiki-learning/v1', 'source_revision': cfg['revision'],
        'status': 'prepared', 'stages': {}, 'runtime_validation': 'not_run', 'release_status': 'draft'})
    print(json.dumps({'work': str(work), 'baseline_pages': len(inventory(work / 'A-original'))}, ensure_ascii=False))


def verify_inputs(work):
    failures = []
    for name, item in read_json(work / 'input-lock.json').items():
        current = inventory(item['root'], name == 'baseline')
        if current != item['files']:
            failures.append(name)
    if failures:
        raise ValueError('Frozen input mutation: ' + ', '.join(failures))


def mcp_config(cfg):
    args = ['-X', 'utf8', str(PROJECT / 'scripts/codewiki_learning_mcp.py'),
            '--vendor', cfg['vendor'], '--cache', cfg['token_cache']]
    if cfg.get('parser_site'):
        args += ['--parser-site', cfg['parser_site']]
    return {'mcpServers': {'codewiki': {'command': cfg['mcp_python'], 'args': args}}}


def generation_prompt(cfg, work, stage):
    out = work / ('B-enhanced' if stage == 'enhanced' else 'C-specialist')
    subject=cfg.get('subject','本批选定模块')
    def leaf_count(tree):
        return sum(leaf_count(node['children']) if node.get('children') else 1 for node in tree.values())
    count=leaf_count(read_json(cfg['module_tree']))
    common = f'''你通过 Claude Code 执行有界源码研究，真实使用 CodeWiki stdio MCP 工具。
源码版本 {cfg['revision']}。核心源码 {cfg['source']}；同版本外部上下文 {cfg['context']}。
输出目录 {out}。先读 {cfg['scope_file']}，其中列明材料范围及版本。数据库执行 not_run。
只读以上源码、指定方法和本阶段文章；不读 A 组、评测问题、旧核验报告、其他组答案或运行日志。
不能调用 shell、网络、数据库、子代理。源码只读。只通过 CodeWiki write_doc_file/edit_doc_file 写本阶段 Markdown。
阅读官方 Skill {cfg['vendor']}/skills/codewiki-wiki-generator/SKILL.md 并执行适用的 MCP 操作。
analyze_repo(repo_path=核心源码, output_dir=输出目录)，读取索引。复用已核对模块树 {cfg['module_tree']}，save_module_tree 后读取处理顺序。
核心组件读取用 read_code_components 并实际 Read 返回的文件；可读完整源文件避免割裂上下文。
外部上下文通过 Read/Grep 定位，不能宣称已学习整个外部子系统。禁止读取未列出的其他目录。
生成后实际回读本阶段文章，保留未知并 close_session。远程 Mermaid 校验禁用不等于语法错误。
本轮是原生生成接收试点，不调用旧 repository/study 命令伪造已审状态。发布状态保持 draft。
中文写作，不复制大段源码，重点解释行为、条件和边界。页面中的源码引用用原仓库相对路径和精确行号。
'''
    if stage == 'enhanced':
        return common + f'''
本阶段从源码新生成模块说明，不读取手册及专项 Skill，不参考旧文档内容。
先读 {work / 'enhanced-learning.md'}。每个叶模块调用 get_prompt(system_leaf)，把该文件的完整学习要求通过 variables.custom_instructions 传入。
以已给模块树为分组生成各模块 Markdown，最后 overview.md。遵循要求研究正常机制、参数、状态、异常、边界、反例和未解问题。篇幅以实际内容为准，不机械满足上游行数建议。
本批模块树有 {count} 个叶模块，所有叶模块都要说明；外部依赖可读上下文目录的必要范围。完成后报告实际写入页与局限。
'''
    skills = [PROJECT / p for p in cfg.get('specialist_skills',[
              'skills/source-guc-learning/SKILL.md','engine/source-error-learning/SKILL.md',
              'skills/source-memory-learning/SKILL.md','references/common/research-depth.md'])]
    return common + f'''
本阶段目录已复制 B 组生成稿。先读已有 overview/driver/fitness/population/erx/contracts 及相关页面，按问题复用已解释的机制。B 组未经过独立审阅，关键结论实际回查源码，不能自动接受。
阅读真实用户手册 {cfg['manual']} 下的 manifest.json 和手册正文。逐项区分文档声明、源码行为、版本不能对应的范围；两者矛盾时保留来源和条件。
加载以下专项 Skill/规则，实际阅读其中与本轮问题相关的方法资源：{json.dumps([str(p) for p in skills],ensure_ascii=False)}。
采用错误 Skill 时使用“补已有缺口”模式，仅限 {subject} 的相应检测点，不宣称全错误族研究完成。
主动深化：参数注册/消费与交互、局部错误/断言及上游合法性、评估内存与正常/异常清理、用户可观测与安全采集建议。兼容性、导入导出等未涉及的专题说明范围，不编造内容。
首先写 learning-tasks.md：从已有说明、手册和源码发现的具体学习问题、已有答案、要补的证据；随后逐项研究并更新完成/开放状态。
以已有页面为共同事实载体，改正发现的错误，不重写全部正确模块。新增最多四篇必要专题，修订 overview.md 链接到专题；通过链接复用算法主流程。
必须写 reuse-ledger.md，逐条说明复用哪些 B 组段落、核对了什么、改正了什么、新增了什么、仍缺什么。依据是真实正文和实际源码，不以页数证明提升。
写 diagnosis.md：提供可观察事实、必要前提、候选解释、证据缺失时的出口；只有机制支持的结论才给有条件建议。参数调整、错误消息、RSS 等都不能单独证明唯一根因。当前只编写诊断建议和规则候选，不冒充已发布可执行规则包。
发现错误时改正本组文章并记录，不修改 B 组。结束前回读主说明与专题，检查重复/矛盾/链接。
'''


def execute(cfg, work, label, prompt, use_mcp=False, search_scopes=None):
    run = work / 'runs' / label
    run.mkdir(exist_ok=False)
    (run / 'prompt.txt').write_text(prompt, encoding='utf-8')
    servers=mcp_config(cfg) if use_mcp else {'mcpServers': {}}
    # The unified controller can expose its frozen evidence/lease tools beside
    # CodeWiki. Existing configurations retain exactly their original tool set.
    for name, server in cfg.get('extra_mcp_servers', {}).items():
        if name in servers['mcpServers']:
            raise ValueError('Duplicate extra MCP server: '+name)
        servers['mcpServers'][name] = server
    if search_scopes is None:
        search_scopes={k:{'root':cfg[k]} for k in ('source','context')}
        if label!='enhanced':search_scopes['manual']={'root':cfg['manual']}
        if cfg.get('scoped_read') and (use_mcp or cfg.get('frozen_methods_only')):
            group='B-enhanced' if label=='enhanced' else 'C-specialist'
            search_scopes['wiki']={'root':str(work/group)}
            if cfg.get('frozen_methods_only'):
                search_scopes['baseline']={'root':cfg['baseline']}
            paths=[Path(cfg['vendor'])/'skills/codewiki-wiki-generator/SKILL.md',
                Path(cfg['scope_file']),Path(cfg['module_tree']),work/'enhanced-learning.md']
            if not cfg.get('frozen_methods_only'):
                paths += [PROJECT/p for p in cfg.get('specialist_skills',[
                    'skills/source-guc-learning/SKILL.md','engine/source-error-learning/SKILL.md',
                    'skills/source-memory-learning/SKILL.md','references/common/research-depth.md'])]
                paths += [p for base in (PROJECT/'references',PROJECT/'engine/source-error-learning/references') for p in base.rglob('*.md')]
            paths += [Path(p) for p in cfg.get('extra_method_paths', [])]
            # Group exact-file scopes by drive, including portable installations
            # whose model runtime and work directory are on different volumes.
            method_groups={}
            for path in paths:
                if path.exists():
                    method_groups.setdefault(path.resolve().drive or '/', []).append(path.resolve())
            for n,group in enumerate(method_groups.values()):
                common=Path(os.path.commonpath([str(p.parent) for p in group]))
                search_scopes['methods' if n==0 else 'methods_'+str(n)]={'root':str(common),'files':[str(p) for p in group]}
    write_json(run/'search-scopes.json',search_scopes)
    servers['mcpServers']['learning']={'command':cfg['mcp_python'],'args':['-X','utf8',
        str(PROJECT/'scripts/learning_search_mcp.py'),'--scopes',str(run/'search-scopes.json')]}
    write_json(run / 'mcp.json',servers)
    prompt+='\n本会话若没有内置 Grep/Glob，必须使用 mcp__learning__search_text 按字面符号检索，再 Read 返回的真实行号。它是本地只读工具，不能执行 shell 或改文件。\n'
    prompt+='可用检索 scope：'+', '.join(search_scopes)+'。省略 scope 会搜索上述全部范围；不支持正则表达式。\n'
    (run / 'prompt.txt').write_text(prompt,encoding='utf-8')
    env = os.environ.copy()
    if not env.get('ANTHROPIC_API_KEY') and env.get('ANTHROPIC_AUTH_TOKEN'):
        env['ANTHROPIC_API_KEY'] = env['ANTHROPIC_AUTH_TOKEN']
    secrets = [v for k,v in env.items() if ('TOKEN' in k or 'API_KEY' in k) and len(v)>=12]
    def redact(value):
        for secret in secrets:
            value = value.replace(secret, '[REDACTED]')
        return value
    builtins = [] if cfg.get('scoped_read') else ['Read']
    if cfg.get('scoped_read'):
        prompt+='\n内置 Read 已禁用。所有读取必须使用 mcp__learning__read_text(file_path,offset,limit)；只允许配置中的材料。绝对路径清单已给出，不猜目录。has_more=true 时继续按行读取。\n'
        (run/'prompt.txt').write_text(prompt,encoding='utf-8')
    allowed = builtins + ['mcp__learning__search_text'] + (['mcp__learning__read_text'] if cfg.get('scoped_read') else []) + ([f'mcp__codewiki__{n}' for n in MCP_TOOLS] if use_mcp else [])
    allowed += cfg.get('extra_mcp_tools', [])
    command = [cfg['claude'], '--bare', '-p', '--output-format', 'stream-json', '--verbose',
        '--tools', ','.join(builtins), '--allowedTools', ','.join(allowed), '--permission-mode', 'dontAsk',
        '--strict-mcp-config', '--mcp-config', str(run/'mcp.json'), '--no-session-persistence',
        '--max-budget-usd', str(cfg.get('max_budget_usd', 10))]
    if cfg.get('model'):
        command += ['--model', cfg['model']]
    for folder in {str(work), cfg['source'], cfg['context'], cfg['manual'], str(PROJECT), cfg['vendor']}:
        command += ['--add-dir', folder]
    write_json(run/'launch.json', {'execution':'claude_code', 'codewiki_mcp':use_mcp,
        'requested_model':cfg.get('model','configured default'), 'source_revision':cfg['revision'],
        'credentials':'inherited; not persisted', 'allowed_tools':allowed,
        'is_os_sandbox':False, 'scoped_read':bool(cfg.get('scoped_read')), 'runtime_validation':'not_run', 'prompt_sha256':sha(run/'prompt.txt'),
        'runner_sha256':RUNNER_SHA256})
    start=time.monotonic()
    proc=subprocess.Popen(command,cwd=run,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace')
    def stderr():
        with (run/'stderr.log').open('w',encoding='utf-8') as handle:
            for line in proc.stderr:
                handle.write(redact(line))
    thread=threading.Thread(target=stderr,daemon=True);thread.start()
    timed_out=threading.Event()
    def stop():
        timed_out.set();proc.kill()
    timer=threading.Timer(cfg.get('timeout_seconds',1800),stop);timer.daemon=True;timer.start()
    proc.stdin.write(prompt);proc.stdin.close()
    final=None;calls=[];model=None
    with (run/'transcript.jsonl').open('w',encoding='utf-8') as log:
        for raw in proc.stdout:
            raw=redact(raw);log.write(raw);log.flush()
            try:event=json.loads(raw)
            except json.JSONDecodeError:continue
            if event.get('type')=='system' and event.get('subtype')=='init':
                model=event.get('model')
                print(json.dumps({'run':label,'model':model,'mcp':event.get('mcp_servers')},ensure_ascii=False),flush=True)
            if event.get('type')=='assistant':
                for item in event.get('message',{}).get('content',[]):
                    if item.get('type')=='tool_use':
                        calls.append({'name':item.get('name'),'id':item.get('id'),'input':item.get('input'),
                                      'elapsed_seconds':round(time.monotonic()-start,2)})
                        print(json.dumps({'run':label,'tool':item.get('name'),'elapsed':calls[-1]['elapsed_seconds']}),flush=True)
            if event.get('type')=='result':final=event
    code=proc.wait();timer.cancel();thread.join(timeout=5)
    receipt={'exit_code':code,'timed_out':timed_out.is_set(),'elapsed_seconds':round(time.monotonic()-start,3),
        'model':model,'usage':(final or {}).get('usage'),'modelUsage':(final or {}).get('modelUsage'),
        'total_cost_usd':(final or {}).get('total_cost_usd'),'permission_denials':(final or {}).get('permission_denials',[]),
        'subtype':(final or {}).get('subtype'),'is_error':(final or {}).get('is_error'),
        'tool_counts':dict(Counter(c['name'] for c in calls)), 'tool_calls':calls}
    write_json(run/'receipt.json',receipt)
    (run/'result.txt').write_text((final or {}).get('result',''),encoding='utf-8')
    verify_inputs(work)
    if code or timed_out.is_set() or not final or final.get('is_error') or final.get('subtype')!='success':
        raise RuntimeError('Claude execution did not complete successfully: '+label)
    return receipt


def run_stage(work, stage):
    cfg=read_json(work/'config.json');state=read_json(work/'state.json');verify_inputs(work)
    if stage in state['stages']:
        raise ValueError('Stage already frozen; create a new trial for revisions')
    if stage=='specialist':
        if 'enhanced' not in state['stages']:
            raise ValueError('Enhanced stage must complete before specialist reuse')
        if inventory(work/'B-enhanced',True)!=state['stages']['enhanced']['pages']:
            raise ValueError('Enhanced input changed after acceptance')
        for p in (work/'B-enhanced').rglob('*.md'):
            dest=work/'C-specialist'/p.relative_to(work/'B-enhanced')
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    execute(cfg,work,stage,generation_prompt(cfg,work,stage),True)
    accept_stage(work,stage)


def accept_stage(work,stage):
    """Receive completed native output, without fabricating a learning/review run."""
    cfg=read_json(work/'config.json');state=read_json(work/'state.json');verify_inputs(work)
    if stage in state['stages']:raise ValueError('Stage already frozen')
    receipt=read_json(work/'runs'/stage/'receipt.json')
    if receipt['exit_code'] or receipt.get('timed_out') or receipt.get('is_error') or receipt.get('subtype')!='success':
        raise ValueError('Cannot receive an incomplete/failed model execution')
    counts=receipt['tool_counts']
    # Specialist research may directly read source files; component navigation is
    # mandatory for the native first-generation stage, not a second whole read.
    required=('analyze_repo','read_code_components','close_session') if stage=='enhanced' else ('analyze_repo','close_session')
    if any(not counts.get('mcp__codewiki__'+n) for n in required):
        raise ValueError('Missing real CodeWiki execution tools')
    if stage=='enhanced' and not counts.get('mcp__codewiki__get_prompt'):
        raise ValueError('Enhanced stage never requested native prompts')
    if stage=='enhanced':
        prompts=[c['input'].get('variables',{}) for c in receipt['tool_calls']
                 if c['name']=='mcp__codewiki__get_prompt' and c['input'].get('prompt_type')=='system_leaf']
        enhanced_modules={v.get('module_name') for v in prompts if v.get('custom_instructions')}
        def leaves(tree):
            result=set()
            for name,node in tree.items():
                if node.get('children'):result.update(leaves(node['children']))
                else:result.add(name)
            return result
        if not leaves(read_json(cfg['module_tree']))<=enhanced_modules:
            raise ValueError('Enhanced instructions did not reach all native leaf prompts')
    folder=work/('B-enhanced' if stage=='enhanced' else 'C-specialist')
    pages=inventory(folder,True)
    if 'overview.md' not in pages or len(pages)<2:
        raise ValueError('Missing handbook pages')
    if stage=='specialist':
        if inventory(work/'B-enhanced',True)!=state['stages']['enhanced']['pages']:
            raise ValueError('Specialist changed frozen B input')
        if not {'learning-tasks.md','reuse-ledger.md','diagnosis.md'}<=set(pages):
            raise ValueError('Missing specialist integration records')
    state['stages'][stage]={'pages':pages,'receipt':str(work/'runs'/stage/'receipt.json'),
                           'status':'generated_draft','semantic_review':'pending'}
    state['status']='specialist_generated' if stage=='specialist' else 'enhanced_generated'
    write_json(work/'state.json',state)
    print(json.dumps({'stage':stage,'pages':len(pages),'status':'generated_draft'},ensure_ascii=False))


def refine_specialist(work,attempt=1):
    """Apply the referenced specialty methods before freezing C for comparison."""
    cfg=read_json(work/'config.json');state=read_json(work/'state.json');verify_inputs(work)
    if 'specialist' not in state['stages']:
        raise ValueError('Specialist draft must exist first')
    if (work/'readback-C-specialist.json').exists():
        raise ValueError('C has already been evaluated; create a new comparison instead of rewriting it')
    current=inventory(work/'C-specialist',True)
    if current!=state['stages']['specialist']['pages']:
        raise ValueError('Specialist pages changed outside tracked workflow')
    suffix='' if attempt==1 else f'-{attempt:02d}'
    history=work/('history/C-before-method-review'+suffix)
    history.mkdir(parents=True,exist_ok=False)
    for relative in current:
        target=safe_child(history,relative);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(work/'C-specialist'/relative,target)
    resources=cfg.get('specialist_resources',[
        'references/common/learning.md','references/common/research-depth.md',
        'references/domains/memory.md','references/source-only/memory.md',
        'references/source-only-learning.md','references/source-manual-learning-playbook.md',
        'engine/source-error-learning/references/error-causal-learning.md',
        'engine/source-error-learning/references/field-scenario-playbooks.md',
        'references/error-applicability.md'])
    files=[str(PROJECT/r) for r in resources]
    prompt=generation_prompt(cfg,work,'specialist')+f'''
这是专项阶段的第二个新会话：C 目录已经有前轮候选稿，请先读现有 learning-tasks.md 和 reuse-ledger.md，以本轮收口修订为目标，避免重写正确说明。
专项 Skill 引用的以下方法是本轮必须实际读取的资源，不可只读 Skill 入口摘要：{json.dumps(files,ensure_ascii=False)}。
按这些方法检查本轮已有研究是否支持其因果、配置、生效、状态写者、异常清理和建议；补读缺少的源码范围。发现不支持的陈述应修订或降级，同时更新任务和复用记录。
对现有任务清单中“定义不在上下文/未提供/不存在/没有消费者”等断言，必须先用 Grep 在给定 source/context 全范围按符号检索，再按实际命中位置 Read。不能把猜行号没读到当作文件或实现缺失。找到后读完整相关定义；未能闭合继续保留具体未知。
只能在已给 source/context 中定位源码；未提供的构建或外部路径明确待补，不凭常识补全。引用行号必须对应实际 Read 结果。
使用 read_code_components 获取本轮需要复核的核心组件，实际读返回文件。通过 write_doc_file/edit_doc_file 修订 C 页面，结束前 close_session。
无需输出满篇文章；没有支持依据的结论留在明确的待研究项。不要读取评测题、评测答案、旧审计或 A 组。此轮仍是研究方法收口，不是正式发布批准。
'''
    label='specialist-method-review'+suffix
    receipt=execute(cfg,work,label,prompt,True)
    read_paths={str(Path(c['input']['file_path']).resolve()) for c in receipt['tool_calls']
                if c['name'] in ('Read','mcp__learning__read_text') and c['input'].get('file_path')}
    if not set(files)<=read_paths:raise ValueError('Required specialist references were not all read')
    if not (receipt['tool_counts'].get('Grep') or receipt['tool_counts'].get('mcp__learning__search_text')):
        raise ValueError('Missing symbol search for claimed source gaps')
    if not receipt['tool_counts'].get('mcp__codewiki__close_session'):raise ValueError('MCP session not closed')
    if inventory(work/'B-enhanced',True)!=state['stages']['enhanced']['pages']:
        raise ValueError('Specialist review mutated B')
    stage=state['stages']['specialist']
    stage['previous_pages']=current;stage['pages']=inventory(work/'C-specialist',True)
    stage['method_review_receipt']=str(work/'runs'/label/'receipt.json')
    stage['method_resources']={r:sha(PROJECT/r) for r in resources}
    state['status']='specialist_method_reviewed_draft'
    write_json(work/'state.json',state)
    print(json.dumps({'stage':'specialist-method-review','pages':len(stage['pages']),'status':'generated_draft'}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare');p.add_argument('--config',required=True,type=Path)
    p=sub.add_parser('run');p.add_argument('--work',required=True,type=Path);p.add_argument('--stage',choices=('enhanced','specialist'),required=True)
    p=sub.add_parser('pipeline');p.add_argument('--work',required=True,type=Path);p.add_argument('--max-consistency-rounds',type=int,default=2);p.add_argument('--seeds',type=Path)
    p=sub.add_parser('accept');p.add_argument('--work',required=True,type=Path);p.add_argument('--stage',choices=('enhanced','specialist'),required=True)
    p=sub.add_parser('check');p.add_argument('--work',required=True,type=Path)
    p=sub.add_parser('refine-specialist');p.add_argument('--work',required=True,type=Path);p.add_argument('--attempt',type=int,default=1)
    p=sub.add_parser('task');p.add_argument('--work',required=True,type=Path);p.add_argument('--name',required=True);p.add_argument('--prompt',required=True,type=Path)
    args=parser.parse_args()
    if args.action=='prepare':return prepare(args.config)
    work=args.work.resolve()
    if args.action=='pipeline':
        for stage in ('enhanced','specialist'):
            if stage not in read_json(work/'state.json')['stages']:run_stage(work,stage)
        if not read_json(work/'state.json')['stages']['specialist'].get('method_review_receipt'):
            refine_specialist(work)
        from codewiki_consistency import run_consistency
        result=run_consistency(work,args.max_consistency_rounds,args.seeds)
        if result['status']!='passed':raise SystemExit(2)
        evaluation=read_json(work/'state.json').get('evaluation',{}).get('status','not_run')
        print(json.dumps({'consistency':'passed','evaluation':evaluation,'customer_release_approved':False}))
        if evaluation=='requires_followup':raise SystemExit(2)
        return
    if args.action=='run':return run_stage(work,args.stage)
    if args.action=='accept':return accept_stage(work,args.stage)
    if args.action=='refine-specialist':return refine_specialist(work,args.attempt)
    if args.action=='check':verify_inputs(work);print('Frozen inputs unchanged');return
    safe_child(work/'runs',args.name)
    return execute(read_json(work/'config.json'),work,args.name,args.prompt.read_text(encoding='utf-8'))


if __name__=='__main__':
    main()
