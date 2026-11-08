---
name: gauss-knowledge
description: 在当前 Claude Code 会话中学习 GaussDB/openGauss 源码和用户手册，生成全仓计划、按模块续学、带源码证据的知识、Wiki 和开发/测试/review 上下文。用于源码建库、继续模块学习、查询知识和审阅入库；无需由工程另起 Claude。支持只有源码和手册、没有设计文档或编译调用图的环境。
argument-hint: "源码=<路径> 手册=<路径> 工作区=<路径>；或：继续 / 计划 / 学习 <模块> / 查询 <问题> / 审阅 <任务>"
user-invocable: true
---

# 当前会话执行

由**当前会话**理解用户目标、阅读材料、分析机制、撰写知识。Python 助手只调用工程原有的任务、证据、审阅和查询 API；不执行 `kb run`、`whole run`、`claude -p`，也不通过 SDK/API 再启动模型。不需要先配置 MCP。

## 定位工程和材料

本文件位于 `<工程>/skills/gauss-knowledge/SKILL.md`；从本文件**所在目录上行两级**为工程根目录 `ENGINE`（即 `Path(SKILL.md).resolve().parents[2]`）。如果通过 `.claude/skills` 安装入口进入，以入口提供的工程路径为准。不要把源码目录当作工程目录。

1. 从用户输入读取源码、手册和输出工作区路径，或已有 `paths.json`。缺少设计、调用图不阻止开始。没有输出路径时由助手返回默认路径；输出不能放在输入材料目录内。
2. 查找 Python 3.12：优先工程 `.venv/Scripts/python.exe`（Linux `.venv/bin/python`），其次 Windows `py -3.12` 或 `python`，Linux `python3.12`。路径带空格时正确引用，用户的自然语言不能直接拼进 shell。需要 Python 3.12 和 Git；缺少时说明缺项，不尝试安装客户端或改变模型/认证。
3. 所有操作使用 `ENGINE/scripts/claude_session.py`。若工程没有 `.venv`，它会校验完整发行包并从包内 wheels 离线准备 Python 依赖。**首次不安装 Claude，也不下载产品源码。**
4. 初始化（`PY` 表示上一步实际找到的 Python 命令，之后以绝对脚本路径调用）：

```text
PY "ENGINE/scripts/claude_session.py" --session "SESSION" init --source "SOURCE" --manual "MANUAL" --home "HOME"
```

已有配置用 `--session "SESSION" --paths "PATHS" init`。公开源码可加 `--product openGauss --adapter opengauss`。只有源码时省略 `--manual`；已有 ECS 图继续使用配置的 `index_db`，不要把原始 `compile_commands.json` 当作 `--index-db`。

`SESSION` 优先使用入口替换出的当前 Claude session ID；若入口没提供就省略 `--session`，助手会生成 ID。记住返回的 **session、paths、home**。此后每次调用均为：

```text
PY "ENGINE/scripts/claude_session.py" --paths "PATHS" --session "SESSION" ACTION ...
```

下文用 `K ACTION ...` 简写这段调用，实际 shell 要展开完整路径。全局参数 `--paths`、`--session` 写在 ACTION **之前**。保存初始化输出到会话摘要，断点后不要猜工作区或换 worker。不要读写 `assistant-sessions/*/handle.json` 来改身份或租约。

## 全仓规划和领取

- 用户只要求规划：执行 `K plan`、分页 `K modules`，展示返回的 PLAN.md / PLAN.json / index.html 与模块数量，到此结束，不擅自开始全仓研究。
- 用户指定优化器等自然语言模块：`K modules --query "优化器"`（也可查 `optimizer`），展示/选择返回的**完整模块 ID**。大范围先盘点再分机制，不能把函数和调用边逐条变成学习任务。
- 执行 `K next --module "完整模块ID"`。返回 claimed/resumed/reclaimed 时读取完整任务上下文；awaiting_review 时停止研究并报告待审；in_progress/waiting_review/blocked 等按返回原因报告，不伪造成功。
- 默认本轮完成一个有界任务。用户明确要求持续或完成模块时，在审阅权限范围内循环，直到达到用户要求、待审、预算或材料缺口；不可宣称一个会话已学完全仓。
- `next` 恢复本会话有效租约；过期后重新领取会增加 attempt，**本轮重新阅读证据**。它不会继承另一会话的活动租约。切换模块前提交/审阅或 `K release`。

## 真实学习

先读 `context.methods` 中适用的冻结方法（用下面的 `read`），再读任务问题、previous_research、dependency_results、已审复用知识、active_progress 和 review_feedback。工程旧方法文件提供专题方法；本文件规定当前会话入口和工具映射，不按旧文档去另起模型。

