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

四角色需要实际结构内容，不能只把同一段正文回显为四种答案。按证据提供以下可选字段（同样必须纳入 source_refs 并实际审阅）：

- 开发：`state` / `state_transitions` / `resource_lifecycle` / `interfaces`，以及 `consumers` / `affected_modules`。source_only 可写源码支持的消费者说明和文件位置，不伪造编译 symbol ID 或正式 contract。
- Review：`invariants`、conditions、消费者及源码位置，明确哪些修改会破坏约束。
- 测试：实际 `test_obligation` 的 expected_from、conditions/cases/counterexamples，不把一句测试建议冒充 oracle。
- 运维：`operations` 对象内的 observations、diagnostics、configuration、actions；写可区分观测、收集依据、配置生效点及有条件措施。来源没有承诺的项保留未知，不为消除 missing_required 杜撰。

`K ask` 的 role_context 返回必需字段及缺口。缺设计/运行观察时保持来源与未运行边界。没有结构事实时 partial 是正确结果。

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

## CPP 实现区间和历史特性闭合

以下字段写在同一份 progress.json 中，并从 `implementations` / `features` 的实际查询返回取 ID。区间不是函数任务，适合一个功能/机制任务中同时处理多项。新的研究必须按该 attempt 读取证据，单纯看过一段代码不能证明解释完成。

```json
{
  "implementations": [
    {
      "item": "implementation:查询返回的真实ID",
      "state": "explained",
      "reason": "本区间完整阅读并由机制知识解释，具体边界已核对。",
      "analysis": {
        "behavior": "说明该区间实际实现的行为以及它所属的机制。",
        "conditions": "说明输入、构建宏、运行配置和调用前置条件。",
        "state": "说明创建、读写、变换的状态及其生命周期。",
        "consumers": "说明本模块或跨模块的消费者和影响范围。",
        "cleanup": "说明正常和异常出口的资源处理；无资源操作要给具体理由。",
        "test_basis": "说明正常和边界测试预期依据以及尚未执行的验证。"
      },
      "evidence_refs": ["evidence:实际覆盖整个区间的ID"],
      "unit_ids": ["mechanism:实际暂存或已审的ID"],
      "unknowns": []
    }
  ],
  "feature_mappings": [
    {
      "feature_id": "feature:查询返回的真实ID",
      "state": "mapped",
      "reason": "特性名、手册预期与真实实现范围经过源码证据核对。",
      "modules": ["本任务实际模块ID"],
      "unit_ids": ["mechanism:实际暂存或已审的ID"],
      "evidence_refs": ["evidence:本轮实际阅读的ID"]
    }
  ]
}
```

implementations.state 仅 explained/open；open 仍需 item 与具体 reason，不能伪造六项解释。explained 的六个 analysis 字段都要有具体说明，evidence_refs 必须覆盖该区间全部行并已被关联知识引用。unknowns 不为空会保留覆盖缺口；知识未入库或版本变化会显示 pending_knowledge，不能当作验收完成。

feature_mappings.state 可为 mapped/ambiguous/not_located/out_of_scope，每项都需要真实源码/手册证据和具体理由，modules 必须含当前调查模块。mapped 还必须关联真实机制知识。名称候选映射不等于已审知识，无法定位和歧义要继续作为缺口；不得为了清零把未知标成不适用。

## 提交问题覆盖

`coverage.json` 是**数组**，不是包在 coverage 字段里的对象：

```json
[
  {"question":"本任务的实际问题","status":"answered","explanation":"哪些源码/手册支持什么结论","evidence_refs":["evidence:实际阅读"]},
  {"question":"尚未核实的边界","status":"open","explanation":"缺少什么证据，下一步去哪里核对","evidence_refs":[]}
]
```

status 只能 answered/open/not_applicable。answered 必须有本租约真实阅读证据。not_applicable 需具体理由，不能把“没找到”写成不适用。stage 是暂存，submit 是提交，review 两个阶段才接受知识；这三件事分开描述。

## 原生子代理交接

`batch` / `batch-next` 的 `handoffs` 由工程生成，不由模型编造。每项包含独立的 session、worker、原生 task 摘要、paths/home、可直接执行的 context_command，以及 evidence_must_be_reread。租约 token 只留在本地私有 handle；交接 JSON、研究 JSON 和 Agent prompt 都不能带 token。父会话不为子代理重新 init、修改 worker 或复制 token。

`children` 是现有槽位状态，`resume_candidates` 是需要宿主核查/续接的已有 Agent；它们不是再次派发清单。只有新返回的 handoffs 才能开启新任务。`native_agent_id` 必须由真实宿主 Agent 工具返回，再用 batch-attach 登记；不把 session/worker/task ID 冒充宿主 Agent ID。

子代理仍使用本文 unit/progress/coverage 三种原生数据形状。progress.proposals 是研究提案，不能另造并行待办列表来代替。批次状态依据真实任务的 queued/leased/submitted/accepted 和已审知识计算；submitted 只表示待审。盘点的 inventory_complete 不表示所有 CPP 已解释，队列暂空也不表示全仓知识验收通过。

每个新的租约 attempt 都重新读取实际证据；原有草稿可当线索，旧 attempt 的回执不自动算本轮已读。根 Agent 与子代理的阅读回执互不替代。审阅者用自己的真实会话阅读审阅上下文、源码引用和对应 digest；作者审阅必须保留 self_reviewed，不能以批次关闭或子代理退出代替审阅。
