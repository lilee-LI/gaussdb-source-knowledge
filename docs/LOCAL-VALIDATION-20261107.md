# 本地工程验收记录：2026-11-07

范围为 `feat/knowledge-platform-20261107` 的本地软件工程。外部 RAGFlow、模型与 GaussDB 实机接入按用户要求延后。验证环境为本机 Windows、Python 3.12；未运行数据库、SQL、产品构建或故障注入。

## 已执行

| 验证 | 结果 | 证明范围 |
| --- | --- | --- |
| `python -m unittest discover -s tests -v` | 50 项通过，34.015 秒 | 原有流程和新增适配、规划、查询、发布、召回、MCP 的软件回归 |
| `python -m pip check` | 无依赖冲突 | 当前虚拟环境与扩展锁文件安装结果 |
| `verify_local_platform.py` | 通过，41.453 秒 | 先执行 58 条命令的双成员合成样例流程，再执行本地发布、幂等回放、完整证据组和无答案检查 |
| 官方 MCP 客户端 → 真实本地 Uvicorn 服务 | 通过，包含于上述 50 项 | Streamable HTTP 初始化、工具列表、查询、只读拒绝与正常关闭 |
| RAGFlow HTTP 客户端 | 协议测试通过 | MockTransport 模拟解析状态、重试、内容与元数据检查；未连接真实 RAGFlow |
| `benchmark_source_gateway.py` → 既有 openGauss 图 | 80 次成功 | 单个实际符号的一跳查询、同版证据读取与并发响应大小 |

测试中的研究者/审阅者为合成软件测试身份，不能当作专家批准。Starlette TestClient 有 httpx 弃用提示；测试全部通过，升级相应测试依赖时需要处理。查询端拒绝研究写入工具的测试会产生预期的未注册工具日志。

本地运行产物：`local/platform-acceptance-20261107/report.json`、`evaluation-report.json`、`context.json`；阅读样例为 `local/platform-acceptance-20261107/workflow/hub/wiki/index.html`。`local/` 不进入工程 Git 和程序包。

## 实际大图回放

本次复用 **旧 Clang 图**，不是另一个已经完成 GCC 产图的新交付件：

- 上游 run：`assembled:b903fa933f3a06291012d7b747b26896`。
- 上游源码快照：`snapshot:66156d6549a4f1307abe4822a89063f1`，profile：`linux-native`。
- 图文件：5,276,512,256 字节，约 4.914 GiB。
- 索引报告 2,412 个 TU：818 parsed、1,594 partial；398,544 个符号、1,994,720 条关系。保持 `semantic_completeness=not_certified`。
- 学习库 `main.symbols`、`main.relations` 均为 0；图只读挂接，查询未启动编译前端。
- `ExecSort` 定义的一跳查询，8 并发、80 次请求；每次 30 条关系，无截断，最大响应 10,054 字节。
- 查询 P50 **15.360 ms**、P95 **31.115 ms**、最大 39.041 ms；包含每次工作区打开为 P50 111.686 ms、P95 144.623 ms、最大 170.611 ms。

操作系统缓存未清空，测量前已做符号定位和证据读取。这些数据不代表冷缓存、高扇出、跨模块完整路径、模型端到端问答或公司 500 万行源码的容量成绩。原始回执保存在 `local/opengauss-gateway-benchmark.json`。

发现并修复的实际问题：最初通过合并视图查询并按 ID 排序时，SQLite 选择了遍历整个 run 的主键路径，超过 2 秒执行预算。修复为分别在本地表和挂接图上按 `(run, name)`、`(run, source/target)` 索引定位，取有限记录后合并，再执行分页。索引名称从实际数据库读取；缺必要索引时明确报错。上面性能结果来自修复后的重跑。

历史身份缺口：旧学习工作区的 `product` 使用了默认值 `GaussDB`，实际输入是公开 openGauss；旧计划也没有新增适配器摘要。本次保留原始回执，没有修改历史绑定或把它称为 GaussDB 验收。新项目必须显式配置真实 `product` 和 `product_adapter`，正式领域发布前重新建立正确绑定。源码未核实 Git HEAD，仍使用冻结内容摘要；不借用其他 checkout 的提交号。

## 可重复命令

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 scripts/verify_local_platform.py --output local/acceptance-new
.\.venv\Scripts\python.exe -X utf8 scripts/benchmark_source_gateway.py --home <现有学习库> --output local/gateway-new.json --concurrency 8 --requests 80
```

验收脚本的输出目录必须是新路径。依赖与操作方法见 [LOCAL-PLATFORM.md](LOCAL-PLATFORM.md)。包从 Git 暂存区的精确文件字节生成，附每文件 manifest 和整包 SHA-256；程序包不包含产品源码、用户学习库或服务密钥。平台扩展仅提供锁文件，尚未验证其离线 wheel 安装；核心离线安装能力沿用原工程。

## 尚未证明

openGauss 排序的全量特性及错误、内存、兼容、GUC 知识是否充分；200 道领域金标题及真实召回/回答正确率；模型自动研究吞吐；RAGFlow 服务互通及检索效果；GaussDB 实际源码、真实宏配置和 500 万行容量；全部更新类型在实际产品上的增量/全建一致性。本次完成了这些工作的工程承载和部分软件验证，不能用流程成功代替领域结论。
