# 兼容性全景与覆盖台账

此版图用于排课和查缺，不是已经实现或验证的功能清单。每项都要在选定产品/提交中识别真实对象。某版本不存在的能力，需区分未实现、被构建排除、插件提供、入口不同和仅本次未发现。

| 主题 | 需要识别的规则族 | 重点入口与交叉关系 |
|---|---|---|
| 语法和名称 | 关键字、标识符大小写/引用、限定名、同义词、运算符、特殊语法 | lexer/grammar、parse tree、namespace、catalog、权限 |
| 类型绑定 | unknown、重载优先级、隐式/显式转换、domain/typmod、公共类型 | parser、cast catalog、coercion、函数/操作符注册 |
| 数值 | 精度标度、溢出、舍入、整数/浮点、格式化与解析 | 输入函数、中间表示、算法、错误检查 |
| 字符 | NULL/空串/空格、长度单位、截断、编码、拼接、比较/排序 | 类型实现、collation、编码转换、会话设置 |
| 日期时间 | date/timestamp/timestamptz/interval、时区、历法、截断、格式 token | 类型转换、格式解析/执行、timezone、缓存 |
| 条件和集合 | NULL 三值逻辑、比较、CASE、集合/聚合、排序去重 | 绑定、执行算子、优化重写、排序/哈希 |
| DDL 和事务 | 对象属性、默认值、约束、序列、锁、提交与异常回滚 | catalog、utility、事务、资源清理 |
| PL 与异常 | 变量绑定、参数模式、游标、动态 SQL、异常传播 | PL 编译/执行、SPI、错误上下文、子事务 |
| 外部交互 | 工具生成 SQL、文本/二进制输入、协议类型、驱动映射 | tools、COPY/输入函数、客户端显示 |

沿主题 → 规则族 → 签名/对象 → 分支 → 场景组织台账。每行使用以下字段：

```text
topic / rule_id / object_signature / source_snapshot
entry_binding / relevant_conditions / decision_rule
positive_case / nearest_counterexample / error_boundary
local_source_evidence / target_product_evidence
source_analysis_status / local_runtime_status / comparison_status
known_gaps / next_study / reusable_knowledge_refs
```

状态建议：unmapped、candidate、path_traced、rule_explained、runtime_checked、comparison_checked。它们分别说明完成了什么，不能仅因后一步有一个成功例，就认为前面所有对象都已覆盖。缺失值保留 unknown。

对每个函数族采用不同轮次：

1. 梳理签名与共享实现，按输入域选择代表对象。
2. 抽取已读实现的决策规则，读替代分支、错误与清理路径。
3. 补最容易误判的重载、转换、边界和状态反例。
4. 运行必要实验并回灌差异；重新定位差异所在阶段。
5. 用未参与撰写的近邻案例检验规则能否解释新行为；有条件时再做真实独立复核。

一轮完成的判据是增加了有证据的新规则、关闭了明确缺口或推翻了旧解释。族内仍有未映射签名、未读实现、未覆盖条件或对照缺口，就在族索引保留它们。禁止用“100 条 SQL 全过”代替具体覆盖关系。

不要求每个专题把全景重新执行。研究日期格式 token 时，可以把 PL 标为本任务范围外；但如果建议导入工具改写日期格式，就要加载工具阶段和输入函数的依赖研究。
