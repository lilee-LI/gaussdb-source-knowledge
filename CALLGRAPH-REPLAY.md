# ECS 交付与 Windows 查询

## 生成第一份图

在真实构建机加载产品平时编译所用的环境，准备源码、依赖和配置步骤生成的头文件。Python 需要 3.9 或以上，含 venv、ensurepip 和启用了 JSON 的 SQLite；准备 Git 与项目 C/C++ 工具链。进入仓库根目录执行 `sh ecs.sh doctor`，首次启动会离线安装当前 CPU 架构的 libclang。

1. 已有 `compile_commands.json` 可直接进入下一步。对于 Make，执行 `sh ecs.sh capture --source /srv/src --output /srv/compile_commands.json -- make -B -j4`。采集器在当前子进程的 PATH 放入编译器包装器，保留原参数并转发给真实编译器。没有重新编译或构建失败时不签发编译数据库。Makefile 固定编译器绝对路径时，使用项目的 CMake 导出，或使用系统 Bear 捕获真实构建。使用 CMake 的 Makefiles/Ninja 生成器可在原配置命令加入 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`。[LLVM 编译数据库格式](https://clang.llvm.org/docs/JSONCompilationDatabase.html) · [CMake 导出选项](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
2. 执行以下命令。保持源码、工作与交付目录互相独立；`--output` 必须是新目录。默认 4 个工作进程以内，显式 `--jobs` 可设 1–128。先按机器内存和 TU 大小选择并发。加入一个或多个 `--tu src/…/file.cpp` 可先跑子集。

~~~bash
sh ecs.sh build --source /srv/src --compile-db /srv/compile_commands.json \
  --work /srv/kb-work --output /srv/export/build-01 --jobs 4
~~~

3. 将整个 `build-01/` 复制到 Windows。检查 `run.json` 的 `coverage.parsed_tus/partial_tus/failed_tus/deferred_tus`、`source_evidence_files` 和 `sha256`。在 PowerShell 可用 `Get-FileHash E:/ecs-export/build-01/knowledge.sqlite3` 对照摘要。设置 `index_db` 后运行 `kb.cmd check` 和 `kb.cmd start`。

## 构建差异和重试

- `--facts calls` 是默认值，按配置后的宏分支记录函数、调用点、跨文件绑定和源码行号。`--facts full` 也记录 libclang 观察到的类型、字段、宏展开和包含边。不同宏配置用不同编译库和 `--profile` 值分别构建。
- 使用项目 GCC 时，通过 `--cc /path/to/gcc --cxx /path/to/g++` 选择头文件搜索路径所用的真实驱动，并继承构建机的库路径。交叉编译、显式 sysroot 或关闭标准包含时，请按实际目标提供头文件。可用 `--no-driver-includes` 关闭本机探测，用可重复的 `--extra-arg=-I/path` 添加前端参数。仅在核实含义后使用 `--drop-arg=…`；所有省略项和原编译库摘要写入报告。
- 支持 GNU 风格响应文件，保留 `-D/-U`、语言、目标架构及显式搜索路径。工程内指向普通文件的符号链接按内容冻结，记录链接目标。自定义扩展名头文件可用 `--include-file 仓内路径` 纳入快照。缺失头文件、不可识别的参数、超时会在对应 TU 标为失败或带诊断的部分解析。
- 查看工作目录中的 `last-build.json`。修复输入后用原 `--work` 重试。每个 TU 单独提交；内容、前端参数和头文件查找均可校验时可复用。无充分证据的缓存会重新解析。默认阻止含失败或部分解析 TU 的交付；核对后可显式加 `--allow-partial`，仍要求至少一个 TU 干净解析。主动选择子集时，计划单列其余延后 TU。
- `knowledge.sqlite3` 仅导出所选 run 的事实、锚点和快照，不携带解析工作队列和 TU 缓存。`blobs/` 用于 Windows 缺少生成头文件、未跟踪文件或链接时的取证，内容按 SHA-256 去重。协调端仍需要完整源码来做全仓盘点。

## 已有兼容索引

也可以接入先前产出的同格式 SQLite 与 `run_id`。若从使用 WAL 的活动工作区手工导出一致性副本，使用 SQLite 备份 API：

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
