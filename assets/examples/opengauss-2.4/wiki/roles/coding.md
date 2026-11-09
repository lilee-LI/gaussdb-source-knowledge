# 开发知识视图

修订 knowledge:9e4ee092006998e86d257dfc0032055f

状态 partial

## 实现行为与入口

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · statement

```json
"在 make_rel_from_joinlist 中，只有 levels_needed > 1 且 enable_geqo 为真、levels_needed >= geqo_threshold 时才调用 geqo()，否则走 standard_join_search；七个 GEQO GUC 均为 PGC_USERSET/NODE_ALL、分类 QUERY_TUNING_GEQO，并注册了默认值与上下界；geqo() 借用 root->join_search_private 存放栈上 GeqoPrivateData 并在正常返回前清空；geqo_eval() 为每次评估创建并删除 GEQO 子内存上下文，并按原长度/原指针恢复 join_rel_list 与 join_rel_hash；同一批 GUC 以 enable_geqo 的 1 个签名位和其余 6 个值字段进入全局计划缓存环境。"
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · statement

```json
"在 enable_geqo 为真且 levels_needed >= geqo_threshold、从而由 make_rel_from_joinlist 调用 geqo() 时，geqo() 把栈上 GeqoPrivateData 挂到 root->join_search_private，按 Geqo_seed 播种，按 Geqo_pool_size/Geqo_effort 定池大小、按 Geqo_generations（0 则取池大小）定代数，随后用 random_init_pool 初始化并 sort_pool 排序；每代以 Geqo_selection_bias 选取双亲，按编译宏选择交叉算子（源码层 ERX），用 geqo_eval 读取代价并 spread_chromo 替换最差个体；循环结束后取池首个体调用一次不计入 GEQO 子上下文的 gimme_tree 得到 best_rel，再按同样宏组释放 momma/daddy/交叉缓冲/池并把 root->join_search_private 置 NULL 后返回。"
```

[源码层 ERX 由 geqo.h 无条件定义，geqo() 的交叉分支恒走 ERX](../pages/7edbf06c7441fff5fbd7dfb9.md) · statement

```json
"在源码层，server/src/include/optimizer/geqo.h 在 include guard 内、任何条件编译之外无条件 #define ERX（第 30 行）。geqo_main.cpp 第 31 行包含 optimizer/geqo_pool.h，而 geqo_pool.h 内含 #include \"optimizer/geqo.h\"，因此进入 geqo_main.cpp 第 38-41 行的默认宏回退块之前 ERX 已被定义。geqo() 的声明区、内存分配、每代交叉分派和收尾释放四处均以 #if defined(ERX) 打头并后接 #elif defined(PMX)/CX/PX/OX1/OX2；即使构建额外定义 PMX/CX/PX/OX1/OX2，ERX 仍因已定义且判断顺序最先而命中。所以本源码快照下 geqo() 实际编译的是 ERX 边缘重组路径（gimme_edge_table + gimme_tour，使用 edge_table）。"
```

[geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](../pages/503935492fb1cab9eea7288e.md) · statement

```json
"在 geqo() 运行期（root->join_search_private 已指向栈上 GeqoPrivateData、root->join_rel_level 为 NULL）对每个候选 tour 调用 geqo_eval 时，函数以 CurrentMemoryContext 为父创建名为 GEQO 的 AllocSet 子上下文并切入；记录 root->join_rel_list 长度与 root->join_rel_hash 指针、断言 join_rel_level == NULL，把 hash 置 NULL，调用 gimme_tree 构造连接树，然后 fitness = ((Path*)linitial(joinrel->cheapest_total_path))->total_cost，再把 join_rel_list 截断回原长度并恢复 hash，切回原上下文并 MemoryContextDelete(GEQO)；因此 gimme_tree 内的临时连接关系对象随子上下文回收，而异常 longjmp 路径跳过恢复语句，只依赖 planner 父上下文统一回收。"
```

## 适用条件

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only，未运行 SQL/GUC 设置/编译/故障注入","进入 make_rel_from_joinlist 且 levels_needed > 1；GUC 取值来自当前会话 u_sess->attr.attr_sql","状态恢复结论以 geqo_eval 正常返回路径为准；ereport(ERROR) 中止路径不执行恢复语句","计划缓存结论仅覆盖 globalplancache_util.cpp 第 95-179 行的签名/字段填充，不含缓存匹配与失效算法","GEQO_DEBUG、ERX 及其他交叉宏的实际编译状态未验证"]
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only，未运行 SQL/GUC/编译/故障注入","由 make_rel_from_joinlist 在 levels_needed > 1 且 enable_geqo 为真、levels_needed >= geqo_threshold 时调用 geqo()（入口条件来自已审 claim，本 attempt 未重读 allpaths.cpp）","Geqo_seed/Geqo_pool_size/Geqo_effort/Geqo_generations/Geqo_selection_bias 取当前会话 u_sess->attr.attr_sql 值","翻译单元包含 optimizer/geqo.h（经 geqo_pool.h 间接包含），使源码层宏分支为 ERX","GEQO_DEBUG 是否定义、实际交叉宏由构建决定，未验证"]
```

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；declared-build / source_only，未编译、未做 TU 解析","两者构建文件共存于 server/src/gausskernel/optimizer/geqo，且 Makefile 的 OBJS 与目录内 .cpp 当前一致（15 个）","geqo_main.cpp 经 optimizer/geqo_pool.h 间接包含 optimizer/geqo.h，使 geqo.h 的无条件 #define ERX 在宏判断前生效","compile_commands.json 的 geqo_eval.cpp/geqo_main.cpp 声明行是本 attempt 实际冻结读取的 6053-6062 行","构建变量 MACRO_OPTIONS/MACRO、OPTIMIZE_OPTIONS 等的实际取值由上层构建系统决定，未读"]
```

[源码层 ERX 由 geqo.h 无条件定义，geqo() 的交叉分支恒走 ERX](../pages/7edbf06c7441fff5fbd7dfb9.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146","翻译单元包含 optimizer/geqo.h（geqo_main.cpp 经 geqo_pool.h 间接包含），使第 30 行的 #define ERX 在任何宏判断前生效","未出现 #undef ERX（server/src/include/optimizer/* 搜索无 #undef 命中）","构建是否额外定义 PMX/CX/PX/OX1/OX2 不改变结果：ERX 总已定义，且 #if defined(ERX) 在全部 #elif 之前"]
```

