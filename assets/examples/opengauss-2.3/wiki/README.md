# 源码知识 Wiki

openGauss · content-addressed · linux-native

## 已核对结论

- [claim：bias 默认 2.0 且 1.0 不在注册范围](pages/5874ca7c07c9ed17490ab581.md)
- [CheckRecreateCachePlanBySqlPatch 的判定条件与语义边界](pages/234a0c4e1b022361a8f381df.md)
- [claim：ERX 在头文件无条件定义使其他交叉分支不可达](pages/f7d2f50dd59f5998387b3d08.md)
- [claim：GEQO_DEBUG 调试面由 ifdef 条件编译，启用与否取决于构建宏](pages/9cb3cc9612e4abbd861f9a32.md)
- [claim：pool_size=1 被消费者忽略](pages/7d1d7e2615901e16c9191af7.md)
- [RevalidateGplanBySqlPatch 的快速返回、目录/QueryIsPatched 判定与失效后续处理](pages/1fa951c5675aa482ac23bb12.md)
- [claim：seed 只保证同构建同序列的可复现性边界](pages/266f4a86d5cf54a512ac37b9.md)
- [全局补丁序号的类型、初始化与所引提交推进点](pages/a10df08269bba8cac992b0f7.md)
- [claim：备用交叉算子编译但不可达](pages/98bd671e513de35eba47e6d5.md)

## 源码契约

- [契约：geqo → geqo_eval 的候选打分](pages/6f0284e7987dc5182111596a.md)
- [契约：gimme_tour → geqo_rand/remove_gene/gimme_gene 的 tour 生成](pages/8fa0c030df201a2e37335803.md)
- [契约：geqo_eval → gimme_tree 的树重建](pages/99bd348b6e0b4fe53ad103fc.md)
- [契约：spread_chromo → geqo_copy 的最差替换](pages/6775fea90b2b597450bad640.md)
- [契约：geqo_selection → geqo_copy 的父代复制](pages/0aa2ed6076968e4359e0ee9e.md)
- [SQL Patch 序号失效端点与全局计划缓存/RevalidateCachedQuery 的调用契约](pages/eceaf0d4c3fcce21305fc4b4.md)

## decision

- [决策：开发修改指南与 Review 检查点](pages/b52fab9fe6b8dc4589860661.md)

## 特性节点

- [L2 · L2 特性：连接顺序优化能力](pages/235216264475c8cfbfca264b.md)
- [L4 · L4 特性：构建目标与调试宏面](pages/6c231d593cd1740bdc4b41df.md)
- [L4 · L4 特性：clump 合并与终态计划重建](pages/ced6757a212adccba79cc6b8.md)
- [L4 · L4 特性：ERX 边重组交叉](pages/2ed0448a471f581e9147d015.md)
- [L4 · L4 特性：候选适应度与临时上下文](pages/c5df46c306e8c1493b7576fe.md)
- [L4 · L4 特性：GEQO 启用门控](pages/aae85b971b0ad0640c35be8f.md)
- [L4 · L4 特性：GEQO 参数注册与会话字段](pages/f8b5572b254ee660b572f24d.md)
- [L4 · L4 特性：种群初始化、排序与最差替换](pages/c31cea325c59385afc3c2d95.md)
- [L3 · L3 特性：GEQO 可观察能力](pages/6dc89cbbd38bf88b53c52e95.md)
- [L4 · L4 特性：代际遗传搜索](pages/5c78f3b5f6b894785dcebb7b.md)
- [L4 · L4 特性：线性偏置父代选择](pages/c8d0575c083d8efd9f57ef27.md)
- [L4 · L4 特性：PMX/CX/PX/OX1/OX2 与变异（未启用）](pages/f1e492c5744be19e2d7e04f2.md)
- [L1 · L1 特性：SQL 能力（GEQO 所属）](pages/ce40f626a18e7340b836c796.md)
- [L1 · 特性：以实例级补丁序号驱动计划缓存失效与重解析](pages/57c20d8fd513e1594122a2e6.md)
- [L2 · 特性子项：共享计划的补丁重建走 GPC 检查与复制重建，不原地失效](pages/0117ffe30c237bc27711d6e8.md)

## 调用与数据流程

- [主流程：门控→遗传迭代→评估→终态重建](pages/3bb0a8e18999444e7ade88e7.md)
- [SQL patch 从提交推进序号到共享/本地计划重验证的流程](pages/0ce53dfa96b13c1bc5a198c8.md)

## mechanism

