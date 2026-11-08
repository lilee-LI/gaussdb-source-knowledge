# 测试：同 seed 同序列的可复现性与跨架构边界

openGauss · content-addressed · linux-native

审阅状态 依赖已变化，待复核

测试义务（未运行）：在同一构建下用相同 Geqo_seed 与相同调用序列重复初始化并调用 geqo_rand/geqo_randint，比较序列是否一致；再用不同 seed 对照。预期依据：geqo_set_seed 清零后复制 double 低 6 字节到 random_state，geqo_rand 用 erand48；默认 seed=0.0 是固定初态而非关闭随机。最近反例：跨架构不承诺位级一致，因此该测试只能限定在同一构建/同一平台；若观察到跨平台差异，不构成缺陷。执行状态：not_run。

## 适用条件

- 同一构建与平台
- 相同 seed 与相同调用序列

## 边界与反例

- 不同 seed 序列相同才异常；默认 seed=0.0 不等于无随机

## 测试预期来源

- {"kind":"claim","ref":"claim:seed-determinism"}

## 执行状态

- not_run

## 证据

- [server/src/gausskernel/optimizer/geqo/geqo_random.cpp:1-40](../evidence/1d200fe9e16cf462fadc00ff.html)
- [server/src/include/optimizer/geqo_random.h:1-39](../evidence/0dc76bbb048c941a9c0385d9.html)

## 相关知识

- [VERIFIED_BY · claim：seed 只保证同构建同序列的可复现性边界](266f4a86d5cf54a512ac37b9.md)
- [测试预期依据 · claim：seed 只保证同构建同序列的可复现性边界](266f4a86d5cf54a512ac37b9.md)
