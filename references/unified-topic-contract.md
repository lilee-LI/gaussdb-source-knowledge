# 专题知识到统一对象的适配合同

合同：unified-topic-extensions/v1。基础对象继续采用 `contracts/unified-knowledge-proposal-v1.schema.json` 的 kind；不新增 module_page、tree_node、relation 等旁路类型。

## 一份事实，多种使用入口

| 专题 | 保留的专业结构 | 转成或引用的统一知识 |
|---|---|---|
| errors | 身份/检测点、正常与失败、成因和传播清理、场景判别及有条件措施；完整 error_analysis 可保留 | 逐检测点 claim、机制、flow、保护/恢复 contract、诊断 observation、测试义务 |
| compatibility | 输入绑定、条件分支、行为与最近反例的语义矩阵 | 条件 claim、实现 flow、文档 requirement、明确来源的测试预期 |
| memory | 所有权/寿命、分配/回收、统计口径与竞争假设 | 生命周期 contract、状态 flow、指标 observation、清理及失效测试 |
| guc | 参数定义、来源覆盖与生效、消费者和观测 | requirement/claim、设置→消费 flow、缓存/生效 contract |
| waits | 队列/状态、计时口径、取消与观测 | 状态 flow、同步 contract、计时 observation、取消/唤醒测试 |
| views | 定义/字段血缘、权限与一致性、字段语义 | 字段 claim、生产/返回 flow、采样 observation、权限/NULL 测试 |
| tools | 参数/阶段、快照与依赖、失败残留及重试 | 阶段 flow、事务/幂等 contract、错误关联、恢复与结果测试 |
| decoding | 事务快照、位点与确认层次、保留资源及重启 | 位点 claim、状态 flow、所有权/确认 contract、重复/遗漏测试 |

同一错误码的不同检测点、同名函数的不同签名、同名上下文的不同生命周期，先核对身份和条件，不按名称合并。专业结构可以挂在共同 mechanism/module 上，其他事实引用它，无需每个 claim 复制整套表格。

## 扩展格式

```json
{
  "id": "mechanism:example-memory",
  "kind": "mechanism",
  "title": "范围明确的内存机制",
  "body": "基于实际源码撰写正文。",
  "source_refs": ["evidence:0123456789abcdef0123456789abcdef"],
  "knowledge_refs": [],
  "topic_extensions": {
    "memory": {
      "contract": "unified-topic-extensions/v1",
      "depth": "reference",
      "scope": "此例只展示格式，不是产品知识",
      "coverage": [{
        "check": "ownership_and_lifetime",
        "status": "answered",
        "explanation": "实际解释所有者与有效期。",
        "evidence_refs": ["evidence:0123456789abcdef0123456789abcdef"],
        "knowledge_refs": []
      }],
      "details": {
        "ownership_and_lifetime": [{"owner": "示例占位，实际任务必须回查源码"}]
      }
    }
  }
}
```

此处 evidence ID 仅演示合法形状，不是已存在或已读证据。真实锚点仍由统一引擎创建和核验。

每个选中的专题按 registry 的深度提交检查项。answered 必须有解释、结构化 details 和证据或显式知识引用；not_applicable 要解释范围原因；open 要写 next_step。范围内盘点还须 scope_inventory，保留搜索范围、候选处置和遗漏，不能宣称范围之外完整。

所有 coverage/details 中的 evidence_refs 或 source_refs，必须是当前知识对象 source_refs 的子集；所有嵌套 knowledge_refs 必须已列入该对象的 typed knowledge_refs。这样现有证据依赖和知识依赖失效能覆盖专业表格。历史旧 evidence ID 不能只改字符串，需按冻结源与实际审阅重新绑定。

专业 details 保持对象或数组，不压成一段摘要。由专业结构生成可读正文、契约及测试义务；必要时保留原 error_analysis 等表格作为冻结文档证据，再引用它，不依赖活研究目录中的未登记路径。

旧 evidence_id / evidence_ids / source_ref 等引用字段须实际重绑后归一为 evidence_refs / source_refs，不能把旧 ID 原样藏进专业表。正文中的可识别 evidence ID 同样需要外层登记。自然语言因果是否依赖其他事实，仍由实际语义审阅判定。

## 检查与边界

`scripts/unified_skill_methods.py check --input proposal.json --request topic-request.json --method-plan method-plan.json` 检查方法绑定、基础 kind、专题深度、检查项、结构及引用登记。它不读取或修改知识工作区，也不接受知识。源文件真实性、实际读取、当前版本、构建范围及语义审阅继续经过统一引擎。

旧研究迁入时逐项决定复用、修订、保持未知或暂缓，保留旧结果与原方法身份。方法升级不追认旧知识符合新合同，当前内部完整母库也不自动转换成客户无源码输出。
