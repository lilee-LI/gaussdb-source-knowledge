# L4 责任：clump 启发式合并与强制兜底

openGauss · content-addressed · linux-native

审阅状态 依赖已变化，待复核

L4 clump 合并责任：gimme_tree 按 tour 逐个取 initial_rels 的第 (gene-1) 个元素（1-based 映射），先做成 size=1 的 clump，再用 merge_clump(force=false) 合并。desirable_join 只在 have_relevant_joinclause 或 have_join_order_restriction 为真时允许合并，否则新 clump 按 size 降序插入。扫完 tour 后若还有多个 clump，则以 force=true 再逐个合并；force 只放宽“想不想连”的启发式，仍要 make_join_rel 返回非 NULL 且 set_cheapest 成功才算合法。最终 clump 数不为 1 时报 ERRCODE_OPTIMIZER_INCONSISTENT_STATE "failed to join all relations together"。
L4 · 上级 [L3 责任：GEQO 近似连接搜索总体](9ec835f6815b6d9e5dd3881d.md)

## 适用条件

- tour 元素必须在 1..num_gene，list_nth 用 gene-1

## 边界与反例

- force=true 不会绕过 make_join_rel 的合法性检查，笛卡尔连接也仍需合法 joinrel

## 证据

- [server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:138-200](../evidence/ca1406b9c729798eff53e486.html)
- [server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:210-296](../evidence/f32b6dcb0d7c49fb96b95453.html)

## 相关知识

- [REFINES · L3 责任：GEQO 近似连接搜索总体](9ec835f6815b6d9e5dd3881d.md)