## 实现证据

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · source_refs

```json
["evidence:c0ae6ac260a56cb6adc5fc28a443fe1e","evidence:094dae4a795787e32fba6827ce8c4b49","evidence:cf7a96b418097855b370cb55ebcbe6ae","evidence:5bfb8f409356e673137336be48cb58ca","evidence:90e7741e039c3a5f1af6dc6385495d18","evidence:9cf894263271474a263bede8d2bb47cd","evidence:de7316f3a1a399504f149e6157c6d518","evidence:121b6810e6c9081bb37a029e599c5e22"]
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · source_refs

```json
["evidence:4f7db3e4c1edbef23d45e23a3c03e6d6","evidence:567e0488b204eb37f9b42f075feafe22","evidence:b6a65f7f71ff3505f6a8b6464215d628","evidence:dbf9d486c8447da102abab41ec69f4f5"]
```

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · source_refs

```json
["evidence:995107881e875903bfd1d7a621d08e35","evidence:a29b817be9353dec5a2bf68daf402423","evidence:b6a65f7f71ff3505f6a8b6464215d628","evidence:dbf9d486c8447da102abab41ec69f4f5"]
```

[源码层 ERX 由 geqo.h 无条件定义，geqo() 的交叉分支恒走 ERX](../pages/7edbf06c7441fff5fbd7dfb9.md) · source_refs

```json
["evidence:b6a65f7f71ff3505f6a8b6464215d628","evidence:fca84562596d3a2aa417614bac484806","evidence:3d21632bb8ef14d848918c29be591b8b","evidence:dbf9d486c8447da102abab41ec69f4f5","evidence:ff70b75d6aa0b17756430436a83931e2"]
```

## 接口与状态约束

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · state

```json
{"initial_rels":"make_rel_from_joinlist 在分流前写入 root->initial_rels，geqo() 与 standard_join_search 分别消费","plan_cache_env":"env_signature2 第 0 位 = enable_geqo；plainenv 保存 geqo_threshold 与其余 5 个 GEQO 算法 GUC 的值","planner_join_state":"root->join_rel_list 长度在每次 geqo_eval 前后相同；root->join_rel_hash 在评估期临时为 NULL、之后恢复原指针；root->join_rel_level 必须为 NULL（仅断言）","planner_private_slot":"root->join_search_private 在 geqo() 运行期指向栈上 GeqoPrivateData（含 initial_rels 与 random_state），正常返回前置 NULL","session_gucs":"enable_geqo=true、geqo_threshold=12、Geqo_effort=5、Geqo_pool_size=0、Geqo_generations=0、Geqo_selection_bias=2.0、Geqo_seed=0.0 为注册默认值"}
```

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · state_transitions

```json
[{"at":"make_rel_from_joinlist 分流","transition":"levels_needed>1 -> root->initial_rels=initial_rels -> 条件成立则 geqo()，否则 standard_join_search","trigger":"allpaths.cpp:3400"},{"at":"geqo() 入口","transition":"root->join_search_private 改为 &priv（栈上 GeqoPrivateData），priv.initial_rels=initial_rels","trigger":"geqo_main.cpp:77-78"},{"at":"每次 geqo_eval 评估","transition":"join_rel_hash 原值 -> NULL -> 原值；join_rel_list 长度 N -> N+k -> N；join_rel_level 维持 NULL（断言）","trigger":"geqo_eval.cpp:86-108"},{"at":"每次 geqo_eval 内存","transition":"CurrentMemoryContext -> GEQO 子上下文 -> oldcxt；随后 MemoryContextDelete(GEQO)","trigger":"geqo_eval.cpp:67-69,111-112"},{"at":"geqo() 正常返回","transition":"释放 momma/daddy/edge_table/pool 后 root->join_search_private = NULL","trigger":"geqo_main.cpp:237-265"}]
```

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · resource_lifecycle

```json
"GEQO 内存上下文由 AllocSetContextCreate 在 CurrentMemoryContext 下创建，是 planner 上下文的子上下文；正常路径 MemoryContextSwitchTo(oldcxt) 后 MemoryContextDelete(mycontext)，异常 ereport(ERROR) 路径由父上下文统一回收。种群 Pool、染色体 momma/daddy、按 ERX 宏分配的 edge_table 均在 geqo() 内分配并在返回前 free；GeqoPrivateData priv 是栈对象，不单独释放。"
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · state

