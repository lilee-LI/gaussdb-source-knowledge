# 运维知识视图

修订 knowledge:9e4ee092006998e86d257dfc0032055f

状态 partial

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

## 症状与观测

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · operations.observations

```json
[{"candidate":"编译数据库中存在 CMakeFiles/gausskernel_optimizer_geqo.dir/geqo_*.cpp.o 的记录","caveat":"这是声明上下文；未确认对象文件真实存在或编译成功","source":"compile_commands.json:6053-6062 输出路径"},{"candidate":"CMake 构建目录中出现 gausskernel_optimizer_geqo 目标","caveat":"未运行 CMake；目标实际形态由 add_static_objtarget 定义决定（未读）","source":"CMakeLists.txt:18"},{"candidate":"Make 构建目录中出现 15 个 .o","caveat":"未运行 make；依赖 Makefile.global/common.mk 规则","source":"Makefile:19-22 OBJS"}]
```

[geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](../pages/503935492fb1cab9eea7288e.md) · operations.observations

```json
[{"candidate":"语句期间内存上下文中出现名为 \"GEQO\" 的子上下文（若诊断输出列出上下文树）","caveat":"本 attempt 未确认具体内存诊断接口/视图；每次评估都会创建并删除，稳定存在可能意味着异常路径或泄漏","source":"geqo_eval.cpp:67-69 的 AllocSetContextCreate 名称"},{"candidate":"多表查询规划时间随候选 tour 数增长（pool_size + generations 次评估）","caveat":"未运行计时；GC/统计/连接树复杂度不可由源码定量","source":"geqo_main.cpp:190 每代一次 + random_init_pool（已审 claim）"},{"candidate":"无 \"GEQO\" 上下文残留可作为正常回收的弱证据","caveat":"只在能观察上下文树时有意义；未验证","source":"正常路径 MemoryContextDelete"}]
```

[gimme_tree 按 tour 增量合并 clump：desirable_join 启发式择机连接、按大小排序插入、末尾强制合并，失败以 ereport 退出](../pages/7015a856ab6c44156556aba1.md) · operations.observations

```json
[{"candidate":"规划错误日志出现 \"failed to join all relations together\"（errmodule MOD_OPT，ERRCODE_OPTIMIZER_INCONSISTENT_STATE）","caveat":"表示强制合并后仍未形成单一 clump；触发条件与具体查询相关，未运行复现","source":"gimme_tree 失败出口（geqo_eval.cpp 1-200 区间后段）"},{"candidate":"同一查询在 geqo 开关切换后计划形态（bushy/连接顺序）不同","caveat":"源码未承诺 EXPLAIN 可稳定区分 GEQO 与动态规划；不能作硬判定证据","source":"gimme_tree 的 desirable/force 合并与 tour 指导"},{"candidate":"候选 tour 的 fitness 分布随 clump 合并结果变化","caveat":"无运行时观测；pool 初始化/替换由已审 claim 说明","source":"geqo_eval 读取 joinrel->cheapest_total_path"}]
```

## 诊断证据

[GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](../pages/4262939b5238222715309097.md) · operations.diagnostics

```json
[{"check":"先确认当前会话 enable_geqo 与 geqo_threshold，以及目标查询的 jointree 分项数 levels_needed","evidence":"allpaths.cpp:3400 条件；GUC 注册项","why":"决定是否可能进入 geqo()，避免把标准动态规划计划误判为 GEQO 问题"},{"check":"检查 joinlist 分项数是否大于 1","evidence":"allpaths.cpp:3385-3389","why":"levels_needed==1 时根本不进入任何连接搜索算法"},{"check":"若怀疑状态泄漏，核对 geqo_eval 前后的 join_rel_list 长度与 join_rel_hash 指针","evidence":"geqo_eval.cpp:86-108","why":"源码以截断/恢复方式回滚状态，异常路径不执行恢复"},{"check":"若更改了 GEQO GUC，核对 globalplancache_util.cpp 是否包含该参数","evidence":"globalplancache_util.cpp:106,158-163","why":"GEQO GUC 是计划缓存环境的一部分；遗漏会使缓存环境身份不完整"}]
```

[GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](../pages/35a82ea6cb4914924c30b9d5.md) · operations.diagnostics

