# 错误码完整学习的任务与交付契约

在工程根目录运行；大写占位值替换为实际返回值。详细项目初始化与源码提取见纯源码手册（旧版资料）。本方法是新的严格研究档位，**显式选择** error-causal/v1；旧任务不会因更新规则自动变成完整学习。

## 创建任务

先固定配置的源码提交和已提取文件，用 discover 找到候选对象：

```text
python -X utf8 scripts/dbknowledge.py --project PROJECT study discover --domain errors --paths SOURCE_PATH
```

request.json：

```json
{
  "contract": "research-request/v1",
  "execution_profile": "source_only",
  "analysis_contract": "error-causal/v1",
  "source_closure_required": true,
  "applicability_required": true,
  "goal": "完整学习目标错误家族的正常机制、多分支成因、现场判别与有条件措施",
  "primary_domain": "errors",
  "supporting_domains": [],
  "object_version_ids": ["替换为实际对象版本ID"],
  "dependencies": [],
  "knowledge_refs": []
}
```

辅助领域按实际因果依赖选择，不要为了显得全面一律增加。单任务只能绑定一个明确快照。完整错误家族涉及多个点时选入对应对象，研究过程中发现新点则修订范围/另建任务，不将其偷偷算作已学。

```text
python -X utf8 scripts/dbknowledge.py --project PROJECT study plan --input request.json
python -X utf8 scripts/dbknowledge.py --project PROJECT study claim --worker WORKER --task TASK_ID
python -X utf8 scripts/dbknowledge.py --project PROJECT study context --task TASK_ID
```

context 提供冻结方法、源码锚点、问题及 result_template。保留返回的租约 token；读取冻结方法再展开源码。初始锚点不够就沿真实调用/数据流补充精确证据。不要虚构哈希或 quote。

## 研究交付物

study-result/v1 保留既有问题/claims/evidence/domain_findings/source_analysis，另增加 error_analysis。所有 claim/evidence ID 必须指向本研究真实的源码；后者的独立 schema 为 [error-causal-v1](../../../contracts/error-causal-v1.schema.json)。

| 字段 | 内容与主要门槛 |
|---|---|
| identity | 码/状态的中文解释及映射 bound/alias_only/unresolved，限制与证据 |
| searches | 编号、消息、SQLSTATE、包装层、调用者五轴的真实检索范围与限制 |
| sites | 正常机制、完整谓词、级别、副作用、清理，分析/开放状态 |
| causes | 检测点、输入/状态源头、逐步链、前提、竞争原因与区分事实；假设明确缺口 |
| scenarios | 入口/条件/现象/易混淆点、改变判断的事实、判别/措施引用和当前状态 |
| discriminators | 支持/排除哪些原因，具体采集，正/负/未知条件和归因边界 |
| collections | 命令或材料请求、位置/身份/权限/时段/产物/代价/空值失败解释，not_run |
| actions | 场景/原因、类别、前提/排除、操作、语义约束/影响/权限/回退/失败出口和复验，not_run |
| cases | 显式绑定原因和场景；触发、最近正常、竞争原因或错误措施案例及源码推导，not_run |
| coverage | 每个声明检测点恰好一行；covered/open/out_of_scope 及关联和下一步 |
| field_conclusion | 固定 not_assessed，不能从源码推出客户事实 |

空模板不能提交。字符串的内容质量需审阅，不能用“无/已检查”等占位通过实质审查。允许有假设和无安全动作，但必须如实保留缺口；开放点不能计 covered。covered 仍只是声明范围内覆盖，并非全仓穷尽。

完整新任务还包含结果顶层 `error_applicability`，按[适用性契约](../../../contracts/error-applicability-v1.schema.json)记录条件组合、八域依赖、点/成因/采集/动作的逐组合覆盖、传播恢复与反例。创建完整任务会自动启用 `applicability_required`；不能显式关闭以绕过。历史冻结任务无此字段时保留原契约。详细研究方法见[适用性规程](../../../references/error-applicability.md)。

