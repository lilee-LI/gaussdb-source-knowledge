---
name: source-memory-learning
description: Learn database memory contexts, allocators, ownership, pointer lifetime, cleanup and accounting from source. Use for context research, growth and OOM hypotheses or memory dependencies in other studies.
---

# 内存上下文专题研究

执行协议：unified-skill/v1。先读[共同协议](../../references/unified-skill-protocol.md)；本 Skill 只补充专业方法，任务、审阅和发布使用统一引擎。

根据本次具体问题选择引用核对、机制深化或范围内盘点。先读[专业手册](../../references/domains/memory.md)中适用的方法及[研究深度](../../references/common/research-depth.md)。旧手册里的执行命令只属于旧项目，不覆盖当前协议。

## 研究路径

1. 区分 context、业务对象、chunk、block、空闲/保留、原生堆、共享内存和 OS 页，明确线程/会话/事务/语句/缓存归属。
2. 从创建者追父子树、具体 allocator、参数、指针存放和别名；核对 SwitchTo 的内联替代及旧上下文保存/恢复。
3. 追实际分配入口、尺寸来源、类别/对齐、自由链表/大块、复用/淘汰和 realloc；方法表要落到具体实现。
4. 追最后合法使用与 pfree/reset/delete/回调，分别检查正常、取消、ERROR、事务 abort、线程退出和子树清理；外部资源另查 ResourceOwner。
5. 给 used/allocated/free/peak/RSS 建账本：生产者、header/子树/空闲是否计入、更新/重置/同步；逻辑释放、allocator 保留与 OS 还页分别判断。
6. 比较缓存高水位、生命周期过长、遗漏回收、悬空引用和业务积压；用同负载多轮及预期清理点区分，不能凭曲线形状定性。

## 专业判断

SwitchTo 不代表搬迁或释放；Reset/Delete 子树行为以本实现为准。RSS 未降不证明泄漏；OOM 要区分请求规模、尺寸计算、限额、allocator、系统约束与并发峰值。

## 依赖与交付

统计加载 views，OOM/断言加载 errors，重排内存加载 decoding，批量/并行负载加载 tools。必要依赖写具体问题和依据；未知段保留 unknown，关系链接不能补全未读因果段。

| 结果章节 | 应有内容 |
|---|---|
| ownership_and_lifetime | 所有者树、指针关系、生命周期和使用前提 |
| allocation_and_cleanup | allocator、尺寸/复用、正常异常清理和外部资源 |
| accounting_and_growth | 指标账本、增长竞争假设、区分实验和未知范围 |

## 充分性挑战

对清理后占用未降或事务结束仍增长，能否从所有权和指标口径解释，或提出有效区分观测？缺失回收/观测路径保留 gaps，不能用常识补全。

## 统一交付

专业表格保持结构，按[专题合同](../../references/unified-topic-contract.md)写入 topic_extensions.memory；事实、契约、路径和测试仍使用统一对象及证据。分层必检字段由 `adapters/unified-skill-profiles.json` 登记，提交前执行专题合同检查。

开发需知道修改前提与消费者，测试需有边界/最近反例及预期来源，review 需能核对不变量、清理、并发和缓存影响。现场诊断只在相关任务中展开。当前 source_only，运行计划和推导案例保持 not_run。旧研究保留原方法与审阅身份。
