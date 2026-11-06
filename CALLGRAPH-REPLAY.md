# ECS 交付与 Windows 查询

ECS 沿用已有并发分析程序。按实际构建冻结源码、宏和编译命令，交付工程格式的 `knowledge.sqlite3` 一致性备份及已完成的 `run_id`。保留构建 profile 和快照摘要。上游若使用 WAL，用 SQLite 的备份 API 将运行中库导出为一个新文件。

~~~bash
python3 - /srv/index/knowledge.sqlite3 /srv/export/build-01/knowledge.sqlite3 <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3, sys
src, out = map(lambda p: Path(p).resolve(), sys.argv[1:])
out.parent.mkdir(parents=True, exist_ok=True)
if out.exists():
    raise SystemExit("Choose a new output path")
with closing(sqlite3.connect(src.as_uri()+"?mode=ro",uri=True)) as read:
    with closing(sqlite3.connect(out)) as dest:
        read.backup(dest)
PY
~~~

将交付件放在 Windows 协调端可访问的位置。配置 `source` 与 `index_db`，执行 `kb.cmd check`、`start`。协调端只读挂接上游，通过 SHA-256 校验并冻结材料。`home` 指向学习工作区。查看某个函数的上下游：

~~~powershell
.\kb.cmd --home E:/kb/hub navigate --symbol <函数名> --direction forward
.\kb.cmd --home E:/kb/hub navigate --symbol <函数名> --direction reverse
~~~

只查询调用边时可用 `graph --run <start返回的学习run> --targets <符号> --kind CALLS --direction forward --depth 2`。候选边和未解析边保留原状态。类型、字段、宏、包含关系取决于上游实际导出的关系种类。间接分派、异步消息以及状态写入和消费需要研究者核对注册、生产与消费源码。线上真实调用顺序需要运行观测。

例如精简测量库只含 `funcs/pairs/sites`，需要先适配到本工程包含快照、证据和符号的上游合同。详见 [设计](docs/DESIGN.md)。
