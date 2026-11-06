---
name: source-view-learning
description: Learn database system views by tracing SQL definitions, function bindings, field producers, permissions, NULL behavior, snapshots and node scope. Use for view semantics and diagnostic query design.
---

# 系统视图专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/views.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

## 研究路径

1. 核对 schema、安装/升级定义、视图/表/函数、签名和构建可达性，区分本地、集群、实时、缓存和历史接口。
2. 从 SELECT 投影/过滤/连接/聚合追函数注册与 C/C++ 返回结构，核对 descriptor 序号、Datum、values/nulls 和 SRF 迭代。
3. 对相关字段建立状态值→变换→返回字段→SQL 表达式的血缘，逆查初始化、所有相关写入、刷新和重置。
4. 单独解释权限身份、行过滤、字段置空，区分 NULL、零、空串、unknown、无行和查询失败。
5. 查锁、序列计数、复制重试的真实一致性；单行、跨行、跨视图和跨节点分别判断；核对关联标识复用。
6. 从生产者设计对象出现/变化/退出、权限、开关和重置实验；查询代价会影响采样建议。

## 专业判断

wait_status 不能推出 duration，memory 不能推出 RSS，NULL/零不能自动解释成没有事件。SQL 定义存在也不证明目标构建安装了该接口。

## 依赖与交付

字段涉及等待、内存、解码或工具阶段时加载对应领域，把真实机制带回字段解释。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| definition_and_lineage | 定义/注册、SQL 变换、字段到状态读写的血缘 |
| visibility_and_consistency | 权限/置空、节点/缓存、快照/刷新/重置 |
| field_semantics | 类型/单位/时间、NULL/零/无行及使用限制 |

## 充分性挑战

解释相同查询在另一身份下怎样变化，以及相同显示值可能对应的两种真实状态。只研究部分字段时明确范围，未追写入者不能宣称整张视图完成。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.views；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
