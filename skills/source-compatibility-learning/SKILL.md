---
name: source-compatibility-learning
description: Learn database compatibility semantics from bound source through SQL binding, coercion, configuration branches, function families and counterexamples. Use for compatibility research and dependencies in errors or migration.
---

# 兼容语义专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/compatibility.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

全景盘点按需读[语义覆盖矩阵](../../references/domains/compatibility-map.md)，格式化问题按需读[路径示例](../../references/domains/compatibility-formatting-case.md)；示例只作方法参考。

## 研究路径

1. 从语法或内置/扩展注册确认入口和精确签名；追名称解析、重载选择、unknown 字面量、隐式/显式转换和默认参数。测试专用 catalog 不能作为目标构建注册证明。
2. 读取前置处理和核心算法：strict/NULL、类型表示、精度/标度、编码/时区、格式解析与执行、舍入/溢出；按本题展开相关维度。
3. 核对模式、配置、构建、插件和版本的组合条件，包括不等式、switch、宏与默认路径；从用户入口正向追踪，避免只搜索兼容关键字。
4. 分开解释解析、缓存构建、执行、输出和报错阶段；查缓存键、失效以及哪些选择固化、哪些条件每次读取。
5. 生成输入域→绑定→条件→规则→结果/错误的决策表，用最近重载、边界、引号文字及单条件变化构造反例。
6. 目标产品等价结论需要独立的版本、文档或运行证据；静态预期、本地实测和目标侧结果分别记账。

## 专业判断

“支持函数”“兼容模式”“存在分支”不是完整语义。日期函数不代表数值同名函数；缓存存在不证明模式选择被缓存；改写或切换模式要解释语义变化。

## 依赖与交付

错误检测加载 errors，工具输入/生成 SQL 加载 tools，DDL/事务的等待与观测加载 waits/views，缓存对象生命周期相关时加载 memory。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| inputs_and_binding | 输入/签名、入口与绑定、转换和环境 |
| conditions_and_branches | 决策规则、配置/构建/插件、生效阶段与替代路径 |
| behavior_and_counterexamples | 正反例、错误边界、静态/实测/目标侧证据和缺口 |

## 充分性挑战

让规则解释一个未照抄的近邻 SQL：绑定哪个入口，哪条条件决定结果，怎样进入最近错误分支？无法解释的部分给出具体缺口。单路径、函数族、整个领域覆盖分别判断。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.compatibility；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
