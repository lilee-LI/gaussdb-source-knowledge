# 完整开源工程选型复核

日期：2026-11-07。范围：公开仓库、许可证、发布记录、关键实现及公开评测的核查。本轮没有安装候选平台、调用模型、迁移知识库或执行 openGauss/GaussDB 的候选平台效果测试。

## 结论与调整

存在可直接部署或安装、具备完整工作流的源码知识工程，不能把它们仅当作 Wiki 生成器或零散组件。之前将通用任务、知识发布和检索控制面作为自研主平台推进得过早。

后续优先采用一个上游维护的主工程。**OpenDeepWiki 是完整产品的优先试用对象，CodeWiki 是源码研究流水线的完整对照，Potpie 是持久知识与 Agent 召回路线的候选。三者是选型路线，不是同时组合进一个新系统。** 暂停扩展本仓的通用平台功能；现有源码索引、证据方法、软件测试和评测材料保留作资产与对照。

本轮没有找到足以证明某个候选已经同时满足“500 万行 C++、真实宏配置、数据库四专题深度学习、有效召回、增量一致性”的公开证据。完整产品可以成为底座；目标场景是否达标必须另验。此结论不是断言市场上不存在满足要求的工程。

RAGFlow 不再预设为必选组成部分。主平台本身若能完成知识查询，就先使用它的原生查询路径。只有实测揭示具体缺口时，才考虑扩展，不能为了保留已写代码而继续增加系统。

## 版本与维护状态

以下 SHA 为本轮通过 GitHub tree API 核对的 main 快照；发布记录与 main 功能分开记录。Star 数未用作能力或成熟度证明。

