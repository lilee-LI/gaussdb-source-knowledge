# SQL Patch 序号失效端点与全局计划缓存/RevalidateCachedQuery 的调用契约

openGauss · content-addressed · linux-native

审阅状态 independent_review

SQL Patch提供两个不同端点。共享计划消费者在所引非多节点分支调用CheckRecreateCachePlanBySqlPatch；布尔结果只是重建判据的一部分。私有计划消费者RevalidateCachedQuery在提前返回检查后调用RevalidateGplanBySqlPatch，由后者按标记或目录命中设置有效性字段，再由消费者处理重解析。锁、对象复制和发布属于调用方协议，必须分别检查入口，不从一个SPI调用点推断所有调用方。两处实际静态调用与数据/状态阶段分开记录；两个消费模块尚需分别核对本契约。

## 提供方符号

- CheckRecreateCachePlanBySqlPatch · server/src/gausskernel/optimizer/sqlpatch/sqlpatch.cpp:751-761
- RevalidateGplanBySqlPatch · server/src/gausskernel/optimizer/sqlpatch/sqlpatch.cpp:763-830

## 使用方符号

- CheckRecreateCachePlan · server/src/gausskernel/process/globalplancache/globalplancache.cpp:556-626
- RevalidateCachedQuery · server/src/common/backend/utils/cache/plancache.cpp:829-1199

## 适用条件

- 只适用于所引源码及实际构建条件；图为静态证据。
- 共享与私有对象、版本和只读条件必须分开。

## 边界与反例

- 低版本或提前返回路径不会走到同样的补丁处理。
- 单方核对不能充当两个消费模块的验收。

## 前提

- 版本、编译与对象分支符合所引入口条件
- 调用方维护对象/锁与重建协议

## 保证

- 共享谓词只返回序号比较结果
- 私有重验证在源码命中条件下设置有效性字段，未命中追平序号

## 不变量

- 共享和私有分支不能互相代替
- 原子序号不是目录快照或完整并发正确性的证明

## 证据

- [server/src/gausskernel/optimizer/sqlpatch/sqlpatch.cpp:751-761](../evidence/7ced453b49f5ca23cea6ac30.html)
- [server/src/gausskernel/optimizer/sqlpatch/sqlpatch.cpp:763-830](../evidence/dbc6055eb075df790bab974e.html)
- [server/src/common/backend/utils/cache/plancache.cpp:845-930](../evidence/e91bf5e1389b1a1b22d86e40.html)
- [server/src/gausskernel/process/globalplancache/globalplancache.cpp:556-626](../evidence/fb8352b3479aada5fc3f35aa.html)
- [server/src/gausskernel/process/globalplancache/globalplancache.cpp:628-660](../evidence/d7b64e7b30eb4b2b4b501a19.html)
- [server/src/gausskernel/process/globalplancache/globalplancache.cpp:690-780](../evidence/a23009aaae59df391bf32e68.html)
- [server/src/common/backend/utils/cache/plancache.cpp:1000-1080](../evidence/c1c84debb99d249aad2fea4e.html)

## 相关知识

- [DEPENDS_ON · CheckRecreateCachePlanBySqlPatch 的判定条件与语义边界](234a0c4e1b022361a8f381df.md)
- [DEPENDS_ON · RevalidateGplanBySqlPatch 的快速返回、目录/QueryIsPatched 判定与失效后续处理](1fa951c5675aa482ac23bb12.md)