```json
[{"check":"确认当前会话 enable_geqo、geqo_threshold 与查询 jointree 分项数，判断是否可能进入 geqo()","evidence":"入口条件由已审 claim join-search-entry-selection；本 attempt 未重读 allpaths.cpp","why":"未进入 geqo() 时调 GEQO 参数不会改变计划"},{"check":"SHOW geqo_pool_size / geqo_effort / geqo_generations / geqo_selection_bias / geqo_seed，按源码公式复算实际 pool_size 与代数","evidence":"geqo_main.cpp:274-311","why":"配置值 0/1/<2 被忽略，0 代表示自动，容易误读"},{"check":"若怀疑 GEQO 未执行，先查构建是否定义 GEQO_DEBUG","evidence":"geqo_main.cpp 的 #ifdef GEQO_DEBUG 分支","why":"无日志不等于未执行"},{"check":"关注 edge_failures/mutations 汇总日志（ERX/CX + GEQO_DEBUG）","evidence":"geqo_main.cpp:202-214","why":"可提示交叉算子质量，但仅诊断构建可见"}]
```

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · operations.diagnostics

```json
[{"check":"确认当前构建走 CMake 还是 Makefile 路径，并核对源集合是否包含全部 15 个 .cpp","evidence":"CMakeLists.txt:2；Makefile:19-22","why":"两条路径的源集合维护方式不同，缺失会造成链接错误或遗漏"},{"check":"怀疑交叉算子行为与预期不符时，先确认 geqo.h 的 ERX 定义未被改动，再查构建是否注入其他宏","evidence":"geqo.h:30；geqo_main.cpp:38-41","why":"ERX 在头文件无条件定义，命令行无交叉宏"},{"check":"确认 GEQO_DEBUG 是否被构建启用（声明命令行无该宏）","evidence":"compile_commands.json:6053-6062；geqo_main.cpp 的 #ifdef GEQO_DEBUG","why":"决定调试日志是否存在"},{"check":"对象目录/目标名是否与本模块 CMake 目标一致","evidence":"CMakeLists.txt:18 与 compile_commands.json 输出路径","why":"可判断声明来自哪条构建路径"}]
```

[geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](../pages/503935492fb1cab9eea7288e.md) · operations.diagnostics

```json
[{"check":"若怀疑 GEQO 规划期状态污染，核对 geqo_eval 调用前后 root->join_rel_list 长度与 join_rel_hash 指针","evidence":"geqo_eval.cpp:86-108","why":"正常路径应恢复；异常路径不会执行恢复"},{"check":"确认 join_rel_level 在 GEQO 期间为 NULL","evidence":"geqo_eval.cpp:88 AssertEreport","why":"非断言构建不阻止违反，可能引发未定义行为"},{"check":"怀疑内存增长时区分单次评估泄漏与池/评估次数放大","evidence":"GEQO 子上下文按次创建/删除；池与染色体在 geqo() 内","why":"放大效应来自评估次数，不是单次泄漏"},{"check":"确认最终 best_rel 是在 planner 上下文生成（不经 geqo_eval）","evidence":"geqo_main.cpp:230","why":"把最终构造也包进 geqo_eval 会删除 best_rel"}]
```

## 配置来源及生效边界

缺少已审知识，需要补充。

## 有条件处理依据

[GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](../pages/c49395b141add9645feb899f.md) · operations.actions

```json
[{"action":"依赖 CMake 自动收集的同时，手工把对应 .o 加入 Makefile OBJS，并复核依赖文件","condition":"新增 GEQO 源文件","guard":"本次未运行构建；add_static_objtarget 与 common.mk 规则未读"},{"action":"移除/条件化 geqo.h 的 ERX 定义，在构建层注入目标宏，并同步 geqo_main.cpp 四处宏组","condition":"需要切换交叉算子","guard":"未编译验证；仅改构建文件或仅改兜底块都无效"},{"action":"以实际编译命令/构建变量为准；声明命令行可作为线索但不能证明最终产物","condition":"需要判断产物是否启用 GEQO_DEBUG","guard":"未做 TU 解析或产物检查"},{"action":"先比对 CMake 自动源集合与 Makefile OBJS，再检查宏注入变量","condition":"发现不同构建路径行为不一致","guard":"两条路径实际采用关系未核对"}]
```
