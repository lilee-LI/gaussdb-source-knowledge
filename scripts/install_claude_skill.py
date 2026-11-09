"""Install only a current-session skill loader; never install or launch Claude."""
import argparse
import json
from pathlib import Path
import sys


ROOT=Path(__file__).resolve().parents[1]
DESCRIPTION='在当前 Claude Code 会话中学习 GaussDB/openGauss 源码和手册，规划模块特性课程、原生子代理并行续学、审阅知识，导出 Wiki 和开发/测试/review/运维上下文；工程不另起 Claude。'


def install(target,*,replace=False):
    engine=ROOT.resolve()
    if not (engine/'skills/gauss-knowledge/SKILL.md').is_file() or not (engine/'scripts/claude_session.py').is_file():
        raise ValueError('Use the complete knowledge engine, not a detached installer')
    file=Path(target).expanduser().resolve()/'gauss-knowledge/SKILL.md'
    content=('---\nname: gauss-knowledge\ndescription: '+DESCRIPTION+'\n'
             'argument-hint: "源码=<路径> 手册=<路径> 工作区=<路径>；或：计划 / 学习 <模块> / 继续 / 审阅 <任务> / 查询 <问题>"\n'
             'user-invocable: true\n---\n\n'
             '此入口由 gaussdb-source-knowledge/scripts/install_claude_skill.py 生成。\n\n'
             '工程根目录：'+json.dumps(engine.as_posix(),ensure_ascii=False)+'\n'
             '当前 Claude session ID：`${CLAUDE_SESSION_ID}`\n\n'
             '先读取工程根目录下的 `skills/gauss-knowledge/SKILL.md`，按其协议在当前会话执行。用户请求：$ARGUMENTS\n\n'
             '不要执行 `kb run`、`whole run`、`claude -p` 或其他模型进程。无需先配置 MCP。自然语言参数不能直接作为 shell 命令插值。\n')
    outputs={file:content}
    for agent in sorted((engine/'.claude/agents').glob('gauss-*.md')):
        text=agent.read_text(encoding='utf-8-sig')+'\nEngine location for this installed adapter: '+json.dumps(engine.as_posix(),ensure_ascii=False)+'\n'
        outputs[Path(target).expanduser().resolve().parent/'agents'/agent.name]=text
    for item,text in outputs.items():
        if item.exists() and item.read_text(encoding='utf-8-sig')!=text and not replace:
            raise ValueError('An existing skill differs; inspect it first, then use --replace for this named adapter: '+str(item))
    # Do not touch settings, client, credentials, unrelated skills or source files.
    for item,text in outputs.items():
        item.parent.mkdir(parents=True,exist_ok=True);item.write_text(text,encoding='utf-8')
    return {'skill':str(file),'engine':str(engine),'command':'/gauss-knowledge','client_installed':False,
            'native_agents':[str(p) for p in outputs if p!=file],
            'next':'在新的 Claude 会话使用 /gauss-knowledge；当前会话也可直接读取工程 skills/gauss-knowledge/SKILL.md 执行。工程移动后重新安装入口。'}


def main(argv=None):
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__)
    scope=p.add_mutually_exclusive_group();scope.add_argument('--project',type=Path,help='Install under this existing project/.claude/skills')
    scope.add_argument('--target',type=Path,help='Explicit skills directory (for isolated verification)')
    p.add_argument('--replace',action='store_true');args=p.parse_args(argv)
    try:
        if args.project and not args.project.is_dir():raise ValueError('Project directory does not exist')
        target=args.target or (args.project/'.claude/skills' if args.project else Path.home()/'.claude/skills')
        print(json.dumps(install(target,replace=args.replace),ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError) as error:
        print(json.dumps({'error':str(error)},ensure_ascii=False),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
