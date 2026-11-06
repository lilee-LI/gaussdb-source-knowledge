# 格式化路径示例：token、文字与相近重载

这是方法示例，证据身份为 openGauss-server 提交 `aee4abd5a9ebd29ef6b8d410b8b353b2a4f7e106`。以下定位在该提交核对；换版本必须重新定位。这里的静态分析不表示已经运行 SQL，也没有证明 Oracle 侧行为。

## 研究问题

当格式串包含 X 时，能否只根据“兼容模式”解释结果？需要先区分实际调用的签名、格式 token 与被引号包围的文字，以及 token 的执行条件。

## 核对链条

| 证据位置 | 能支持的事实 | 不能据此扩大为 |
|---|---|---|
| `src/common/backend/catalog/builtin_funcs.ini` 的 to_char 注册 | `(1114,25)` 绑定 timestamp_to_char，`(1184,25)` 绑定 timestamptz_to_char；需检查注册的 strict/属性 | 所有同名重载共用相同语义 |
| `src/common/backend/utils/adt/formatting.cpp` 的关键字表 | 大写/小写 X 都有 DCH_X token 映射 | 引号文字也按 token 执行 |
| `parse_format` 的 action 与引号文字分支 | token 形成 action node；引号内文字形成 char node | 所有输入格式都合法或没有其他解析限制 |
| `DCH_to_char` 的 DCH_X 分支 | 此提交在 A_FORMAT 时写入小数点文字；需沿非该条件路径检查输出指针 | 所有模式都输出 X 或均与 Oracle 等价 |
| `timestamp_to_char` 与 `timestamptz_to_char` | 都进入 datetime_to_char_body；timestamp2tm 的时区参数不同，入口还有空格式/非有限值处理 | 时间类型互换后所有输出都相同 |
| `datetime_to_char_body` | 长格式与缓存路径都需要分析；缓存节点与实际 DCH 执行分别发生 | 有缓存就一定缓存了模式选择结果 |

可复查的行窗：注册约 12134–12142；formatting.cpp 关键字约 1311/1366，parse_format 2068–2150，DCH_X 3757–3766，datetime_to_char_body 4183–4249，两个入口 4260–4315。行号只作导航，提交、函数内容和文件哈希才约束证据。

## 从代码构造区分输入

以下仅为未执行的候选，不把静态预期当实际输出：

```sql
SELECT to_char(TIMESTAMP '2026-01-02 03:04:05', 'SSX');
SELECT to_char(TIMESTAMP '2026-01-02 03:04:05', 'SS"X"');
SELECT to_char(TIMESTAMP '2026-01-02 03:04:05', 'SSx');
```

第一与第二例区分 token 和文字；第一与第三例核对大小写 token 映射。再按研究目标加入显式 timestamptz、空格式、NULL、相关模式、缓存首轮/复用与长格式。模式切换能否在现有会话完成须先核对创建/设置方式，不能杜撰 SET 命令。

对未引号 X 的静态预测，应沿实际入口、节点类型和 DCH_X 两侧条件解释；对引号文字，应沿 char node 的输出路径解释。若只给出“X 受兼容模式控制”，就漏掉了文字分支。若只看 DCH_X，就漏掉了空格式入口和重载差异。

## 此例对错误学习的意义

同族函数的“格式不合法”“字段越界”“数值超范围”不能归并为一个原因。先核对报错点属于日期输出、日期解析还是数值格式实现，再逆查格式解析与类型转换。一个日期格式 token 的发现不能解释数值 to_char 的格式错误。

同一提交的 `timestamp_to_char`（4274–4275）和 `timestamptz_to_char`（4302–4303）都可能报告 `ERRCODE_DATETIME_VALUE_OUT_OF_RANGE` / `timestamp out of range`。错误文本与错误宏不能唯一定位入口：两个入口的 timestamp2tm 时区参数不同，而且检查发生在 datetime_to_char_body 之前。此前的空格式/非有限输入还可能直接返回 NULL。因此，看到这段错误不能直接建议改 X 格式或切兼容模式。

继续追 `src/common/backend/utils/adt/timestamp.cpp` 的 `timestamp2tm`（1763 起）：整数与浮点时间表示有各自路径；日数换算到 Julian date 后，在负值或大于 INT_MAX 时返回 -1（1795–1796、1814–1815）；tzp 为 NULL 会在 1835–1841 提前成功返回；有时区参数时还有时区处理。由此可以解释这两个报错点的检测条件，但尚不能证明某个 SQL 字面量一定能穿过类型输入/转换的更早检查，抵达这里。

这次错误研究的 required 依赖是 compatibility：签名、类型输入/转换、时间表示和时区。若要解释事务影响，再追 errors 的异常传播/清理；若只是解释此检测条件，可将工具、解码等标为本次路径范围外，附上直接 SQL 入口的范围依据。目标构建、可触发输入和实际复验仍是 unknown/not_run，不能用已有路径替代它们。

下一步的区分性材料应是：完整 SQL 与参数实际类型、目标构建、对应调用栈/检测点和相关时区状态。正常值与边界输入用于区分“输入阶段已拒绝”和“进入 to_char 后转换失败”；不能先假定现场触发了上述某一分支。

## 本地复查身份

本示例在 2026-10-20 直接读取上述提交的 Git blob，并复查注册、大小写 token、引号节点、char 输出、缓存/执行和错误路径。文件 SHA-256：

| 路径 | SHA-256 |
|---|---|
| `src/common/backend/catalog/builtin_funcs.ini` | `49de801a3dbae4691e51c594044bbe726846ed043c77816ec0efb3be01742ba1` |
| `src/common/backend/utils/adt/formatting.cpp` | `e374c97c74458617986dc071b73601bb2fa183850043cde1bae527c4a963f70d` |
| `src/common/backend/utils/adt/timestamp.cpp` | `96bcec6377ab4b988d3593562679f25e895084d2cf1b147fdd4c8a15b1e41ff5` |

该材料为作者自查的教学案例，未作为新 study 或已验证 Wiki 文章发布。

后续任务应分别处理：注册到目标构建的对应；每个输入的实际运行；目标产品版本侧的独立证据；其他格式 token/数值重载的族内覆盖。该例是有界路径演示，不是兼容性专题完成证明。