```json
{"best_tour":"指向 pool->data[0].string，仅在 free_pool 前有效","kid":"ERX：kid = momma（就地改写 string）；PMX/CX/PX/OX1/OX2：kid 独立分配，循环内复用","operator_buffers":"ERX edge_table+edge_failures；CX 另有 cycle_diffs/mutations；PX/OX1/OX2 与 CX 各需 city_table","parents":"momma/daddy 各 alloc_chromo(string_length)，每代由 geqo_selection 重新复制","planner_private_slot":"root->join_search_private 指向 geqo() 栈上 GeqoPrivateData{initial_rels, random_state[3]}，正常返回前置 NULL","pool":"Pool* pool：size=pool_size，Chromosome 数组，string_length=number_of_rels，worth 升序（data[0] 最优、data[pool_size-1] 最差）","session_gucs":"Geqo_seed、Geqo_pool_size、Geqo_effort、Geqo_generations、Geqo_selection_bias 在本次调用中只读"}
```

## 消费者与影响

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · consumers

```json
["server/src/gausskernel/optimizer/path/allpaths.cpp:3400-3403 使用 enable_geqo 与 geqo_threshold 选择 geqo()/standard_join_search","server/src/gausskernel/optimizer/geqo/geqo_main.cpp:77-81 设置 join_search_private 并消费 Geqo_seed","server/src/gausskernel/optimizer/geqo/geqo_main.cpp:279-311 消费 Geqo_pool_size/Geqo_effort/Geqo_generations 计算 pool_size 与代数","server/src/gausskernel/optimizer/geqo/geqo_eval.cpp:86-108 保存并恢复 root->join_rel_list/join_rel_hash/join_rel_level","server/src/gausskernel/process/globalplancache/globalplancache_util.cpp:106,158-163 把同一批 GEQO GUC 写入全局计划缓存环境"]
```

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · affected_modules

```json
["server/src/gausskernel/optimizer/path","server/src/gausskernel/optimizer/geqo","server/src/common/backend/utils/misc/guc","server/src/gausskernel/process/globalplancache","server/src/include/optimizer","server/src/include/knl（会话 GUC 字段声明，本 attempt 未读）"]
```

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · knowledge_refs

```json
{"relation":"DEPENDS_ON","target":"claim:server/src/gausskernel/optimizer/geqo:join-search-entry-selection"}
```

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · knowledge_refs

```json
{"relation":"DEPENDS_ON","target":"claim:server/src/gausskernel/optimizer/geqo:guc-registration-and-bounds"}
```
