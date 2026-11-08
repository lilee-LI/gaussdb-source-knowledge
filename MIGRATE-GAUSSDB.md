# 迁移到 GaussDB：一条可执行的使用路径

本手册对应 **2.3.0 全仓持续学习代码包**，入口固定为：Linux ECS 产图 → Windows 协调端 → 本机 Claude Code 通过 stdio MCP 研究 → 两步审阅 → SQLite 知识与 Wiki → 开发/测试/review 查询。无需部署 HTTP 网关、RAGFlow 或 CodeWiki vendor；Claude Code 与其模型配置使用你现有的环境，不随包提供。

## 能直接用到什么程度

可以在目标环境配置路径后启动盘点、选择模块/特性、由 Claude 实际读源码提交研究、审阅入库、导出 Wiki 和查询。它不是“改几个路径后，无人干预自动学完 GaussDB 全仓并证明知识完备”的系统。

`gaussdb` 适配器是 PostgreSQL 家族线索规则的初始配置，尚未在公司专有 GaussDB 源码与工具链上验收。目录、注册接口或宏不同需要调整适配规则/模块边界；即使没有候选，也可以按模块和问题研究。openGauss 的既有知识不能因迁移程序就当作 GaussDB 已审知识。

`start` 自动生成全仓控制计划和逐资产覆盖账、模块调查、公共机制与跨域任务。模块调查通过审阅后，`advance` 将经审的机制提案按依赖和预算转为后续任务；`run` 使用本机已有Claude执行有界会话并停在待审。`learn`仍可用于手动选题；`ask`返回证据上下文。全仓完成必须通过`coverage`和实际审阅签署，程序不会自己批准研究或知识。

## 1. 准备环境与目录

Windows：64位 CPython 3.12、Git、本机已可使用的 Claude Code。ECS：Linux x86_64/aarch64、Python 3.9+及venv/ensurepip、Git、GaussDB的真实构建工具链与生成头。GCC产图还需要与该编译器匹配的插件开发头，工程不会把产品工具链打进包。

代码包可在ECS和Windows各解压一份。安装使用包内wheel离线进行；Git用于知识修订，源码可以直接使用你本机已有的检出目录，不会因填写source就重新下载产品源码。

示例Windows布局：

```text
E:/kb/engine/                       解压后的工程，含kb.cmd
E:/GaussDB/source/                  与ECS同版的完整GaussDB源码
E:/corpus/design/                   设计文档，可选
E:/corpus/manual/                   用户手册，可选
E:/ecs-export/build-01/             ECS完整交付目录
E:/knowledge/gaussdb/               新建的独立学习工作区
```

学习工作区不要放进源码、文档或代码包目录。不要复制本机已有的`.venv`、Claude设置或openGauss示例知识库作为目标运行环境。

## 2. ECS生成调用图

已有真实`compile_commands.json`时，直接使用，不需要再次采集。

```bash
cd /srv/gaussdb-source-knowledge
sh ecs.sh doctor

sh ecs.sh build \
  --source /srv/GaussDB \
  --compile-db /srv/build/compile_commands.json \
  --work /srv/kb-work \
  --output /srv/export/build-01 \
  --jobs 8
```

使用产品自带GCC时先加载产品构建环境，必要时加`--cc /path/gcc --cxx /path/g++`。建议首次在独立smoke输出目录加`--tu <真实仓内相对路径.cpp>`验证，再生成全量版本。`doctor`或TU分析失败时查看具体工具链、头文件、路径与选项原因，不能把失败当作已完整解析。

没有编译数据库时，CMake可在原构建配置中启用`CMAKE_EXPORT_COMPILE_COMMANDS`；Make工程可用以下命令包住一次真实构建。它会运行你提供的产品构建命令，不属于只读盘点，已有编译数据库就跳过：

```bash
sh ecs.sh capture --source /srv/GaussDB \
  --output /srv/export/compile_commands.json -- make -B -j8
```

把输出的**整个**`/srv/export/build-01/`复制到Windows的`E:/ecs-export/build-01/`，包含`knowledge.sqlite3`、`run.json`及`blobs/`。协调端这条文件回放路径需要本地可访问的完整图；成员可用模块包。不是只复制`compile_commands.json`。

## 3. Windows只配置一个文件

在包含`kb.cmd`的工程目录打开PowerShell：

```powershell
New-Item -ItemType Directory -Force local | Out-Null
Copy-Item paths.example.json local/paths.json
notepad local/paths.json
```

内容如下。没有设计或手册时删除相应字段，不要填不存在的目录。

