# 源码版本、共享证据和知识适用范围

完整错误学习采用版本化证据。源码本体保存在独立证据仓；Wiki 讲原理、根因、场景判别与条件方案。全文源码、长窗口和重复的 JSON quote 不进入日常 Markdown 或常规知识检索。减少展示不减少阅读：函数、调用者、写者、宏和清理仍按因果与适用性规程追踪。

## 两类身份分别绑定

- **源码身份**：product、repository_id、完整提交或受控快照、补丁清单。Git 捕获从指定提交读取原始 blob，不读取浮动工作树。没有 Git 或研究未提交补丁时，用 bind-snapshot 捕获实际文件，记录声明版本和补丁内容哈希；这种绑定证明所提供字节，不认证厂商版本或完整产品。
- **构建与执行上下文**：沿用产品档案与 applicability.json。宏、生成头、实际参数、集中式/分布式、节点角色和连接来源独立记录；同一提交的源码绑定不等于目标构建确认。

source_id 表示源码来源身份，binding_id 还绑定此次选择的文件清单。Git 同一提交不同选择范围可有相同 source_id、不同 binding_id。受控快照将所提供文件字节纳入 source_id，不能仅靠一个版本名称建立身份。所有清单明确 selected_files_only，不冒充整仓快照。

## 一份源码，多处引用

使用 [versioned_evidence.py](../scripts/versioned_evidence.py)，Python 3.10+ 标准库，无网络和数据库依赖。证据仓布局为 objects/sha256/内容哈希.source 和 bindings/绑定ID.json。同字节文件跨错误码、跨版本共用；文件和绑定不可静默覆盖。增量补文件产生新绑定，旧清单和引用保持有效。

证据采用 source-evidence/v2：每个条目记录 E-ID、身份、相对源码 path、整文件哈希、含尾行号、片段哈希及用途，不再内嵌 quote。多条重叠范围只保存定位，不复制源代码。证据索引链接到共享源码对象，正文引用稳定锚点。按需 show 时检查整文件和片段哈希，再返回原文。

Wiki 中只有当代码有助于解释谓词、状态顺序或分支差异时才放短片段，通常 5—20 行。范围是写作参考，不是强制截断规则；前置护栏、宏和异常边界不能因为片段变短而消失。长链用文字/流程图表达，每一步可回溯证据。source-evidence.md 作为紧凑定位索引；完整源码留在授权证据仓，不在 Skill 方法包中。

## 可以直接使用的操作

paths.json 为需要冻结的相对文件路径数组；不要把个人机器路径写进研究清单。

```text
python scripts/versioned_evidence.py bind-git --store STORE --source SOURCE_REPOSITORY --revision FULL_COMMIT --product GaussDB --repository-id INTERNAL_REPOSITORY_ID --paths paths.json
python scripts/versioned_evidence.py bind-snapshot --store STORE --source SOURCE_DIRECTORY --revision DECLARED_REVISION --product GaussDB --repository-id INTERNAL_REPOSITORY_ID --paths paths.json --patches patches.json
python scripts/versioned_evidence.py profile --store STORE --binding BINDING_ID --profile FILLED_PROFILE.json --output BOUND_PROFILE.json
python scripts/versioned_evidence.py cite --store STORE --binding BINDING_ID --id E-001 --path src/example.cpp --start 10 --end 24 --purpose "支持的具体结论或阅读义务"
python scripts/versioned_evidence.py verify --store STORE --profile BOUND_PROFILE.json --evidence evidence.json
python scripts/versioned_evidence.py show --store STORE --evidence evidence.json --id E-001
python scripts/versioned_evidence.py scope --store STORE --profile BOUND_PROFILE.json --evidence evidence.json --ledger applicability.json --scope knowledge-scope.json
python scripts/versioned_evidence.py index --store STORE --profile BOUND_PROFILE.json --evidence evidence.json --store-link RELATIVE_STORE_PATH --output source-evidence.md
```

Git 和快照方式二选一。patches.json 为含 id、sha256 的数组，补丁原件由环境另行保管；捕获文件本身含应用后的实际字节。profile 中 product/revision 必须与捕获结果一致，模板填完才能绑定。cite 输出一个条目，将它加入 templates/evidence.json 的 evidence 数组，顶层身份取自绑定产品档案。完整研究结果中保留实际自查，不把工具通过称为语义或运行验证。

## 知识精确声明适用范围

knowledge-source-scope/v1 每份文档只声明一个已复核的源码绑定。claims 记录可读结论、证据 ID、相关依赖文件、variant_ids、条件和 claim_kind；review 记录实际审阅者、日期、发现。可执行路径结论不能引用 unknown/infeasible 的构建为可用范围；构建拒绝等事实使用 build_fact。

同一页可展示多个已复核版本，但每个版本各自有 scope 和证据集；不得填写“某版本及以后”代替绑定。未提供/未读的新版本保持 unreviewed。只有源码条件已闭合才提供局部方案，原有 open/infeasible 不因证据去重而变更。

```text
python scripts/versioned_evidence.py compare --store STORE --old OLD_BINDING --new NEW_BINDING --scope OLD_KNOWLEDGE_SCOPE.json
```

compare 读取清单并产生增量复学候选：依赖变更/未捕获或产品不同标 requires_review；已列依赖字节未变也只标 candidate_unchanged，所有新版本适用状态仍为 unreviewed。它不检查 C/C++ 调用图，也不证明新增调用者、外部头、宏配置或构建语义等价。研究者必须检查检测点、生产者、调用者、类型布局、参数、生成头和清理的相关变化，再写新版本 scope。未在新清单出现的文件只表示未捕获，不能断言产品删掉了它。

## 主工程和历史材料

主工程 objects 快照已经按文件哈希保存冻结字节，并将 product/revision/清单纳入 snapshot_id；其证据锚点也支持 quote_sha256。新的完整错误任务给出紧凑锚点，历史 quote 凭据继续按原规则验证。原有知识绑定 task、snapshot 和 variant；跨版本复学工具和独立包使用上述显式清单，不能用一个模型/平台名替代绑定。

历史冻结文档不就地删源码、改编号或刷新哈希；另建新版。旧证据可在逐字检查后转换为 v2，保留来源版本和迁移记录。方法包只打包 Skill、文档、模板和工具；研究成果可另带共享证据仓供离线追溯。正常查询只加载 wiki 正文及索引，按需查研究/源码，不把 objects 或证据索引当知识文章灌入。
