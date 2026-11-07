# 仅基于本仓库的 openGauss 学习流程与实现状态

核对日期：2026-11-07。运行时代码基线：`f53b9c0`。本文只依据 `gaussdb-source-knowledge` 的源码、命令入口、测试代码及仓内验证记录；不借用其他项目的能力或学习成果。目标架构与实际能力分别说明。

当前可以由宿主 Agent 驱动本仓的任务、源码证据、提交、审阅和查询流程。`learn` 创建或复用任务并给出研究指令；`ask` 返回证据上下文。两者都不会直接调用模型完成整个研究或生成最终答案。CodeWiki 有执行适配代码，但尚未成为经 openGauss 验收的通用默认学习流程。

## 1. 输入与配置

输入是匹配的 openGauss 源码、可选设计/手册和已有编译图。程序与方法从本仓读取；源码及生成数据在独立材料/学习目录中。不能把输入源码目录当作另一个知识工程。

在仓库内的 `local/paths.json` 配置，例如：

```json
{
  "product": "openGauss",
  "product_adapter": "opengauss",
  "source": "D:/corpus/openGauss",
  "index_db": "D:/corpus/openGauss-index/knowledge.sqlite3",
  "run_id": "<该交付图中真实的 run ID>",
  "graph_storage": "reference",
  "home": "opengauss-workspace"
}
```

这些路径和 run ID 是示例，需替换成实际输入。相对 `home` 以配置文件所在目录解析；此例即 `local/opengauss-workspace`。有手册/设计时增加真实 `manual` / `design` 路径，缺失则保持缺失。输入不应与学习工作区重叠。

`project.py` 未显式配置产品时默认使用 GaussDB，因此 openGauss 必须写明产品身份。`check` 验证路径与图接口；`start` 冻结材料、核对源码和图的配套关系、登记索引能力并生成学习计划。只读挂接复用原图，不为学习库再复制一份大图。

仓内[验证记录](LOCAL-VALIDATION-20261107.md)显示，历史 openGauss 查询使用的是 2,412 个 TU 中 818 parsed / 1,594 partial 的旧图，而且旧学习库的产品标签曾使用默认 GaussDB。正式试点需新建正确绑定，不能直接继承其产品标签、完整性或研究状态。另一次 GCC 产图成绩与此本地查询回放分开看。

## 2. 当前如何规划

已存在以下命令；本轮实际核验了 `plan-tasks`、`learn`、`review`、`ask` 的 CLI 帮助，未对真实 openGauss 执行新一轮 `start` 或建单。

```powershell
.\kb.cmd check
.\kb.cmd start
.\kb.cmd modules
.\kb.cmd features --limit 30
.\kb.cmd plan-tasks --max-tasks 20
```

`start` 通过 `study.py` 盘点源码并建立模块调查任务，借助 `catalog.py` 从参数注册、语法、测试 SQL 和文档段落发现候选。内置 `opengauss` 适配器当前继承 `postgres-family`，没有专门的模块规则；默认归属主要来自目录。候选是待核对问题，不是已证明的完整特性。

`product_adapter.py` 对错误、内存、兼容和宏等采集词法线索，每模块每专题默认最多 12 条，超过单文件 2,000,000 字节的信号扫描会记为缺口。因此该输出不能当作全量错误点、内存上下文或宏分支清单。

模块调查由 Agent 实际阅读入口、状态、消费者和必要测试，给出有来源的新机制、拆分/合并及前置依赖。反馈用 `planning-feedback` / MCP `planning_feedback` 登记。然后 `task_planning.py` 按已声明依赖、模块范围和批次预算建任务；程序不会自行推导所有业务机制及其语义依赖。

```powershell
.\kb.cmd planning-feedback --input local/sort-feedback.json
.\kb.cmd plan-tasks --module "<modules 返回的完整模块 ID>" --max-tasks 12
.\kb.cmd plan-tasks --module "<同一个完整模块 ID>" --max-tasks 12 --apply
```

反馈文件要包含真实 study plan、模块 ID、冻结材料 key 和有效行号，不可直接用示意名称入队。一个机制可引用多个模块的证据，同时指定一个归属模块。依赖在下一批范围外时保留缺口；已完成前置任务是领取后续任务的条件。