```json
{
  "product": "GaussDB",
  "product_adapter": "gaussdb",
  "source": "E:/GaussDB/source",
  "design": "E:/corpus/design",
  "manual": "E:/corpus/manual",
  "index_db": "E:/ecs-export/build-01/knowledge.sqlite3",
  "home": "E:/knowledge/gaussdb",
  "graph_storage": "reference"
}
```

设计和手册建议先用文本型Markdown、TXT、HTML，另支持DOCX和有文本层的PDF；须检查实际提取结果。CHM先导出HTML，扫描型PDF不能凭文件存在认定内容已读。源码仓中已有文档仍属于全仓盘点材料。

Windows不填写`compile_commands.json`。`graph_storage=reference`只读引用原图，不把整图再复制进学习库。多个可用run时按检查输出补充`run_id`。自定义产品规则可将`product_adapter`改为自己的JSON文件路径；多仓源码用`repository_roots`补齐ECS记录的仓库ID。

## 4. 按全仓计划持续学习

```powershell
.\kb.cmd check
$kbStart = .\kb.cmd start | ConvertFrom-Json
Start-Process $kbStart.whole_plan.html
.\kb.cmd modules
.\kb.cmd next --worker learner-a --module '<完整模块名>'
.\kb.cmd run --worker learner-a --module '<完整模块名>' --steps 1 --budget 3 --timeout 1800
```

打开的是全仓计划，不是Top-N函数列表。所有源码、头文件、构建与测试资产、文档都进入覆盖账；未提取成功的文档和图外源文件不消失。`PLAN.json`保留版本、领域策略、模块、工作包、候选、依赖和验收缺口，`COVERAGE.csv`用于逐资产追踪。模块数量依版本及目录边界变化；openGauss本次为535模块，不是GaussDB的固定值。

默认先做模块盘点：把多个入口／注册线索归并成机制研究问题，不逐函数建单。盘点提案通过后，按所提机制推进，再自动补足尚未覆盖资产。没有设计的旧特性同样沿源码、测试和手册追踪，保留没有证实的条件。

`run`每步一个Claude会话，只用本工作区MCP；Windows自动寻找本机已安装的原生可执行文件，必要时传`--claude C:/path/claude.exe`。不打包Claude，不读取或复制用户认证。`--budget`是传给CLI的每会话美元限额，实际模型计费以用户配置的服务为准。`--steps`、每任务超时及默认4项待审上限限制并行积压。它没有无限后台自动学习服务。

研究中，MCP的`module_assets`分页查看完整范围，`read_source`分段读取冻结源码并记录回执，`stage_research_unit`提交正文，`stage_progress`提交覆盖／后续机制／契约／缺口，`finish_research`同时校验两个草稿指纹。大文件可以`partial`分段研究：已审知识的同版引用区间跨任务累积，完整之前不算整个文件学完。

## 5. 审阅、继续和使用

```powershell
.\kb.cmd review --task '<run输出的任务ID>' --reviewer reviewer-a
.\kb.cmd review --task '<任务ID>' --reviewer reviewer-a --accept '<研究digest>' --notes '真实审阅意见'
# 有正文时，上一条返回知识提案；核对正文及源码后再接受新digest：
.\kb.cmd review --task '<任务ID>' --reviewer reviewer-a --accept '<提案digest>' --notes '知识审阅意见'
.\kb.cmd advance --max-tasks 8
.\kb.cmd run --worker learner-a --module '<完整模块名>' --steps 2 --budget 3
.\kb.cmd progress --module '<完整模块名>'
.\kb.cmd wiki
.\kb.cmd ask --role coding --question '修改此机制时会影响哪些消费者和资源协议？'
.\kb.cmd ask --role test_generation --question '边界条件、反例和预期依据是什么？'
.\kb.cmd ask --role review --question '有哪些跨模块契约和未验证分支？'
```

纯规划任务没有知识正文，研究审阅后即可推进。知识正文必须另经提案审阅才入库。Wiki和上下文均基于同一已审修订。SQL用例属于源码推导的测试义务，`not_run`不能解释为测试执行通过。

手动选题仍可使用`features`／`learn`。不要把`plan-tasks --apply`对原始线索的兼容批量接口当成新的持续学习入口，持续流程使用`next/run/review/advance`。

失败会话的`home/sessions/*/result.json`、stdout.jsonl、stderr.log记录实际模型、退出状态、时间及任务状态。查看`--home <home> task status --id <ID>`；有效租约通过MCP的`renew_task/checkpoint_task/release_task`或对应task命令管理。不要删除数据库或随意覆盖令牌；到期后可重新领取，证据需在新租约回读。

## 6. 多人在自己的服务器上工作

协调端依模块分派，一个工作单可以连续回传多次：

