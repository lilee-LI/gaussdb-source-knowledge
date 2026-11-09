# 内网协调与多人操作

本页保留旧 ECS/MCP 操作细节。**2.4 推荐流程及完整命令以 [迁移手册](MIGRATE-GAUSSDB.md) 和 [当前 Claude 入口](CLAUDE-START.md) 为准**：四输入可先规划、选模块、原生子 Agent 学习与中央汇总，不必先产全仓图。

## ECS 首次产图

在产品构建机按[从源码产图的操作](CALLGRAPH-REPLAY.md)生成交付目录，把整个目录复制给协调端。Windows 的 `index_db` 填其中的 `knowledge.sqlite3`。

## 协调端

创建 `local/paths.json`，填写 `source`、`home` 和 `index_db`，可选 `design`、`manual`、`run_id`。默认只读引用交付图，`home` 保存学习状态及冻结材料，两个路径应分离。多源码仓以 `repository_roots` 补齐其他仓库 ID 的本地路径。`module_prefixes` 可列仓库 ID 开头的资产前缀，最长前缀优先。

~~~powershell
.\kb.cmd check
.\kb.cmd start
.\kb.cmd features --state needs_owner
.\kb.cmd route --candidate <ID> --module <完整模块名>
.\kb.cmd --home E:/kb/hub team assign --module <完整模块名> --worker opt-a --kit E:/share/opt.zip
~~~

`start` 返回计划文件。模块源码范围来自完整检出，上游涉及的 TU 和仍未覆盖的文件单独记账。缺少上游归档原文时提供同版本源码或上游 `blobs`。缺少设计时仍可核对注册入口、SQL 回归脚本和源码；历史设计意图保留为未知。

当前分派单位是模块，一份工作单可持续交回多个原生任务结果包。协调端审阅后 advance 并 feedback，成员 sync 后继续。只有变更负责人或输入范围才明确重签，不能为了每个任务另建工作单。有活动租约或已审成果时先核对冲突，不覆盖结果。

## 成员与协调端交接

~~~powershell
.\kb.cmd --home E:/kb/member-a team open --kit E:/share/opt.zip
claude --mcp-config E:/kb/member-a/worker.mcp.json
~~~

成员指令示例：

> 以工作单上的身份调用 feature_candidates，选择分配给本模块的候选，用 focus_module 指定 candidate_id 创建任务。领取租约，通过 task_context 和 read_task_evidence 核对文件行号、构建条件、跨模块消费者和测试依据。提交后返回任务 ID 和仍缺的证据。

~~~powershell
.\kb.cmd --home E:/kb/member-a team export --task <任务ID> --out E:/share/opt.result.gz
.\kb.cmd --home E:/kb/hub team receive --input E:/share/opt.result.gz
~~~

`team receive` 检查来源、工作单与证据。用返回的协调端任务 ID 在协调端 `review`；结果包重复传入会复用回执。超过模块一跳范围时，协调端可用 `navigate` 核对全图，通过 `team assign --help` 中的补充资产选项按需重发。上游图只读，研究工作在成员本机的独立数据库完成。

## 旧队列和版本更新

已有约 22 万项旧任务时，先在原学习工作区运行只读预览。`--home` 指向原学习库，不要填 ECS 交付目录。

~~~powershell
.\kb.cmd --home E:/kb/old-learning plan --preview
.\kb.cmd --home E:/kb/old-learning plan --run <原学习run> --granularity module --preview
.\kb.cmd --home E:/kb/old-learning plan --run <原学习run> --granularity module
~~~

确认预览后，最后一条按模块规划。正在处理的工作及其依赖、已提交和已审的研究保留。符合条件且尚未领取的细任务可延后。已有 1.5 学习数据先备份，使用 2.0 和原路径配置重新运行 `start`，用 `features` 查看新版计划。新材料快照需重新核对旧结论。

源码或文档换版时执行 `start --refresh`。待分析的 ECS 构建改变时由上游交付对应 run。底层 `change` 需要显式给出可共同查询的两组快照/run；跨独立工作区不能直接用两个 ID 做比较。日常分发使用 `wiki` 返回的整个阅读目录；`publish` 面向完整归档，会复制图、学习库及证据。