任务已经保存：版本和图绑定、研究问题、初始文件与证据、依赖、专题待判项、预期产物、预算和审阅要求。当前默认每批 20 项、每项初始文件 12 个；这是起始读取预算，不是只允许研究 12 个文件或已经读完这些文件。

## 3. openGauss 的实际学习安排

先保留全仓材料与模块地图，再完成排序的有界研究及问答验收。排序通过后，按实际消费者和可复用机制扩展到相关执行器/优化器功能，然后推进其他模块。不会根据目录数或函数数一次性宣称已经形成完整课程。

下表是建议 Agent 在源码调查后确认的排序工作包，**不是当前 `plan-tasks` 已自动生成或已执行的任务**。不存在或不适用的项需有依据地处理。

| 建议工作包 | 需要回答的问题 | 研究产物 |
| --- | --- | --- |
| 范围与入口 | 哪些排序实现、调用方、测试和构建分支属于本次范围？ | 特性候选、源码入口、排除项及待确认项 |
| 基本机制与状态 | 数据如何进入、比较、排序、输出；关键状态怎样变化？ | 条件化主流程、状态与接口契约 |
| 有界排序与访问方式 | Top-N、随机访问、重扫等条件怎样影响路径？ | 分支条件、复用/重建规则和反例 |
| 外部排序与临时资源 | 何时产生外部数据，如何归并及管理临时资源？ | 数据阶段、临时文件及清理契约 |
| 内存与参数 | 谁提供预算，哪些 GUC 和中间字段参与，谁拥有内存？ | 参数注册到消费者的路径、所有权和生命周期 |
| 比较语义与兼容 | 类型、比较器、NULL、排序规则及兼容条件如何关联？ | 语义条件矩阵、相关绑定和未覆盖分支 |
| 错误与异常退出 | 各检测点的前提、错误码、传播和正常/异常清理是什么？ | 错误点清单、条件与清理证据 |
| 变体、消费者与观测 | 相关向量/并行等变体何时适用；其他调用方和观测口径是什么？ | 变体处置、跨模块契约、测试依据和补学清单 |

每个工作包同时检查错误、内存、兼容和 GUC 的适用性，避免最后补一张泛化列表。共享机制先研究当前任务需要的接口和条件，以知识引用复用；后续专题盘点再扩展其覆盖范围。

执行顺序由真实依赖调整：范围调查先行；基本接口和必要公共机制支撑后续分支；各机制完成后综合并接受问答验收。这里的分组和优先级是本次规划，不是已经实现的自动语义排序算法。

## 4. 一个任务实际怎样执行

可按真实候选创建/复用任务：

```powershell
.\kb.cmd learn --candidate "<features 返回的候选 ID>" --worker learner
```

也可使用 `--module` 与 `--question` 明确创建有界问题，必要时提供 `--file`、`--symbol`。`learn` 返回任务 ID、该工作区 MCP 配置和研究指令，**不表示已经读过源码**。

宿主 Agent 连接 `start` 生成的 `researcher.mcp.json`，实际执行：

```text
next_tasks → claim_task → task_context
    → query_graph / 创建证据锚点 / read_task_evidence
    → 研究条件、调用或数据路径、边界、专题细节
    → stage_research_unit → finish_research
```

这些工具在 `service.py` 中有实现。读取记录区分完整与截断，提交需要有效租约和引用依据；新依赖通过研究反馈登记。Agent 执行理解与写作，程序管理输入身份、流程及可机械检查的约束。

`source-repository-learning` 及专题文件在**本仓** `skills/`、`engine/`、`references/` 中有受 Git 管理的版本。`unified_skill_methods.py` 只允许解析本仓范围内的方法路径。它们是研究输入，不能替代真实研究；也不能据其文字宣布功能已完成。

## 5. 审阅、产物和查询

```powershell
.\kb.cmd review --task "<实际任务 ID>" --reviewer reviewer
```

命令先返回研究结果、证据和摘要供实际核对；`--accept <digest> --notes <真实意见>` 接受对应研究后，还要核对另一份知识提案及其摘要。研究审阅与知识审阅分别记账，程序记录自审/独立审阅声明，不能据不同用户名认定已获真实专家批准。

接受后形成结构化知识、源码引用、知识关系和私有 Git 修订；`wiki` 导出 Markdown/HTML；检索发布通过 `platform prepare → sync → activate` 完成。源码调用关系保留在原图，知识中的关键路径与之关联。