```powershell
.\kb.cmd --home E:/knowledge/gaussdb team assign --module '<完整模块名>' --worker learner-a --kit E:/exchange/opt-a.zip
```

返回材料包及`opt-a.order.json`工作单，工作单留在协调端。材料包只含成员模块、一跳图和必要材料，不携带模型客户端、认证或全仓图。成员在另一台Windows（或Linux使用kb.sh）解压同版本工程，执行：

```powershell
.\kb.cmd --home E:/member/opt-a team open --kit E:/exchange/opt-a.zip
.\kb.cmd --home E:/member/opt-a whole next --worker learner-a
.\kb.cmd --home E:/member/opt-a whole run --worker learner-a --steps 1 --budget 3
.\kb.cmd --home E:/member/opt-a team export --task '<已提交任务ID>' --out E:/exchange/result-01.gz
```

协调端：

```powershell
.\kb.cmd --home E:/knowledge/gaussdb team receive --input E:/exchange/result-01.gz
# 使用第5节review审阅导入后返回的协调端任务ID
.\kb.cmd --home E:/knowledge/gaussdb team feedback --order E:/exchange/opt-a.order.json --out E:/exchange/feedback-01.gz
```

成员同步签名反馈后继续：

```powershell
.\kb.cmd --home E:/member/opt-a team sync --input E:/exchange/feedback-01.gz
.\kb.cmd --home E:/member/opt-a whole advance
.\kb.cmd --home E:/member/opt-a whole run --worker learner-a --steps 1 --budget 3
# 导出result-02.gz，重复相同流程。
```

反馈传递协调端审阅结论、依赖状态与同版参考知识。退回任务会变成`needs_research`，下次领取修订；已审任务不能被新包覆盖。引用的知识有变化时导入会阻止静默覆盖，先同步并调和差异。工作单与结果包需要在授权团队范围交换；各成员只写自己的本地SQLite。模块重新分配需明确`--replace`，旧工作单随后失效。

## 7. 覆盖验收

```powershell
.\kb.cmd coverage --module '<完整模块名>'
.\kb.cmd coverage
```

文件已列入计划、源码已读、研究已审、知识已入库分别统计。未学资产、未处置候选、未闭合任务／主题、两端未核对的跨模块契约、未解决问题和三类使用检查都会阻止验收。目录未命中不会当作“不适用”；semantic文件声明excluded也不会变成完整覆盖。

编写真实的必要知识回读用例（ID从已审知识取得）：

```json
[
  {"id":"module-coding-01","module":"<完整模块名>","role":"coding","query":"<具体修改问题>","required_units":["<必要机制或契约ID>"]},
  {"id":"module-test-01","module":"<完整模块名>","role":"test_generation","query":"<具体边界及预期问题>","required_units":["<必要测试义务或预期依据ID>"]},
  {"id":"module-review-01","module":"<完整模块名>","role":"review","query":"<具体契约或错误清理问题>","required_units":["<必要知识ID>"]}
]
```

```powershell
.\kb.cmd verify-uses --input E:/acceptance/use-cases.json
.\kb.cmd coverage --module '<完整模块名>'
.\kb.cmd accept-coverage --module '<完整模块名>' --digest '<当前报告digest>' --reviewer owner-a --notes '实际验收意见'
```

不带`--module`才签署全仓。签署绑定当前覆盖账和知识指纹，知识或范围改变会失效。三类检查实际执行上下文检索并验证必要ID进入交付上下文；它们不证明模型回答正确，也不替代专家语义审阅、宏配置覆盖和数据库测试。代码图本身的partial状态单独报告，不能靠知识覆盖把编译证据不足抹掉。

`wiki`可导出部分试点的阅读视图；完整发布需要全仓覆盖签署且原有发布检查通过，部分发布显式使用`--home ... publish --allow-partial`。原始5GB图不进入普通Wiki导出；正式图快照发布属于另一种交付，按publish输出检查大小。

## 8. 配置边界与版本更新

默认`learning_policy=postgres-family`；可选`generic`或填写自定义JSON路径，规则见`adapters/learning/`。GaussDB适配器按PostgreSQL家族提供起点，商业内核的独有目录、注册方式与特性需要在实际接入中核对。用`module_prefixes`固定责任边界；未指定时自然目录细分，绝不按调用边拆任务。

材料变化时执行`start --refresh`生成新快照和计划，旧知识保留版本记录，但不会自动变成新版本已审覆盖。先核对知识变化与受影响范围，再按新计划研究。不要手工把openGauss已审知识改名成GaussDB知识。

实际2.3验证见`docs/VALIDATION-2.3.md`；公司专有GaussDB产品效果需要目标环境核验。软件流程跑通与整个商业内核语义完整是不同的验收项。