可处理场景须有源码支持的原因、判别及已准备的采集和措施；未知采集不能支撑此状态。每个已支持原因须有自己的触发和最近正常案例；每个可处理场景须有错误措施反例。措施至少提供检测条件与业务语义两个层次的复验标准。缺前提或业务语义不明时不能输出 ready action。

公开合成样例（旧版资料）展示同一点两条成因及对应规程。它是测试契约的虚构实现，不是 GaussDB/openGauss 知识、实验结果或可直接提交的真实学习成果。

## 检查、提交与实际审阅

```text
python -X utf8 scripts/dbknowledge.py --project PROJECT study inspect --task TASK_ID --input result.json
python -X utf8 scripts/dbknowledge.py --project PROJECT study submit --task TASK_ID --worker WORKER --token LEASE_TOKEN --input result.json
python -X utf8 scripts/dbknowledge.py --project PROJECT study review --task TASK_ID --input review.json
python -X utf8 scripts/dbknowledge.py --project PROJECT study report --task TASK_ID
```

inspect 只检查结构/引用/绑定，不接受成果。review.json 用返回的 result_sha256 作 subject_sha256，reviewer 为实际审阅者，mode 如实写 self_reviewed/independent_review，checks 完整取自 context.review_checks，每项写具体 finding。任何 fail 时 decision 必须 reject。新增九项错误因果检查见[质量标准](error-learning-quality.md)。不要自动生成 pass 来代替阅读与推理。

## Wiki 编译

```text
python -X utf8 scripts/dbknowledge.py --project PROJECT study template --task TASK_ID --kind mechanisms --id ERROR_SLUG --title 错误码的原理与场景处理
```

接受后的模板附带 error_learning_refs，绑定本任务的真实 cause_ids/scenario_ids。正文显示对应 ID，便于核对；ID 出现不等于语义已合格。主文章应完整保留本范围原因导航；专题页面如只讲某些成因/场景，应显式缩小引用与范围并链接主文章。

绑定新版适用性任务的文章同时带 `error_applicability_refs=[{task_id, variant_ids}]`。允许文章选择已研究的部分组合，但须保留可读的适用范围与对应 V-ID；不能引用未知变体或删掉整个适用性绑定。文章审核增加 `error_applicability:reader_scope`，检查条件、节点与跨域影响是否准确。标识可见性只是结构检查，不替代正文审阅。

文章保留 source_only 的 learning_presentation 六段顺序，可设置如下标题：

1. 这个错误是什么意思（编号/SQLSTATE/消息和影响范围）。
2. 先理解这些术语（正常操作与使用入口）。
3. 原因、场景与处理（根因树、原因导航、最小判别顺序、每场景采集和有条件措施）。
4. 源码推导案例（触发/最近正常/错误措施，全部未执行）。
5. 适用边界与未闭合问题（版本/构建/开放点）。
6. 源码依据（逐条关联研究与精确锚点）。

长场景可拆页，但主文必须可独立定位原因和下一步，源码依据放末尾。source-add、submit、review、stage、publish、release 命令继续按纯源码手册执行；文章增加四项因果审阅，保留 validation_status=not-run、validation_refs=[] 和 build_correspondence=unknown。

## 安装与迁移

主工程更新后重新执行 scripts/install_skills.py 安装本机路由。独立 database-source-only-knowledge 包携带相同错误研究方法、契约、工具和合成测试，仍禁止运行验证。历史冻结任务/发布版本保留原字节，不改写其状态。新版方法只有在新规划任务中冻结、实际执行并审阅后，才构成该任务的学习记录。

## 新完整研究的源码闭合扩展

完整新研究设置 source_closure_required=true，context 生成 error_analysis.source_closure。按[闭合规程](../../../references/error-source-closure.md)记录候选处置、入口/状态写者/护栏/清理/领域义务，causes 引用 obligation_ids。未决候选或必要义务未闭合时使用 partial，不能声明范围内完成；开放依赖不能支撑就绪场景。identity.sqlstates 允许空列表，mapping_limitations 解释未找到、未设置或不适用。历史任务维持原合同范围。