| 候选 | 审阅快照 | 许可证与发布记录 | 维护判断 |
| --- | --- | --- | --- |
| [OpenDeepWiki](https://github.com/AIDotNet/OpenDeepWiki) | `7aa53b8427994da27d0bc44e35553f47fec83a33` | MIT；最新查询到的 GitHub Release 为 v2.0.6，2026-09-08 发布 | 有产品前后端、后台任务、测试和版本发布；仍需生产场景验收 |
| [CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki) | `a1b9f4acac4d3e1925c9d49e258b618741410540` | MIT；README 标示 2.0.0，GitHub Releases 查询只返回 assets，不把徽章当作发布证明 | 有论文、评测和工程流水线；运行应固定具体提交 |
| [Potpie](https://github.com/potpie-ai/potpie) | `dab237c8c3f4b887338ad0e21fc6d25db86824b4` | Apache-2.0；v2.0.1 于 2026-08-31 发布 | 当前为本地优先 CLI/daemon/Context Graph 路线，不能沿用旧版平台架构介绍 |
| [DeepWiki-Open](https://github.com/AsyncFuncAI/deepwiki-open) | `10e1be1c15f98a902bf14d0da07d806d024cc6d0` | MIT；本轮 GitHub Releases 列表为空 | 源码仍维护；README 推广 Grok-Wiki，不能将下载产品能力自动归入开源树 |
| [CodeBoarding](https://github.com/CodeBoarding/CodeBoarding) | `de42aa23829fe5cd570edfec91cad8b615b17f40` | 分析引擎及 CLI 为 MIT；v0.14.2 于 2026-09-16 发布 | 架构分析与增量文档工作流完整；C++/CUDA 仍标注 preview |

## OpenDeepWiki：优先验证完整产品

[README](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/README.md) 中已有 Git/ZIP/本地目录导入、目录规划、文档生成、后台任务、管理后台、问答、MCP、增量更新；.NET 10 后端、Next.js 前端，SQLite/PostgreSQL，提供 Compose。能大幅替代我们自建通用前端、队列、模型配置、文档管理和问答入口的工作。

关键源码核查：

- [WikiGeneratorOptions.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/src/OpenDeepWiki/Services/Wiki/WikiGeneratorOptions.cs)：默认每页源码工具调用预算为 6、目录源码调用预算为 4；目录树深度 2、最多 1,200 个树节点、每目录最多 20 个文件。这些是特定环节的预算，不能误称为整个仓库只能处理 1,200 个文件。
- [WikiGenerator.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/src/OpenDeepWiki/Services/Wiki/WikiGenerator.cs)：内容生成提示要求重点读取 2–4 个文件，预算达到后写出文档。当前生成工具为源码工具、文档工具和 Skill 快照；这里没有直接注册聊天端的外部 MCP 工具。因此“聊天已支持 MCP”不能推导为“编译图已参与学习”。
- [ChatAssistantService.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/src/OpenDeepWiki/Services/Chat/ChatAssistantService.cs)：聊天实际加入文档读取工具、选中的 MCP 工具和 Skill 工具。
- [ChatDocReaderTool.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/src/OpenDeepWiki/Agents/Tools/ChatDocReaderTool.cs)：通过文档目录选页、按行读取。这证明了一条 Agent 文档查询路径，不等于验证了大型知识集的语义召回率。
- [RepositoryAnalyzer.cs](https://github.com/AIDotNet/OpenDeepWiki/blob/7aa53b8427994da27d0bc44e35553f47fec83a33/src/OpenDeepWiki/Services/Repositories/RepositoryAnalyzer.cs)：Git 输入支持增量更新；ZIP/普通目录不能一概视为同样的 Git 增量流程。

判断：产品完整度最接近“直接用一套”。默认学习深度不足以直接证明数据库机制充分性；没有查到可核验的 500 万行 C++ 同场景容量与问答基准。先验证原生能力，具体失败再决定是否通过现有扩展点加入源码事实工具和专题规则。

## CodeWiki：优先验证完整学习流水线

[README](https://github.com/FSoft-AI4Code/CodeWiki/blob/a1b9f4acac4d3e1925c9d49e258b618741410540/README.md) 已有依赖图、递归模块划分、模块 Agent、父子文档生成、构建材料、增量更新、HTML 输出，以及 CLI/MCP 模式。它已经承载了此前讨论的相当一部分“构建学习任务”的职责，不能把这部分重复作为全新引擎开发。

[MCP 模式](https://github.com/FSoft-AI4Code/CodeWiki/blob/a1b9f4acac4d3e1925c9d49e258b618741410540/guides/mcp-ide-mode.md) 可由宿主 Agent 提供推理，工具提供分析、读取、模块树和写文档；大型中间结果走文件路径，避免全部塞进 MCP 返回。

关键限制来自实际 [C++ 分析器](https://github.com/FSoft-AI4Code/CodeWiki/blob/a1b9f4acac4d3e1925c9d49e258b618741410540/codewiki/src/be/dependency_analyzer/analyzers/cpp.py)：使用 Tree-sitter；解析失败时通过移除某些 ALL_CAPS 修饰/独立宏行恢复结构。这是语法恢复，不是按 compile_commands 展开宏，也不能据此证明目标构建中的调用绑定。

公开评测中，作者在七个仓库、486 项文档要求上用同一 LLM judge 评定加权文档得分。Wazuh 的基准 LoC 为 1,446,730，2.0 得分 88.14；Electron 为 184,234，得分 71.59。数字来自同一 README，明确属于作者的文档评测，不是 C++ 图准确率、实际知识召回率、人工专家通过率或 500 万行 GaussDB 成绩。

判断：它是最值得对照的源码学习工程，尤其是任务拆分和持续生成。若主要入口是 Agent/CLI，它的适用性更高；不能自动把它视为已经具备团队知识平台的全部治理和检索能力。

## Potpie：完整的持久知识与 Agent 召回路线

[当前 README](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/README.md) 已提供本地安装、setup、daemon、工作区、图浏览、resolve/search/record、proposal/commit。它与“知识能沉淀、能有效取回，Wiki 非必需”的目标高度相关。

[查询文档](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/docs/context-graph/querying.md) 描述统一证据返回、词法/向量匹配、版本化引用、过期证据标记；[写入文档](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/docs/context-graph/writing.md) 描述 proposal/commit、冲突检查、事实与 Agent claim 的区分。这里的自动校验/批准协议仍不能直接等同于数据库专家审阅。

审阅的 [架构文档](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/docs/context-graph/architecture.md) 明确：Windows 默认 Ladybug 后端在操作时加载整个图，变更后事务写回。相应 [实现](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/potpie/context-engine/src/potpie_context_engine/adapters/outbound/graph/backends/ladybug_backend.py) 复用内存状态读取/写入。这阻止我们直接假定它适合装载现有数百万调用边；它用于较小的语义知识图是否合适需要单独测量。

[bench-plan](https://github.com/potpie-ai/potpie/blob/dab237c8c3f4b887338ad0e21fc6d25db86824b4/docs/context-graph/bench-plan.md) 自己声明是规划/参考材料，采用合成场景，非延迟吞吐、LLM 基准或生产真实数据等价证明。没有据此宣称完成了 C++ 500 万行验收。

判断：这是值得以整套工程试验的另一条路线，尤其能替代自研知识状态、来源与召回。当前仍缺目标源码规模证据，不与 OpenDeepWiki、CodeWiki 一起堆叠。

## 其他候选与淘汰理由

- **DeepWiki-Open**：开源树确有完整生成和 RAG 查询。当前 [pipeline.py](https://github.com/AsyncFuncAI/deepwiki-open/blob/10e1be1c15f98a902bf14d0da07d806d024cc6d0/api/rag/pipeline.py) 使用文本分块与 Embedding，并跳过超过 81,920 token 的单文件；[rag.py](https://github.com/AsyncFuncAI/deepwiki-open/blob/10e1be1c15f98a902bf14d0da07d806d024cc6d0/api/rag/rag.py) 使用 FAISS 检索。直接使用时必须核验被跳过的数据库大文件和精确引用。列为体验对照，不凭流行度认定规模和机制精度。
- **CodeBoarding**：[README](https://github.com/CodeBoarding/CodeBoarding/blob/de42aa23829fe5cd570edfec91cad8b615b17f40/README.md) 明确 C++/CUDA preview 使用 clangd，可提供 compile_commands、compile_flags 或 .clangd；也披露类外成员和头文件模板的增量关系可能漏掉或过期。编译语义方向值得参考，但其主要交付是架构分析、图和文档，不能替代所有知识库职责。
- **GitNexus**：功能覆盖图、查询、MCP、Wiki，但当前 [LICENSE](https://github.com/abhigyanpatwari/GitNexus/blob/main/LICENSE) 为 PolyForm Noncommercial 1.0.0，README 提供商业授权入口。本项目的公司使用场景不能把它当作 MIT/Apache 等条件的直接替代项。
- **Bloop**：[仓库 API](https://api.github.com/repos/BloopAI/bloop) 返回 archived=true、最后 push 为 2024-12-04，不作为新建平台默认基础。
- **Sourcegraph**：核心产品仓库已转私有，见[创始人对该决定的说明](https://news.ycombinator.com/item?id=41298641)。scip-clang 等开源组件不能被表述成完整 Sourcegraph 产品仍开源可用。
- **RAGFlow**：完整通用知识检索产品，但目前选型关注源码学习端到端流程；不预设用它加自研工作流取代上述源码平台试用。

## 最小实测及停止条件

当前缺模型服务，本轮只完成静态选型审查。现有宿主 Agent 可以参与支持其模式的候选验证；涉及后台持续生成的候选仍需要实际可用模型配置。不能将模拟 HTTP、脚本返回或静态阅读冒充平台效果。

下一步在单独目录固定上游提交，先测试原生工作流，不改写核心：

1. **相同输入**：同一 openGauss 快照，先排序完整相关范围，再全仓；源码、设计和手册的计量及缺口分开。保留真实构建 profile，禁止借用另一 checkout 的证据。
2. **相同问题**：初选使用 40 道机制问题，覆盖特性、错误、内存、兼容、GUC，以及跨文件、宏、无答案和版本冲突。按机制拆分调参/验收集；小题集只用于淘汰明显不适合者，后续仍做独立的大题库验收。
3. **分开计分**：知识发现、关键证据召回、答案正确性、引用准确性、未覆盖项报告分别统计。不能只看页面数量和 LLM 自评分。
4. **规模测量**：盘点/索引/生成分别记录耗时、峰值内存、磁盘、模型 token 和失败恢复；再测查询 P50/P95、并发、更新成本。不将生成大量 Wiki 当作学习充分。
5. **四类更新**：源文件、公共头、编译宏、生成头变化；检查文档及调用关系是否过期、旧版能否回读。
6. **工程准入**：上游原生承担通用队列、知识/文档管理和查询入口；定制仅针对数据库专题方法、编译事实访问和必要的验证规则。若需要重写大部分规划、存储、检索或前端，就淘汰该路线，不把再次拼装称为采用成品。

选定后，在被选工程的 fork 或扩展中收敛维护。当前自研仓库中的通用平台可由上游替代；源码事实交付件与适用的评测、证据规则按需保留。真正的迁移以实测结果为依据。
