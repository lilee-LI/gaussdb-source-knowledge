# geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期

openGauss · ed99bbde5308942d4eb062e7a851bdb85dda902f · declared-build

审阅状态 independent_review

## 测试目标
为 geqo_eval 建立可核对的结构性预期：每次评估创建/删除 "GEQO" 子内存上下文，join_rel_list 长度与 join_rel_hash 指针成对恢复，fitness 取自 cheapest_total_path 的 total_cost；同时明确异常路径和最终 gimme_tree 的不同处理。本义务不运行 SQL、编译、内存诊断或故障注入，execution_status=not_run。

## 正常路径预期
- 进入前记录 N = list_length(root->join_rel_list) 与 H = root->join_rel_hash；调用返回后两者必须分别等于 N 与 H。
- 评估期间 root->join_rel_level 保持 NULL（源码为 AssertEreport，断言构建才强制）。
- 每次调用创建一个名为 "GEQO" 的 AllocSet 子上下文并在返回前 MemoryContextDelete；连续多次评估不应使 planner 上下文内存线性增长（除池/染色体等 geqo() 自有对象外）。
- 返回值为 joinrel->cheapest_total_path 首元素的 total_cost；该 joinrel 由 gimme_tree 的 set_cheapest 填充。
- 需要观察 fitness 的用例应通过 kid->worth/spread_chroma 的副作用或调试构建断言验证，而不是把 joinrel/Path 指针带出函数（会悬空）。

## 异常与边界
- 在 gimme_tree 内构造 ereport(ERROR)（例如无法连接全部关系）时，list_truncate/hash 恢复和 MemoryContextDelete 都不会执行；join_rel_hash 保持 NULL，内存依赖 planner 父上下文在查询中止时回收。测试应确认失败查询可正常中止且不污染后续语句，而不是期望 geqo_eval 自己恢复。
- geqo() 收尾的最后一次 gimme_tree 不经过 geqo_eval：该 joinrel 必须保留在 planner 上下文；若测试观察到 best_rel 指针在返回后被释放，说明有人把最终构造错误地放入 GEQO 子上下文。
- join_rel_level 非 NULL 时断言构建应失败；非断言构建的行为未定义，不作为测试断言。
- cheapest_total_path 为 NIL 时 linitial 非法，但本 attempt 未发现可达路径，保留未知，不作为用例。

## 未运行与未知
- 未执行任何 SQL/EXPLAIN/内存上下文统计；"GEQO" 上下文是否可在现有诊断接口中观察未验证。
- list_truncate 返回值的分配上下文未读 list.cpp 验证：若 List 头分配在 GEQO 子上下文，恢复后的 root->join_rel_list 可能悬挂；这是需要优先核对的未决点。
- make_join_rel/set_cheapest 是否严格 append-only 未读其实现；测试只能以源码注释的假设为前提。

## 知识来源与版本

```json
{"binding":{"dependencies":[{"fingerprint":"a0724f9402efab40665c6013229bc340e47486c16ff409719ddd59f4853d7fd9","ref":"server/src/gausskernel/optimizer/geqo/geqo_eval.cpp","type":"asset"},{"fingerprint":"350b331042fe9bd35bcd8cdefb1c47ff72a336f16fd098dd4109caa6bc9c9a15","ref":"declared-build","type":"profile"}],"knowledge_dependencies":[{"fingerprint":"de1a460ae525d4ea0d745d98bb44ede064049f1050805645d75dac348fdb1593","ref":"claim:server/src/gausskernel/optimizer/geqo:geqo-eval-child-context-and-fitness"},{"fingerprint":"de1a460ae525d4ea0d745d98bb44ede064049f1050805645d75dac348fdb1593","ref":"claim:server/src/gausskernel/optimizer/geqo:geqo-eval-child-context-and-fitness"}],"methods_digest":"2105f393fcf2f9cbace8ed2a18c743a6932a2d1a904b3f45685af1889bdb508a","profile":"declared-build","run":"index:19d25bffc02c94f56c3add95c053d515","snapshot":"snapshot:e3c7591bc57779ef711950941aa64146"},"content_hash":"06535b0d27c9de84fae02681808adf6eb3aacb1ebfb762bf1f5c34e6a335e742","knowledge_id":"test_obligation:server/src/gausskernel/optimizer/geqo:geqo-eval-restore-and-error-path-cases","knowledge_revision":"knowledge:9e4ee092006998e86d257dfc0032055f","review":{"at":"2026-11-09T03:33:53.386006+00:00","mode":"independent_review","notes":"父会话已读 6 单元全文：mechanism 主循环、eval 子上下文/恢复、gimme_tree clump、构建/ERX 源码默认四类；两个 test_obligation 的 expected_from 指向真实 claim；operations 有条件、configuration 有生效点，unknown 保留 TU/运行时/未读实现。接受入库。","proposal":"proposal:d7e4b096457f0c5bf14fe03454f9b92b","proposal_digest":"4bcb03cb718ce4972b4a073187ecfd88b14f9d54a71472fd3abff4d9a9c2e291","reviewer":"claude-v24-native-parent","runtime_validation":"not_run","verdict":"accept"},"stale_reasons":[]}
```

## 适用条件

- 源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only，未运行 SQL/编译/故障注入
- 调用发生在 geqo() 运行期且 root->join_search_private 有效、root->join_rel_level 为 NULL
- CurrentMemoryContext 为 planner 上下文，GEQO 子上下文为其子级
- 测试只断言源码可推导的状态，不把 GEQO_DEBUG 日志或内存统计输出当作硬 oracle

## 边界与反例

- 最终一次 gimme_tree（best_rel）不经过 geqo_eval，不能要求其 RelOptInfo 随 GEQO 子上下文回收
- gimme_tree 内 ereport(ERROR) 时恢复语句不执行，不能断言 join_rel_hash 已恢复
- 非断言构建中 join_rel_level 检查可能不生效，不能以断言行为约束所有构建
- GEQO 不支持部分结果检索（源码 XXX），不能把 cursor 场景的最优计划作为预期

## 测试预期来源

- {"kind":"claim","ref":"claim:server/src/gausskernel/optimizer/geqo:geqo-eval-child-context-and-fitness"}

## 执行状态

- not_run

## 证据

- [server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:1-200](../evidence/763ef0ffb4a7fa4ce623de3b.html)

## 相关知识

- [DEPENDS_ON · geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](503935492fb1cab9eea7288e.md)
- [REQUIRES_TEST · geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](503935492fb1cab9eea7288e.md)
- [测试预期依据 · geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](503935492fb1cab9eea7288e.md)
