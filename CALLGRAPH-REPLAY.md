# ECS 交付与 Windows 查询

## 生成第一份图

在真实构建机加载产品平时编译所用的环境，准备源码、依赖和配置步骤生成的头文件。Python 需要 3.9 或以上，含 venv、ensurepip 和启用了 JSON 的 SQLite；准备 Git 与项目 C/C++ 工具链。GCC 路径需要该编译器的匹配插件头文件（`gcc -print-file-name=plugin` 返回目录下的 `include/gcc-plugin.h`），工程自动编译插件。Clang 路径使用离线 libclang。进入仓库根目录执行 `sh ecs.sh doctor` 检查 Python 运行环境；产品工具链在 `build` 的前置步骤验证。

1. 已有 `compile_commands.json` 可直接进入下一步。对于 Make，执行 `sh ecs.sh capture --source /srv/src --output /srv/compile_commands.json -- make -B -j4`。采集器在当前子进程的 PATH 放入编译器包装器，保留原参数并转发给真实编译器。没有重新编译或构建失败时不签发编译数据库。Makefile 固定编译器绝对路径时，使用项目的 CMake 导出，或使用系统 Bear 捕获真实构建。使用 CMake 的 Makefiles/Ninja 生成器可在原配置命令加入 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`。[LLVM 编译数据库格式](https://clang.llvm.org/docs/JSONCompilationDatabase.html) · [CMake 导出选项](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
2. 执行以下命令。保持源码、工作与交付目录互相独立；`--output` 必须是新目录。默认 4 个工作进程以内，显式 `--jobs` 可设 1–128。先按机器内存和 TU 大小选择并发。加入一个或多个 `--tu src/…/file.cpp` 可先跑子集。

~~~bash
sh ecs.sh build --source /srv/src --compile-db /srv/compile_commands.json \
  --work /srv/kb-work --output /srv/export/build-01 --jobs 4
~~~

3. 将整个 `build-01/` 复制到 Windows。检查 `run.json` 的 `coverage.parsed_tus/partial_tus/failed_tus/deferred_tus`、`source_evidence_files` 和 `sha256`。在 PowerShell 可用 `Get-FileHash E:/ecs-export/build-01/knowledge.sqlite3` 对照摘要。设置 `index_db` 后运行 `kb.cmd check` 和 `kb.cmd start`。

## 构建差异和重试

- `--frontend auto` 按配置的编译器选择前端；也可显式选择 `gcc` 或 `clang`。GCC 使用同版本的官方插件 API，在 `-fsyntax-only` 下提取优化前的函数及调用，不生成产品目标文件，不链接或运行产品。构建本工程插件是独立前置步骤。Clang 使用 libclang；GCC 的 GNU 扩展由真实 GCC 解释，未添加可写字符串等放宽语义的选项。
- `--facts calls` 是默认值。GCC 导出当前配置下可实例化的函数及调用树，重载按 ABI 名称区分，虚调用和间接调用保留候选；未实例化模板、内联汇编内部调用和未启用宏分支不承诺完整覆盖。`--frontend clang --facts full` 额外记录 libclang 观察到的类型、字段、宏展开和包含边。GCC 路径当前不提供 full 模式。不同宏配置用不同编译库和 `--profile` 值分别构建。
- 使用项目 GCC 时，通过 `--cc /path/to/gcc --cxx /path/to/g++` 指定真实构建工具链，并继承构建机的库路径。GCC 会先并发执行预处理依赖发现，再冻结包括非标准扩展名在内的实际输入，保留原编译参数；前端随后解析冻结副本，并还原源码路径宏与文件时间。Clang 的 `--no-driver-includes` 可关闭驱动头目录探测。可用 `--extra-arg=-I/path` 补充参数，仅在核实含义后使用 `--drop-arg=…`；所有显式适配和原编译库摘要写入报告。
- Flex/Bison 的重复 `#line` 使用编译器活动 line-map 恢复生成文件的实际行号，并保留原始 `.l/.y` 显示位置。相同 `gram.y` 名字不会跨解析器猜测归属。当前 GCC 插件的实机验证范围为 Linux x86_64、原生 GCC 10.3.0；其他版本和交叉编译工具链需先运行随包的 `verify_gcc_producer.py`。
- 支持 GNU 风格响应文件，保留 `-D/-U`、语言、目标架构及显式搜索路径。工程内指向普通文件的符号链接按内容冻结，记录链接目标。GCC 依赖发现自动纳入宏选中的 `.map`、`.ini` 等输入；Clang 自定义扩展名头文件仍可用 `--include-file 仓内路径` 指定。依赖发现阶段有错误时默认立即阻止构建；后续 TU 错误和超时分别保留诊断。
- 查看工作目录中的 `last-build.json`。修复输入后用原 `--work` 重试。每个 TU 单独提交；内容、前端参数和头文件查找均可校验时可复用。无充分证据的缓存会重新解析。默认阻止含失败或部分解析 TU 的交付；核对后可显式加 `--allow-partial`，仍要求至少一个 TU 干净解析。主动选择子集时，计划单列其余延后 TU。
- `knowledge.sqlite3` 仅导出所选 run 的事实、锚点和快照，不携带解析工作队列和 TU 缓存。`blobs/` 用于 Windows 缺少生成头文件、未跟踪文件或链接时的取证，内容按 SHA-256 去重。协调端仍需要完整源码来做全仓盘点。

## 已有兼容索引

从 2.1.x 升级时，旧交付仍能在 Windows 读取；它的 partial 不会因升级软件自动变成 parsed。需要修复后的图时，在 ECS 用新版本和独立的 `--work`、`--output` 重新分析，保留旧交付。Windows 将 `index_db` 改为新交付，并用新的 `home` 执行 `check/start`。GCC ABI 和 Clang USR 的符号身份不同，已有研究按原 run 保留，不能直接替换其符号 ID。

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

`graph_storage=reference` 是对可访问 SQLite 文件的只读挂接，不是通过网络 API 查询 ECS。Windows 作协调端时仍需完整交付图；成员可使用模块包。若将协调端放在 ECS，需要另备 Python 3.12、完整源码与文档，Windows 作为成员领取模块包；本轮尚未对此部署完成实机全流程验收。模块包包含整个模块及一跳邻居，目前没有大小预算限制。

~~~powershell
.\kb.cmd --home E:/kb/hub navigate --symbol <函数名> --direction forward
.\kb.cmd --home E:/kb/hub navigate --symbol <函数名> --direction reverse
~~~

只查询调用边时可用 `graph --run <start返回的学习run> --targets <符号> --kind CALLS --direction forward --depth 2`。候选边和未解析边保留原状态。类型、字段、宏、包含关系取决于上游实际导出的关系种类。间接分派、异步消息以及状态写入和消费需要研究者核对注册、生产与消费源码。线上真实调用顺序需要运行观测。

例如精简测量库只含 `funcs/pairs/sites`，需要先适配到本工程包含快照、证据和符号的上游合同。详见 [设计](docs/DESIGN.md)。
