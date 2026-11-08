# 2.3.1 当前 Claude 会话入口验证

日期：2026-11-08。本次新增 `/gauss-knowledge` 与直接粘贴提示词入口；知识、证据、任务、审阅与覆盖仍使用 2.3 的原生协议。新入口不调用 `kb run`、Claude CLI、模型 SDK 或模型 HTTP。它通过当前会话的本地工具操作 Python 助手，不要求先接 MCP。

## 实现边界

| 层 | 本次实现 |
| --- | --- |
| 项目 skill | `.claude/skills/gauss-knowledge/SKILL.md`，Claude 从工程目录发现 |
| 通用 skill | `skills/gauss-knowledge/SKILL.md` 与按需加载的格式说明；支持直接读文件执行 |
| 个人安装入口 | `scripts/install_claude_skill.py`，只生成指向工程的 loader，不改模型、权限、认证 |
| 当前会话助手 | `scripts/claude_session.py` / `unified_knowledge.assistant_session`，复用 project/whole/planner/knowledge/retrieval |
| 初始化 | 源码和可选手册/设计；无图时 source_only，不解析 TU，不构造全仓调用图 |
| 审阅 | 默认提交待审；明确要求审阅时，两步真实决定，同作者保留 self_reviewed |
| 协作 | 本入口绑定路径配置的协调端工作区；已解开的成员材料包沿用既有 MCP/whole 协议 |

原生 `finish_research` 的历史 `capture=mcp_staged_units` 标记继续表示原有分项暂存协议，不表示该入口启动了 MCP。新入口另记 `assistant_session_submit` 事件和当前 session，保留真实执行来源。

## 软件回归

全量 **72 项测试通过，158.353 秒**。新增当前会话专项 6 项通过；此后修正 Windows UTF-8 输出、bootstrap 子进程编码与提示文字，专项再次通过。新增检查包括：

- 仅源码与手册初始化、生成计划、读取手册材料；输入与工作区重叠拒绝。
- 同会话有效租约恢复；过期增加 attempt 并重新阅读；不能窃取另一活动 token。
- 搜索命中不能冒充阅读；无图时拒绝虚构 symbol、contract、call step。
- 未审研究不进入 Wiki；研究/知识 digest 分离；自审必须显式且按 self_reviewed 保存。
- 原生 Wiki、三类实际知识检索、纯规划审阅后生成有界机制任务。
- 个人 loader 幂等、保护已有不同 skill 与无关设置；非 UTF-8 环境下 JSON 仍输出 UTF-8。

复现命令：

```text
.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -v
.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p test_assistant_session.py -v
```

这是软件协议验证，不等于产品语义准确率或数据库测试。

## 真实 Claude Code 试跑

在 Windows 原生 Claude Code 2.1.310 中直接以 `/gauss-knowledge` 进入，使用其正常 Read/Write/Bash 工具；未配置研究 MCP。试验启动的这个 Claude 是评测宿主，工程助手没有再启动任何 Claude。

实际模型沿用本机配置，报告 `deepseek-v4.1-flash[1m]`，没有改成 Anthropic 模型。合成材料为一个 3 行 C++ 函数与 2 行用户手册。**122.296 秒**完成：

1. 自动创建 source_only 工作区，生成全仓计划，2 个材料模块、24 个初始任务；公共主题仍有待判定范围。
2. 当前会话实际读冻结方法、C++ 与手册，取得阅读回执。
3. 提交模块盘点、1 个机制提案、真实缺口；知识正文 0 项，任务 submitted，未批准。
4. 无权限拒绝，未建立符号/调用图，未编译、运行数据库或 SQL。

该模型把手册的“适用于结果可表示的输入”过度解释成可能缺少防御检查的文码张力。试验结果仍是待审规划，未作为产品结论入库。skill 已补充区分**调用方前置条件**与**承诺的防御检查**，说明真实语义审阅仍有必要。

## 两项有无 skill 的工作流对照

两个隔离 Codex 评测代理分别使用新 skill 或仅查现有 README/原生 API。每项仅运行一次，计时由代理记录，未提供可靠 token 计数；不能据此宣称模型质量或稳定提速。

| 合成场景 | 使用 skill | 不使用 skill | 原生状态检查 |
| --- | ---: | ---: | --- |
| 源码/手册盘点并提交 | 265.590 秒 | 294.539 秒 | 两者 5/5：计划、待审、两种阅读证据、有界提案、无图 |
| 作者自审、入库、Wiki、三角色查询 | 105.860 秒 | 126.029 秒 | 两者 5/5：两步审阅、真实自审模式、Wiki 修订、实际检索、not_run |

基线也完成任务，但需要检查 API 并编写临时包装脚本。新入口的目标是提供固定、可复用的操作协议，不以小样本计时证明优于基线的推理能力。

第二项的初始待审结论由合成软件夹具生成，两个代理实际阅读内容与证据后，以明确的同作者 session 完成 self_reviewed 审阅。三种检索都返回已审 `claim:review-fixture:cost`，状态如实为 **partial**（profile_unknown / index_partial），不冒充编译确认或人工专家审阅。

本机详细记录与可交互静态评测页保存在 `local/skill-evals/iteration-1/`；它们不随公开代码包分发。可查看的正式使用说明为 [CLAUDE-START.md](../CLAUDE-START.md)。

## 迁移冷启动

把 working-tree 候选 ZIP 解压到新的中文路径、没有 `.venv` 的目录，用系统 CPython 3.12 调用当前会话助手。故意设置 `PYTHONIOENCODING=cp1252`，检验中文路径/手册在旧编码环境中能否工作。

首轮发现 bootstrap 子进程继承旧编码，安装报告输出失败；已将安装和 Python 重执行子进程显式设为 UTF-8。新目录重新冷启动 **25.140 秒通过**：

- 使用包内锁定 wheels 与 pip `--no-index --require-hashes`，创建全新虚拟环境；未向包索引取依赖。
- 初始化 stdout 是一个可解析 JSON，安装诊断留在 stderr。
- 原生 source_only 计划生成；项目 skill 在包中；隔离个人 loader 正确指向新安装路径。
- 安装后仍通过发行清单校验，未触碰本机 Claude 模型/认证或个人配置。

公开发行包最终从已提交 Git 索引构建并附带清单与 SHA256。完整包不包含 Claude 客户端、认证、会话日志、用户源码、测试工作区或全仓调用图。Linux 冷启动未在本次另测；工程现有跨平台 Python 与 shell 入口保持原协议。
