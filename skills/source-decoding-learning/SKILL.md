---
name: source-decoding-learning
description: Learn database logical decoding through WAL, snapshots, transaction state, reorder buffers, plugins, slot positions, feedback, retention and restart. Use for decoding semantics, lag and resource analysis or recovery dependencies.
---

# 逻辑解码专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/decoding.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

## 研究路径

1. 区分 SQL/复制协议入口、物理/逻辑、插件输出、发送、接收、反馈与下游持久化，为已消费标明层次。
2. 追 slot 创建/获取/释放、占用互斥、数据库限制、保存/恢复；读请求起点怎样转成 WAL 读取起点和输出边界。
3. 追快照构造、一致点、catalog 可见性和 xmin，追事务/子事务归属、提交/回滚、重排、spill/恢复和清理。
4. 对实际插件读装载/startup/事务/change/commit 回调、过滤、输出和错误；通用框架不代表所有插件具有相同语义。
5. 每个位点记录生产者、推进条件、锁、内存/持久值、保存/恢复、用途与接口；restart、confirmed、发送与下游提交不得合并。
6. 分别追长事务、积压、WAL/catalog 保留、重排内存和 spill 的约束，按受控中断与重启设计重复/遗漏验证。

## 专业判断

LSN 差不是业务记录数或时间延迟；确认推进不证明下游持久化或旧 WAL 立即释放。exactly-once 需要消费端证据；重建 slot 必须说明一致基线、重复和遗漏。

## 依赖与交付

重排增长加载 memory，读写等待加载 waits，slot/延迟观测加载 views，插件/位点报错加载 errors。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| transaction_and_snapshot | 事务可见性/重排/插件、提交回滚与替代路径 |
| positions_and_confirmation | 逐位点账本、反馈/推进/保存/恢复与确认层次 |
| resources_and_restart | 保留约束、资源生命周期、异常和重启验证边界 |

## 充分性挑战

读取起点为何可能早于输出起点，确认很新为何资源仍保留，下游接收未提交时恢复会怎样？选择相关问题解释，未读反馈/持久化/消费端事务就保留保证的缺口。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.decoding；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
