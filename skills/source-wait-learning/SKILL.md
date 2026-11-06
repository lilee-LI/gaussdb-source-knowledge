---
name: source-wait-learning
description: Learn database wait events and elapsed-time analysis from source through queue and state transitions, wakeup, cancellation, clocks, counters and observation boundaries. Use for wait research or timing dependencies in diagnosis.
---

# 等待事件与耗时分析专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/waits.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

## 研究路径

1. 从枚举、上报调用和用户入口建立候选，区分等待对象、观测状态、真实阻塞与累计统计。
2. 追前置快路径、入队、状态/开始时间写入、释放保护锁、sleep 循环、唤醒者、重试、授予和退出；核对虚假唤醒。
3. 查旧状态保存/恢复、嵌套和线程/会话/线程池归属；分别读正常、取消、超时、死锁、ERROR 与退出的队列和状态清理。
4. 每个时间/计数追到时钟、单位、delta 公式、精度/最小值处理、主体、开关、重置和并发读取；当前、单次、累计、阈值分别解释。
5. 外部观测追到快照和字段生产者；不能根据事件名杜撰持续时间列或阻塞者身份。
6. 用无竞争、可控等待、释放和取消设计时间线实验，注明参与者身份、采样间隔与开关；漏采短事件不能证明没有等待。

## 专业判断

超时阈值、死锁检测周期、语句时间和等待计时可能有不同起点。增大超时不证明竞争消除；累计差分需主体和重置周期一致。

## 依赖与交付

观测加载 views，超时与取消错误加载 errors，复制/解码等待加载 decoding，资源压力关联 memory。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| state_lifecycle | 资源/队列、状态迁移、唤醒与正常异常出口 |
| timing_and_scope | 时钟/单位/公式、开关、主体、累计与重置 |
| cancellation_and_observation | 取消清理、字段来源、采样边界与区分实验 |

## 充分性挑战

选择相关的无竞争、虚假唤醒、取消或统计关闭路径，解释原结论怎样变化。唤醒者或计时终点未读到就保留缺口；事件清单完整不代表机制已完成。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.waits；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
