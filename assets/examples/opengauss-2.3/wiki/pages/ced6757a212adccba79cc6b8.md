# L4 特性：clump 合并与终态计划重建

openGauss · content-addressed · linux-native

审阅状态 依赖已变化，待复核

L4 特性：最终 gimme_tree/clump 重建。gimme_tree 把 tour 当作“建议顺序”，不是硬约束：它维护一个按 size 降序的 clump 列表，新关系先做成 size=1 的 clump，再用 merge_clump(force=false) 尝试与第一个能 desirable 合并的 clump 合并；合并成功就递归再试，直到不能合并再按 size 插回（size==1 的 clump 直接追加尾部）。desirable_join 的条件是 have_relevant_joinclause 或 have_join_order_restriction。扫描完后若 clump 仍多于 1，用 force=true 再合并；force 只跳过 desirable 判断，make_join_rel 仍决定合法性。最终必须恰好 1 个 clump，否则 ereport(ERROR) failed to join all relations together（ERRCODE_OPTIMIZER_INCONSISTENT_STATE）。这样既能产生 bushy 计划，也保证连接顺序限制下仍有合法解。
L4 · 上级 [L3 特性：GEQO 可观察能力](6dc89cbbd38bf88b53c52e95.md)

## 适用条件

- clump 列表按 size 降序维护
- force 合并仍调用 make_join_rel 与 set_cheapest

## 边界与反例

- 不能把 gimme_tree 说成总是左深树；clump 机制会推迟非法/不划算的连接

## 证据

- [server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:138-200](../evidence/ca1406b9c729798eff53e486.html)
- [server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:210-296](../evidence/f32b6dcb0d7c49fb96b95453.html)
- [server/src/gausskernel/optimizer/geqo/geqo_main.cpp:228-262](../evidence/ce48555e224ac59e8d9c772a.html)

## 相关知识

- [REFINES · L3 特性：GEQO 可观察能力](6dc89cbbd38bf88b53c52e95.md)
- [DEPENDS_ON · L4 责任：clump 启发式合并与强制兜底](d0be0bdcb5deebd473915ce5.md)
