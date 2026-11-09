# 代码评审知识视图

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

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only","测试入口为 make_rel_from_joinlist 与 geqo_eval 的正常返回路径","geeqo 开关与阈值来自当前会话 u_sess->attr.attr_sql","未运行任何 SQL、GUC 设置、编译或故障注入"]
```

[geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](../pages/74c4e8dca5dbdc26adfa5c89.md) · conditions

```json
["源码快照 snapshot:e3c7591bc57779ef711950941aa64146；source_only，未运行 SQL/编译/故障注入","调用发生在 geqo() 运行期且 root->join_search_private 有效、root->join_rel_level 为 NULL","CurrentMemoryContext 为 planner 上下文，GEQO 子上下文为其子级","测试只断言源码可推导的状态，不把 GEQO_DEBUG 日志或内存统计输出当作硬 oracle"]
```

## 评审不变量

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · invariants

```json
["geqo() 仅在 enable_geqo 为真且 levels_needed >= geqo_threshold 时被 make_rel_from_joinlist 调用；levels_needed==1 时不进入任何连接搜索","geqo() 正常返回后 root->join_search_private == NULL，且 priv 不得逃逸栈帧","geqo_eval 正常返回后 root->join_rel_list 长度等于进入前长度，root->join_rel_hash 等于进入前指针","gimme_tree 只能向 root->join_rel_list 尾部追加项","gimme_tree 运行时 root->join_rel_level 必须为 NULL（AssertEreport 断言，否则失败）","GEQO 临时内存上下文必须是 planner 上下文的子上下文，并在正常路径显式删除","七个 GEQO GUC 的注册分类与作用域保持 PGC_USERSET/NODE_ALL；变更默认值或上下同时影响入口选择、算法参数与计划缓存环境"]
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · invariants

```json
["pool_size 由 helper 保证 >= 2（配置值 < 2 视为自动，自动下限 10*effort >= 10）","number_generations >= 1（pool_size >= 2；显式配置必须 > 0 才生效）","best_tour 必须在 free_pool 之前被 gimme_tree 消费","root->join_search_private 必须在所有正常返回路径置 NULL，priv 不得逃逸栈帧","四处交叉宏组（声明/分配/交叉/释放）必须一致；ERX 下 kid 是 momma 的别名，不得单独释放","最后构造 best_rel 的 gimme_tree 调用不经过 geqo_eval，其 RelOptInfo 必须留在 planner 上下文","GEQO_DEBUG 分支只影响诊断输出，不改变算法状态"]
```

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · invariants

```json
["两份构建文件的源集合必须一致（当前 15 个 .cpp；CMake 自动、Makefile 手工）","交叉算子宏不得在 geqo.h 无条件定义的同时依赖构建层切换；当前源码层 ERX 恒定义","声明层编译命令不含交叉宏与 GEQO_DEBUG（本 attempt 读取的两条命令）","CMake 目标名与对象目录必须与 compile_commands.json 的记录一致（gausskernel_optimizer_geqo）","构建声明不等于编译成功或 TU 解析通过"]
```

[geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](../pages/503935492fb1cab9eea7288e.md) · invariants

```json
["每次 geqo_eval 的 join_rel_list 长度保存与截断、join_rel_hash 保存与恢复都必须成对","gimme_tree 及其被调方只能向 root->join_rel_list 尾部追加（源码注释假设）","gimme_tree 运行期间 root->join_rel_level 必须为 NULL","GEQO 上下文必须是 planner 上下文的子上下文，并在正常路径删除；fitness 必须在删除前读取","不得把子上下文内的 RelOptInfo/Path 指针作为返回值带出（返回值只有 Cost）","评估期间 hash 置 NULL 的前提是 gimme_tree 能在局部重建 hash"]
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

## 实现证据

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · source_refs

```json
["evidence:c0ae6ac260a56cb6adc5fc28a443fe1e","evidence:094dae4a795787e32fba6827ce8c4b49","evidence:cf7a96b418097855b370cb55ebcbe6ae","evidence:5bfb8f409356e673137336be48cb58ca","evidence:90e7741e039c3a5f1af6dc6385495d18","evidence:9cf894263271474a263bede8d2bb47cd","evidence:de7316f3a1a399504f149e6157c6d518","evidence:121b6810e6c9081bb37a029e599c5e22"]
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · source_refs

```json
["evidence:4f7db3e4c1edbef23d45e23a3c03e6d6","evidence:567e0488b204eb37f9b42f075feafe22","evidence:b6a65f7f71ff3505f6a8b6464215d628","evidence:dbf9d486c8447da102abab41ec69f4f5"]
```

[GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](../pages/6a42528f8a71c2413a10f0b6.md) · source_refs

```json
["evidence:c0ae6ac260a56cb6adc5fc28a443fe1e","evidence:de7316f3a1a399504f149e6157c6d518","evidence:90e7741e039c3a5f1af6dc6385495d18","evidence:9cf894263271474a263bede8d2bb47cd"]
```

[geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](../pages/74c4e8dca5dbdc26adfa5c89.md) · source_refs

```json
["evidence:cdcc3f45f682e634103fb735b81d8de5"]
```
