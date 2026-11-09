# 源码知识 Wiki

openGauss · ed99bbde5308942d4eb062e7a851bdb85dda902f · declared-build

[按模块](views/module.md) · [按特性](views/feature.md) · [按执行主干](views/mainline.md) · [开发视图](roles/coding.md) · [测试生成视图](roles/test_generation.md) · [代码评审视图](roles/review.md) · [运维视图](roles/operations.md) · [结构化知识与来源 JSON](knowledge.json)

## 已核对结论

- [GEQO 构建组合：CMake 自动收集全部源文件到静态对象目标，Makefile 显式列 15 个 .o；交叉宏在源码层由 geqo.h 无条件定义 ERX](pages/c49395b141add9645feb899f.md)
- [源码层 ERX 由 geqo.h 无条件定义，geqo() 的交叉分支恒走 ERX](pages/7edbf06c7441fff5fbd7dfb9.md)
- [geqo_eval 以 GEQO 子内存上下文隔离单次 gimme_tree，成对恢复 join_rel 状态后以 cheapest_total_path 代价作为 fitness](pages/503935492fb1cab9eea7288e.md)
- [geqo()/geqo_eval() 对 PlannerInfo 的临时改写与恢复，以及 GEQO GUC 进入计划缓存环境签名](pages/35b05de95ec50ea1e2b5db3e.md)
- [gimme_tree 按 tour 增量合并 clump：desirable_join 启发式择机连接、按大小排序插入、末尾强制合并，失败以 ereport 退出](pages/7015a856ab6c44156556aba1.md)
- [GEQO 七个 GUC 的注册上下文、默认值与上下界](pages/d49f95457f502fa7d1668e70.md)
- [make_rel_from_joinlist 仅在 enable_geqo 打开且 levels_needed >= geqo_threshold 时才调用 geqo()](pages/a33d831475c1dfdaf80e9cd7.md)

## mechanism

- [GEQO 入口、GUC 约束与 PlannerInfo/计划缓存状态契约](pages/4262939b5238222715309097.md)
- [GEQO 主循环：池/代数参数计算、每代选择-交叉-评估-替换与释放顺序](pages/35a82ea6cb4914924c30b9d5.md)

## 应测场景

- [GEQO 入口阈值/开关分支与 geqo_eval 状态恢复的源码预期](pages/6a42528f8a71c2413a10f0b6.md)
- [geqo_eval 的 GEQO 子上下文回收、join_rel 状态恢复与异常路径的测试预期](pages/74c4e8dca5dbdc26adfa5c89.md)
- [gimme_tree clump 合并、desirable_join 推迟与强制合并失败出口的测试预期](pages/68441fa737966f25bad62ae2.md)
