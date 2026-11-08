# 当前会话 JSON 格式

以下是形状示例，替换每个 ID、问题、证据和内容。不要把占位 ID 写入工作区。返回 `id` 的实际冻结阅读才提供可引用 evidence；普通文件读取/搜索不提供回执。

## 机制学习

`unit.json`：

```json
{
  "id": "claim:<模块>:<稳定主题>",
  "kind": "claim",
  "title": "具体实现结论",
  "statement": "在这些条件下，代码产生这个行为。",
  "body": "## 行为和入口\n具体证据支持的说明。\n\n## 状态和消费者\n字段的生产和消费位置、条件、跨模块影响。\n\n## 开发与 review\n修改需要维护的约束与清理路径。\n\n## 测试与未知\n预期依据、反例、未核实的宏/间接调用。",
  "conditions": ["具体输入/版本/配置范围"],
  "counterexamples": ["最接近而不满足结论的情况，或当前证据的边界"],
  "source_refs": ["evidence:真正读过的ID"],
  "symbol_refs": [],
  "knowledge_refs": [],
  "runtime_validation": "not_run"
}
```

- 通用字段 `id/kind/title/body/conditions/counterexamples/source_refs/symbol_refs/knowledge_refs`。
- kind: module、responsibility、feature、mechanism、claim、contract、flow、test_obligation、requirement、observation、decision。
- claim 必须有 statement、证据、条件、反例；requirement/contract 也需证据、条件、反例。产品结论不能只引用方法文件。
- feature/responsibility 使用 level=1..4、parent；先暂存上级。L1 可无 parent，L2 必须引用同 kind 的 L1，逐级类推。源码目录归属不表示已批准组织责任。
- knowledge_refs 是对象数组，例如 `[{"relation":"DEPENDS_ON","target":"claim:已存在的ID"}]`，不能写字符串。目标需当前草稿或适用的已审知识。
- test_obligation 必须有 `expected_from: {"kind":"claim","ref":"claim:真实结论ID"}`，也可用 requirement/contract/source_prediction；ref 指向实际依据。`execution_status="not_run"`，描述测试建议和预期不冒充实测。
- flow.steps 是有序对象数组，kind=call/data_stage/state_transition/async_message。source_only 使用 data_stage/state_transition；call 要真实 symbol/target 两端 ID，不能拿名字代替。source_only 不创建 contract，因为其 producers/consumers 需实际编译 symbol ID。
- 不写 `_binding`、review、content_hash 等保留字段。每项至多80KB，分批研究。

## 资产、线索和机制提案

初次模块盘点可只提交 progress，不必强行产出知识。所有尚未深学的资产用 deferred；inventory_complete 只代表逐项归属/计划完成，不能代表已经学完。

```json
{
  "inventory_complete": true,
  "assets": [
    {"asset":"server/<真实路径>","disposition":"deferred","reason":"已盘点，具体状态机制待下轮深学","evidence_refs":["evidence:实际阅读"],"unit_ids":[]}
  ],
  "leads": [],
  "proposals": [
    {"id":"稳定的局部机制ID","title":"按行为归并的机制","question":"一个可回答的边界问题？","owner_module":"完整模块ID","reason":"为什么值得单独研究","evidence":[{"asset":"server/<真实路径>","start":1,"end":20}],"depends_on":[]}
  ],
  "contracts": [],
  "gaps": [{"question":"具体还缺什么？","reason":"为什么当前证据不足"}],
  "templates": []
}
```

盘点线索用 `leads:[{"candidate_id":"真实ID","state":"research","proposal_ids":["局部机制ID"],"reason":"机制归并理由","evidence_refs":["实际覆盖候选位置的证据"]}]`。其他 state：mapped（需 unit_ids）、excluded、deferred；未处置的候选保留在覆盖缺口，不能声称已清零。

深度研究可用 `assets:[{"asset":"真实ID","disposition":"partial","reason":"本轮解释这些实际区间","evidence_refs":["实际证据"],"unit_ids":["已暂存/已审的知识ID"]}]`。完整已读并有对应知识才用 studied；实现文件不能充当 supporting。范围未读全时不写 inventory_complete=true。

proposals.evidence 区间必须在本租约完整读过；owner_module 取任务 bundle.module。depends_on 只能是真实同批 proposal ID 或候选 ID，不猜函数依赖。公共机制/跨域任务用任务 bundle.program_item 对应的 templates，参照 context.whole_learning，不套用 module_survey 示例。

更新 progress 用上一次返回的 `--previous-digest`；它合并列表同语义键条目，不能误删此前真实盘点。修改 unit 用 `--previous-hash`；可以通过 context/drafts 恢复。

## 提交问题覆盖

`coverage.json` 是**数组**，不是包在 coverage 字段里的对象：

```json
[
  {"question":"本任务的实际问题","status":"answered","explanation":"哪些源码/手册支持什么结论","evidence_refs":["evidence:实际阅读"]},
  {"question":"尚未核实的边界","status":"open","explanation":"缺少什么证据，下一步去哪里核对","evidence_refs":[]}
]
```

status 只能 answered/open/not_applicable。answered 必须有本租约真实阅读证据。not_applicable 需具体理由，不能把“没找到”写成不适用。stage 是暂存，submit 是提交，review 两个阶段才接受知识；这三件事分开描述。