- [机制：局部断言、失败谓词与清理边界](pages/66429f4bfcd7eec7949a994a.md)
- [机制：ERX 中 kid=momma 的别名关系](pages/65aff5672a6c47328aa4b2b9.md)
- [机制：GEQO GUC 注册、读取时机与消费者](pages/4bda7d5b31a51d580b6d1983.md)
- [机制：评估临时上下文与长寿命池对象的所有权](pages/28439cc00af9962c2daf2191.md)
- [机制：池升序不变量与 spread_chromo 右移替换](pages/3e5e03a8f33285a7d7918262.md)
- [机制：随机状态、seed 初始化与可复现边界](pages/9984ffede30ef90963057370.md)

## module

- [GEQO 子模块总览：遗传式连接顺序搜索](pages/d931e30bb0af4ab701044479.md)

## observation

- [join.sql 与 single_node_join.sql 已包含多重退化 IN 的 GEQO 存量回归脚本](pages/1103fd4f40ebc41de0a2a330.md)
- [观察：范围、未运行项与外部未知](pages/52ba0826d6a1cca204e15d20.md)
- [源码分支差异与回滚、快照和同步待核问题](pages/79f554312bd1cf2899c4a42a.md)

## 责任范围

- [L4 · L4 责任：构建接入与调试宏面](pages/09a077aa20c03ad855f4e3ef.md)
- [L4 · L4 责任：clump 启发式合并与强制兜底](pages/d0be0bdcb5deebd473915ce5.md)
- [L4 · L4 责任：ERX 边表、tour 生成与边失败兜底](pages/374cc363a8f946585702f666.md)
- [L4 · L4 责任：驱动与资源生命周期](pages/ce9c8f36238b240fe069a0e0.md)
- [L4 · L4 责任：适应度评估与临时状态还原](pages/b013203bb1db8bd51d816495.md)
- [L4 · L4 责任：单代选择-交叉-评估-替换](pages/ccfc0b6bfdd89014e1319c5e.md)
- [L4 · L4 责任：池大小与代数预算决策](pages/7d3b66fcdd31af6241f16999.md)
- [L4 · L4 责任：终态计划重建](pages/7123e639bf65c8a193acc5ad.md)
- [L3 · L3 责任：GEQO 近似连接搜索总体](pages/9ec835f6815b6d9e5dd3881d.md)
- [L4 · L4 责任：线性偏置选择与复制](pages/a93ee3a126405794fb5a87d1.md)
- [L4 · L4 责任：池/染色体/边表临时存储与释放](pages/fa9c5c266da49e7a338a45e7.md)
- [L2 · L2 责任：查询优化器连接搜索](pages/071474ed5b5d90979399d734.md)
- [L1 · L1 责任：SQL 引擎（GEQO 所属）](pages/ba702595505ef4fcc259e2e5.md)
- [L1 · SQL Patch 模块的职责：维护补丁目录与计划缓存之间的版本一致性](pages/eee044a492ad5f0099728e68.md)

## 应测场景

- [测试：gimme_tour 输出为 1..num_gene 的排列](pages/1d047ad699906bcf6c303cf8.md)
- [测试：geqo_eval 恢复 join_rel_list/hash 并返回 cheapest_total_path 成本](pages/17c836f7bb3e91f8cd8587d5.md)
- [测试：geqo_eval ERROR 时临时上下文回收边界](pages/e9f82773648e126a23d0a23b.md)
- [测试：force 合并仍受 make_join_rel 合法性约束](pages/f7ec92e11e88419f47e2a1af.md)
- [测试：关闭 enable_geqo 时回退标准连接搜索](pages/ead8c7c12df95e98d7c43b76.md)
- [测试：geqo_threshold 的等于/小于边界](pages/c9c06bc9f8de2ed411ce8070.md)
- [复用存量多重退化 IN 回归作为 GEQO 基线测试](pages/ecbc3064c66f72e2a9f7c48f.md)
- [测试：gimme_tree 必须形成单一 clump 或报错](pages/3fffdeb218cd7861ba186d43.md)
- [测试：geqo_pool_size=1 被忽略且不报错](pages/bf2a8f83475467a5db5d7828.md)
- [测试：同 seed 同序列的可复现性与跨架构边界](pages/291d5005c1dcabbadb3da98a.md)
- [测试：pool>1 时选中槽位索引 first/second 不同（不保证内容不同）](pages/76f89316e9cd065ad4816632.md)
- [测试：spread_chromo 接受与最差等值的 kid](pages/51736d438fe072295e670e7e.md)
- [测试：spread_chromo 拒绝严格更差的 kid](pages/ff4b7b6436599c8a7acddb05.md)
- [测试义务：补丁序号在只读/共享/回滚/并发窗口下的边界行为](pages/d788d88d31b3b8b16b5c4ea4.md)
