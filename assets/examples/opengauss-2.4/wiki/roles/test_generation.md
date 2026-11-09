# 测试生成知识视图

修订 knowledge:9e4ee092006998e86d257dfc0032055f

状态 partial

## 实现行为与入口

[源码层 ERX 由 geqo.h 无条件定义，geqo() 的交叉分支恒走 ERX](../pages/7edbf06c7441fff5fbd7dfb9.md) · statement

```json
"在源码层，server/src/include/optimizer/geqo.h 在 include guard 内、任何条件编译之外无条件 #define ERX（第 30 行）。geqo_main.cpp 第 31 行包含 optimizer/geqo_pool.h，而 geqo_pool.h 内含 #include \"optimizer/geqo.h\"，因此进入 geqo_main.cpp 第 38-41 行的默认宏回退块之前 ERX 已被定义。geqo() 的声明区、内存分配、每代交叉分派和收尾释放四处均以 #if defined(ERX) 打头并后接 #elif defined(PMX)/CX/PX/OX1/OX2；即使构建额外定义 PMX/CX/PX/OX1/OX2，ERX 仍因已定义且判断顺序最先而命中。所以本源码快照下 geqo() 实际编译的是 ERX 边缘重组路径（gimme_edge_table + gimme_tour，使用 edge_table）。"
```

[geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](../pages/503935492fb1cab9eea7288e.md) · statement

```json
"在 geqo() 运行期（root->join_search_private 已指向栈上 GeqoPrivateData、root->join_rel_level 为 NULL）对每个候选 tour 调用 geqo_eval 时，函数以 CurrentMemoryContext 为父创建名为 GEQO 的 AllocSet 子上下文并切入；记录 root->join_rel_list 长度与 root->join_rel_hash 指针、断言 join_rel_level == NULL，把 hash 置 NULL，调用 gimme_tree 构造连接树，然后 fitness = ((Path*)linitial(joinrel->cheapest_total_path))->total_cost，再把 join_rel_list 截断回原长度并恢复 hash，切回原上下文并 MemoryContextDelete(GEQO)；因此 gimme_tree 内的临时连接关系对象随子上下文回收，而异常 longjmp 路径跳过恢复语句，只依赖 planner 父上下文统一回收。"
```

[geqo()/geqo_eval() 对 PlannerInfo 的临时改写与恢复，以及 GEQO GUC 进入计划缓存环境签名](../pages/35b05de95ec50ea1e2b5db3e.md) · statement

```json
"geqo() 把栈上 GeqoPrivateData 地址写入 root->join_search_private 并在正常返回前清为 NULL；geqo_eval() 每次评估时创建 GEQO 子内存上下文，记录 join_rel_list 长度与 join_rel_hash，置空 join_rel_hash 后调用 gimme_tree()，正常返回前截断 join_rel_list、恢复 hash、切回旧上下文并删除 GEQO 上下文。同一批 GEQO GUC 还被 globalplancache_util.cpp 写入全局计划缓存环境：enable_geqo 进入 env_signature2 的第 0 位，geqo_threshold、Geqo_effort、Geqo_pool_size、Geqo_generations、Geqo_selection_bias、Geqo_seed 作为独立字段填入。"
```

[gimme_tree 按 tour 增量合并 clump：desirable_join 启发式择机连接、按大小排序插入、末尾强制合并，失败以 ereport 退出](../pages/7015a856ab6c44156556aba1.md) · statement

```json
"gimme_tree 从 root->join_search_private 取 GeqoPrivateData 与 initial_rels，按 tour 中 1-based 基因逐个取基表，把每张基表包装为 size=1 的 Clump，并用 merge_clump(force=false) 只在与已有 clump 存在相关连接条件或连接顺序限制（desirable_join）时合并；tour 扫完后若仍多于一个 clump，则按现有顺序对每个 clump 再执行 merge_clump(force=true) 强制合并；最终若 clump 数不等于 1，以 ERRCODE_OPTIMIZER_INCONSISTENT_STATE 报错 \"failed to join all relations together\"，否则返回唯一 clump 的 joinrel。"
```

## 测试预期依据

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · expected_from

```json
{"kind":"claim","ref":"claim:server/src/gausskernel/optimizer/geqo:join-search-entry-selection"}
```

[geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](../pages/74c4e8dca5dbdc26adfa5c89.md) · expected_from

```json
{"kind":"claim","ref":"claim:server/src/gausskernel/optimizer/geqo:geqo-eval-child-context-and-fitness"}
```

[gimme_tree clump 合并、desirable_join 推迟与强制合并失败出口的测试预期](../pages/68441fa737966f25bad62ae2.md) · expected_from

```json
{"kind":"claim","ref":"claim:server/src/gausskernel/optimizer/geqo:gimme-tree-clump-merge-and-forced-join"}
```

## 输入、状态与边界维度

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only","测试入口为 make_rel_from_joinlist 与 geqo_eval 的正常返回路径","geeqo 开关与阈值来自当前会话 u_sess->attr.attr_sql","未运行任何 SQL、GUC 设置、编译或故障注入"]
```

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · cases

```json
["levels_needed==1：期望不进入 geqo()/standard_join_search，直接返回唯一 RelOptInfo","levels_needed>=2 且 geqo=false：期望进入 standard_join_search","levels_needed 在 [2, geqo_threshold-1]：期望进入 standard_join_search","levels_needed==geqo_threshold 且 geqo=true：期望进入 geqo()（>= 边界）","geqo_eval 正常返回：期望 join_rel_list 长度与 join_rel_hash 指针恢复为进入前值","geqo() 正常返回：期望 join_search_private 为 NULL"]
```

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · counterexamples

```json
["levels_needed==1 时断言进入 geqo() 是错误预期","geqo=false 但 levels_needed 很大时断言进入 geqo() 是错误预期","gimme_tree 内 ereport(ERROR) 后断言 list/hash 已恢复是错误预期","以缺少 GEQO_DEBUG 日志推断未走 GEQO 是无效推断"]
```

[geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](../pages/74c4e8dca5dbdc26adfa5c89.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only，未运行 SQL/编译/故障注入","调用发生在 geqo() 运行期且 root->join_search_private 有效、root->join_rel_level 为 NULL","CurrentMemoryContext 为 planner 上下文，GEQO 子上下文为其子级","测试只断言源码可推导的状态，不把 GEQO_DEBUG 日志或内存统计输出当作硬 oracle"]
```

## 实现证据

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · source_refs

```json
["evidence:c0ae6ac260a56cb6adc5fc28a443fe1e","evidence:de7316f3a1a399504f149e6157c6d518","evidence:90e7741e039c3a5f1af6dc6385495d18","evidence:9cf894263271474a263bede8d2bb47cd"]
```

[geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](../pages/74c4e8dca5dbdc26adfa5c89.md) · source_refs

```json
["evidence:cdcc3f45f682e634103fb735b81d8de5"]
```

[gimme_tree clump 合并、desirable_join 推迟与强制合并失败出口的测试预期](../pages/68441fa737966f25bad62ae2.md) · source_refs

```json
["evidence:cdcc3f45f682e634103fb735b81d8de5","evidence:1740e2ef344ce91c654e1738ef7c70d4"]
```

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · source_refs

```json
["evidence:995107881e875903bfd1d7a621d08e35","evidence:a29b817be9353dec5a2bf68daf402423","evidence:b6a65f7f71ff3505f6a8b6464215d628","evidence:dbf9d486c8447da102abab41ec69f4f5"]
```
