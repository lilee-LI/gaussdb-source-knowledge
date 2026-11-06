---
name: source-tool-learning
description: Learn database import and export tools from source through real binaries, option interactions, SQL and data stages, snapshots, transactions, parallelism and failure recovery. Use for tool research and loader or migration diagnosis.
---

# 外围工具专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/tools.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

## 研究路径

1. 查构建/安装/包装脚本、实际版本、客户端库和两端模式；源目录、主函数和用户命令名分别核对。
2. 从选项解析追字段、默认/重复覆盖、互斥/依赖、标准化与所有读取者，建立参数决策表并确认错误检查顺序。
3. 追连接探测、对象选择、元数据/数据读取、输出归档、建对象/装数据/后处理、worker 汇总和结束，分别画格式与阶段数据流。
4. 读 SQL 生成执行、快照建立/共享、事务提交、对象依赖排序和并行屏障；核对权限、编码、NULL/quote/escape 与类型输入。
5. 按失败阶段列残留文件/对象/行、提交情况和自动清理；确认真实 checkpoint、重试能力与幂等前提。
6. 设计合法基线、最近非法组合、坏对象/行、中断和重试；核验相关对象定义、数据、约束/序列/权限，不能只看退出码。

## 专业判断

客户端参数错误、服务器 SQL 错误、文件/worker/网络错误与外层脚本退出分别定位。dump 成功、restore 成功和迁移等价分别判断；不能从残留日志推断支持续传。

## 依赖与交付

类型/模式加载 compatibility，报错传播加载 errors，批量内存加载 memory，阻塞和统计加载 waits/views。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| options_and_stages | 实际入口、参数决策、SQL/数据流与阶段 |
| consistency_and_dependencies | 快照/事务/对象依赖/并行和数据语义 |
| failure_and_verification | 阶段残留、重试前提、结果核验与未测项 |

## 充分性挑战

同一错误发生在参数校验前或部分对象提交后，恢复建议是否仍成立？源/目标模式变化影响哪段语义？未读提交/清理路径就保留缺口。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.tools；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