```powershell
.\kb.cmd wiki
.\kb.cmd ask --question "排序的内存预算来自哪里，何时生效？"
```

`ask` 和 `platform query` 返回不同接口下的证据上下文，默认检索是词法基线，未接入真实语义 embedding。最终自然语言回答由宿主 Agent 基于上下文和必要的源码补读生成。空知识库不会因执行 `ask` 自动变成已学知识库。

## 6. 已实现、部分实现与尚未完成

| 能力 | 本仓当前状态 | 证明边界 |
| --- | --- | --- |
| 材料绑定、索引挂接、源码查询 | 已实现 | 仓内有软件验证和旧 openGauss 图查询记录，不是全配置语义验证 |
| 全仓目录、候选和模块调查任务 | 已实现 | 目录归属、规则/文档线索；不是全量特性发现保证 |
| 任务批次、去重、依赖、租约、反馈 | 已实现 | 依赖及新机制需研究者提供，程序做持久化和检查 |
| Agent 证据读取、分项提交与审阅 | 已实现 | 可承载宿主驱动的真实研究；不能把软件 fixture 当产品研究 |
| 正式知识、Wiki、发布与 MCP | 已实现 | 支持版本化查询；答案生成依赖宿主 Agent |
| CodeWiki 执行适配 | 部分实现，有具体缺陷 | 尚未成为默认通用全流程，见下文 |
| 效果评估 | 部分实现 | 能测已发布知识 ID 的召回；未入库机制覆盖和答案语义仍缺独立评估 |
| 增量维护 | 有依赖/变化/修订代码 | 源码、公共头、宏和生成材料等真实 openGauss 全链路仍待验证 |
| 排序完整知识包及效果 | 尚未验收 | 没有依据证明全量特性、四专题、必要调用路径都已覆盖并有效召回 |
| 全仓持续自动学习及 GaussDB 效果 | 尚未验收 | 不能从任务数量、产图成功或合成测试推导 |

CodeWiki 的具体边界：独立 `codewiki_learning.py` 接受 baseline、scope、module_tree 等试点输入；`worker.py` 包装层在无已审知识时可以生成 `scope.md` 占位 baseline，因此“必须由用户先写旧 Wiki”不是对整条包装流程的准确描述。但它仍未完成通用原生模块规划，提示中还固定了旧试点页面名。

本轮还将 `worker.py` 默认的 `{name, path, children}` 模块树直接传给当前 `generation_prompt`，复现 `AttributeError: 'str' object has no attribute 'get'`：提示函数遍历 `tree.values()` 时期待每项都是节点。该检查未启动模型，模型调用数为 0；本轮未修复运行时代码。因此有适配脚本不能当作任意模块开箱即用的证明。

评测器当前要求金标知识 ID 已在发布集中，且将答案正确性标为 `not_evaluated`。下一步须增加独立源码机制分母和真实答案/证据评分，再开展同问题、同模型与预算下的源码直接查询、原生文档、已核对知识对照。

## 7. 本轮核对与接续工作

本轮仅检查本仓代码与历史报告，执行四项 CLI 帮助和上述默认模块树检查；没有新跑 openGauss 学习、创建正式任务、启动模型、执行数据库或重跑全量软件测试。[历史验收记录](LOCAL-VALIDATION-20261107.md)中的 50 项测试及合成流程保持其原有证明范围。

具体接续顺序：正确绑定 openGauss 材料；由当前 Agent/MCP 流程完成排序范围调查并登记真实机制任务；修正并验证 CodeWiki 适配；完成逐项研究与审阅；补独立覆盖和答案评估；验证变更后再扩大范围。效果试点任务 E01–E05 仍以[工作单](plans/knowledge-effectiveness-pilot-20261107.md)为准。

代码入口：[project.py](../scripts/unified_knowledge/project.py)、[study.py](../scripts/unified_knowledge/study.py)、[catalog.py](../scripts/unified_knowledge/catalog.py)、[task_planning.py](../scripts/unified_knowledge/task_planning.py)、[service.py](../scripts/unified_knowledge/service.py)、[worker.py](../scripts/unified_knowledge/worker.py)、[evaluation.py](../scripts/unified_knowledge/evaluation.py)。
