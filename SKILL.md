---
name: database-source-knowledge
description: Learn a version-bound database source module from a completed ECS index, frozen documents and code. Submit evidence-backed findings for central review.
---

# 数据库源码学习 · ECS 版

研究协议采用 `unified-skill/v1`。ECS 使用仓内 `ecs.sh capture/build` 从真实构建生成交付图，协调端通过 `kb.cmd` 回放。部署和证据边界见[技术设计](docs/DESIGN.md)。

协调端从 `kb.cmd check` 和 `start` 得到计划，`learn` 返回一个研究 ID、MCP 配置和提示词。学习库持有已审知识与证据，读取 `index_db` 中的关系。提交测试依据时 `expected_from` 使用单个对象，例如 `{"kind":"contract","ref":"contract:example"}`；`finish_research` 成功后向审阅人传回任务 ID。人读的 HTML 与 Markdown 由 `wiki` 从已审修订生成。

从当前工作单读取 `worker`、模块、学习快照和 ECS run。执行 `study_plan` 查看完整源码范围与实际图覆盖，调用 `feature_candidates` 分页查看候选、责任模块、证据和状态。用 `focus_module(candidate_id=…)` 指定一项候选，或选择模块和具体问题。工作包包含模块、一跳依赖和分派候选引用的材料。需要额外资料时，把缺少的资产键交给协调端。

全仓先盘点每个模块的用户可观察特性，留下入口和缺口。一个研究任务回答一个行为与相关契约。沿调用图按证据需要展开，同一问题可跨多个函数和模块。已有旧队列时按 [操作手册](INTERNAL.md) 在协调端切换。使用任务上下文的 `previous_research`，区分已接受、待审及派单时的历史索引。

在 `claim_task` 后读取 `task_context`，通过 `create_task_evidence` 创建准确的行区间，用 `read_task_evidence` 在同一租约下实际读完。沿 `navigate_code`、`query_graph` 的入边和出边检查生产者、消费者、共享状态和宏条件。对于虚调用、函数指针、注册表或仅有候选绑定的边，在源码定位注册点、分发点和具体消费者。保留未验证的路径和配置空白。

按需使用包内 repository、memory、compatibility、GUC、wait、view、tool、decoding 专题及错误研究方法。每项行为写清适用构建、证据、反例、开发影响、测试预期来源及 review 要检查的边界。没有设计文档的特性可由注册入口、实现和测试建立候选，并标记设计缺口。

使用 `stage_research_unit` 和 `finish_research` 提交任务，返回任务 ID 供成员 `team export`。协调端核对证据后接受任务和知识提案。开发、测试和评审使用 `get_context` 查询已接受知识。详见 [内网操作手册](INTERNAL.md)。