1. `K assets --offset 0 --limit 30` 分页盘点所属资产；`K candidates` 分页查看原始线索，ID 原样使用；`K materials --kind document` 找到手册/设计的实际资产 ID，按需用 `--query` 过滤。上下文的 document_matches / selected_files 是材料线索。
2. `K search --query "标识符"` 默认搜本任务材料。跨模块或手册用重复的 `--asset "server/.../*"`、`--asset "manual/*"`，路径前缀以实际资产 ID 为准。按返回的 next_file_offset / next_line_offset 继续分页。
3. `K read --asset "返回的资产ID" --start 1 --lines 200` 读取冻结源码/文档/方法；按 next_line 继续，最多400行。保留返回的 evidence `id`。搜索命中不是阅读；普通 Read 可读 skill、草稿、配置，却不能替代研究证据回执。不要让未经阅读的材料支持结论。
4. 沿入口→状态生产→变换→消费→正常/异常出口追踪；查跨模块读写、配置/宏分支、所有权/生命周期、缓存、错误与必要并发/恢复边界。手册预期与代码行为分开记录；适用范围/调用方前置条件不等于代码承诺防御检查，只有相同条件下的行为不一致才判文码冲突。疑点保留为 gap，未命中关键词不证明不存在。
5. source_only 时用文本证据说明实现、消费者与影响；编译配置、宏选中、重载/间接调用分辨率保持待核。`K symbols` / `K graph` 会明确返回不可用；不要去生成全仓索引、解析 TU，或杜撰 symbol ID、正式 contract / call step。可用 claim 说明跨模块关系、flow 的 data_stage/state_transition 描述过程。
6. 有图时 `K symbols --query "名称"` 获得真实 ID，`K graph --target "ID"` 获取一跳 CALLS 候选，仍回读两端源码和条件，图不等于运行路径。未解析边保留未知。

## 暂存和提交

先读 [结构化格式](references/formats.md)。每次用 Write 在 `HOME/drafts/` 写一个 UTF-8 JSON 文件，再通过助手保存；别在 shell 内手拼大段 JSON。文件名区分 session/task，避免多人覆盖。

- 知识正文：`K unit --input "unit.json"`。一项一个文件；unit.kind/id/title/body/source_refs 等按合同。body 要能指导开发、测试和 review，包含适用条件、关键状态/调用位置、消费者影响、反例和未知。更新已有草稿需 `--previous-hash`；`K drafts` 返回正文及 hash。
- 覆盖和下一步：`K progress --input "progress.json"`。合并更新需上次 `--previous-digest`；`K context` 返回当前完整 active_progress。
- module_survey 优先输出**真实资产盘点和归并后的机制研究提案**，可不写知识单元。未深学文件用 deferred；浏览一段不能标 studied。对大文件用 partial + 真正已研究单元和引用区间。只有确实完成盘点才设置 inventory_complete=true。
- 新机制只登记在 progress.proposals，依赖/gap 写在同一报告；不额外创建第二份任务队列，不逐候选/函数/边泛化成任务。
- `K submit --input "coverage.json"` 保存问题覆盖并使用最新草稿 digest 提交。成功返回 submitted/**awaiting review** 即停止本轮研究。它只做结构与证据校验，不能证明语义正确，也不会自动接受知识。
- 中断前 `K checkpoint --input "checkpoint.json"`；长会话 `K renew`。lease 默认为4小时，过期必须通过 `next` 重新领取和实际回读。

## 审阅和入库

用户仅要求“学习”时默认停在待审。用户要求“审阅/入库/完整产出并查看 Wiki”时可做实际审阅，无需为例行可逆操作另行询问。

1. `K review --task "任务ID"` 返回研究正文、源码证据和 digest。逐项核对；证据被截断或还有材料缺口就补读/退回，不直接 accept。
2. 错误可 `K review --task "ID" --reject "研究digest" --notes "具体错误与复查位置"` 退回。
3. 核对后 `K review --task "ID" --accept "研究digest" --notes "真实核对说明"`。纯规划任务会接受盘点并生成有界后续任务。
4. 有知识单元时会返回**新的知识提案 digest**。阅读该次 units/evidence，再 `K review --task "ID" --accept "新digest" --notes "知识审阅说明"`，第二步才入库。
5. 当前会话就是作者时，两次决定都必须显式加 `--self-review`，保留 **self_reviewed**。不要改 worker/reviewer 名字假装独立审阅。另一会话可用自己的 session 初始化同一个 paths 后审阅指定 task；那是另一 AI 会话审阅，仍不等于人工专家审阅。
6. 被退回后 `K next` 读取 feedback；重新研究不能沿用旧 attempt 的阅读回执。

## 查看和使用

- `K wiki`：返回当前已审知识的 HTML、Markdown 和数据库路径。SQLite 是权威状态，Wiki 是其阅读视图；未审草稿不冒充 Wiki 知识。
- `K ask --role coding --question "修改这个机制还会影响谁？"`
- `K ask --role test_generation --question "边界、反例、测试预期依据和未覆盖分支是什么？"`
- `K ask --role review --question "这个改动需检查哪些前置条件、状态和资源清理？"`
- `K coverage --module "模块ID"`：显示真实未完成项；获取三个上下文不等于通过全仓覆盖验收。
- `K status` / `K plan`：会话状态与全仓计划。多人独立服务器仍使用已有签名材料包/结果包机制，按 [协作说明](../../docs/WHOLE-REPOSITORY.md) 导入，不共享/手工拼 SQLite。该入口首版绑定协调端 paths；已解开的成员包继续使用其既有 MCP/whole 入口，不对它重新 init。

最终用中文简要给出：模块与 task ID、实际提交/审阅模式、Wiki/结构化库/计划的真实绝对路径、重要结论及未知。如果只完成盘点就说盘点完成；如果没有入库就说待审；SQL、数据库、产品编译和故障注入保持未运行。
