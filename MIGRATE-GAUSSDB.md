# 迁移到 GaussDB：2.4 使用手册

推荐直接在当前 Claude Code 中执行；无须工程再调用一个模型，也不用先安装 MCP。完整提示词见 [CLAUDE-START.md](CLAUDE-START.md)。这份手册给出同一流程的完整命令。

## 准备输入

Windows 协调端/成员：64 位 Python 3.12、Git、已有可用的 Claude Code。工程完整解压，包含 wheels；首次助手从包内离线安装核心依赖。不复制其他机器的 .venv、模型认证或 openGauss 知识库充当 GaussDB 知识。

- source：完整稳定源码。源码路径不会触发重新下载。
- manual / design：目录或文件；UTF-8 Markdown/TXT/HTML，以及 DOCX、可提取文本的 PDF。CHM 先导出 HTML 并转 UTF-8，扫描 PDF 先 OCR；提取失败会保留原件与问题。
- features：UTF-8 TXT（一行一个名称）、CSV 或 JSON；仅名称也可，建议 id/name/aliases/version/module_hint。原始行、重复及歧义不丢弃。
- compile_db：原始 compile_commands.json；Linux 路径在 Windows 用 path_maps 映射。它只是构建上下文，尚未生成调用图也能学习。
- home：独立学习目录，不能与输入材料重叠。设计、手册、历史清单、编译数据库、图均可按实际缺失省略。

复制 paths.example.json 到 local/paths.json。可选增加 design；已有图增加 index_db、run_id（多 run 时指定）、graph_storage: reference。自定义模块边界可填 module_prefixes，课程默认24文件/240KB一包，可通过 curriculum.max_files/max_source_bytes 设置；单文件内部按区间续读。

## 当前 Claude 内执行

粘贴启动说明，或安装一次入口：

```powershell
python -X utf8 E:/kb/engine/scripts/install_claude_skill.py
```

安装的是 skill 和两个具名原生 Agent 定义，不安装客户端或修改模型配置。之后可说：

```text
/gauss-knowledge 配置=E:/kb/engine/local/paths.json。先规划全仓并展示计划。
/gauss-knowledge 并行学习 optimizer、executor，各自按模块计划研究、审阅并汇总。
```

当前会话读取 canonical skill；真正的子 Agent 由宿主 Agent 工具创建。软件只分配原生任务、私有租约和独立会话，不复制模型输出成另一套状态。没有 Agent 工具时明确串行。

## 同一助手的命令行

以下 Windows 命令可直接执行。Python 首次可用 PATH 上的 Python 3.12，助手会离线准备工程 .venv。P/S/C 只是减少重复输入的路径变量：

```powershell
$P = 'E:/kb/engine/scripts/claude_session.py'
$C = 'E:/kb/engine/local/paths.json'
$S = 'lead-session-01'
python -X utf8 $P --paths $C --session $S init
python -X utf8 $P --paths $C --session $S plan
python -X utf8 $P --paths $C --session $S modules --query optimizer
python -X utf8 $P --paths $C --session $S inputs
```

plan 返回可打开的 curriculum/index.html、PLAN.md、PLAN.json、工作包CSV和全仓覆盖账。初始课程是待核候选；不是已学知识。

单模块串行：用 modules 返回的完整 ID，随后始终沿用同一 session：

```powershell
python -X utf8 $P --paths $C --session $S next --module 'server/src/gausskernel/optimizer/geqo'
python -X utf8 $P --paths $C --session $S context
python -X utf8 $P --paths $C --session $S read-plan --limit 20
python -X utf8 $P --paths $C --session $S assets --offset 0 --limit 30
python -X utf8 $P --paths $C --session $S implementations --module 'server/src/gausskernel/optimizer/geqo'
python -X utf8 $P --paths $C --session $S features --module 'server/src/gausskernel/optimizer/geqo'
```

不要照抄示例模块 ID 到不同目录的 GaussDB；以实际 modules 结果为准。Agent 按 skill 用 read/search 真正读冻结证据，unit/progress 保存知识与覆盖，submit 提交问题覆盖。JSON 格式见 [formats](skills/gauss-knowledge/references/formats.md)。普通文件 Read、搜索命中及 read-plan 不产生研究阅读回执。

盘点确认所有文件，未学的 deferred。深学需解释 CPP 区间，不能以读完当学懂。通过 curriculum-refine 调整尚未执行的机制分组，必须保留所有模块资产。

原生并行由父会话运行：

```powershell
python -X utf8 $P --paths $C --session $S batch --module optimizer --module executor --parallel 3
python -X utf8 $P --paths $C --session $S batch-status --batch '<返回的批次ID>'
python -X utf8 $P --paths $C --session $S batch-next --batch '<返回的批次ID>'
```

只对新 handoffs 用宿主 Agent 启动；将其 session/context_command 和 skill 传入。children/resume_candidates 用真实 Agent ID 续接，不能重复启动。batch-attach 保存真实宿主 ID；batch-close --release 释放本批仍拥有的租约，宿主负责停止旧 Agent。子会话不 init、不复制 token、不自造审阅身份。

## 审阅、产物与使用

不同实际会话用自己的 session init 到同一配置审阅。当前作者自审需 --self-review，两阶段均保留 self_reviewed；另一 AI 会话不等于人工专家。

```powershell
python -X utf8 $P --paths $C --session 'review-session-01' init
python -X utf8 $P --paths $C --session 'review-session-01' review --task '<任务ID>'
python -X utf8 $P --paths $C --session 'review-session-01' review --task '<任务ID>' --accept '<研究digest>' --notes '实际核对的源码条件、引用及缺口'
# 有知识正文时，读取返回的 units/evidence，再接受新的知识提案 digest
python -X utf8 $P --paths $C --session 'review-session-01' review --task '<任务ID>' --accept '<新的知识提案digest>' --notes '实际知识审阅意见'
python -X utf8 $P --paths $C --session $S wiki
python -X utf8 $P --paths $C --session $S ask --role coding --module '<完整模块ID>' --question '修改入口会影响哪些状态和消费者？'
python -X utf8 $P --paths $C --session $S ask --role test_generation --module '<完整模块ID>' --question '边界、反例、预期来源和未测分支是什么？'
python -X utf8 $P --paths $C --session $S ask --role review --module '<完整模块ID>' --question '需检查哪些不变量、资源清理和依赖？'
python -X utf8 $P --paths $C --session $S ask --role operations --module '<完整模块ID>' --question '哪些观测和配置可区分问题？何时采取措施？'
python -X utf8 $P --paths $C --session $S coverage --module '<完整模块ID>'
```

没有已发布知识时无法导出知识 Wiki。四角色字段不足返回 partial。coverage 检查完整文件、CPP解释、特性、主干、两端契约、未知及四角色内容；它不会自动审阅或证明模型全部正确。verify-uses 使用实际查询检查 required_units 与必需字段，数据库测试仍单独记未运行。

材料变化：start --refresh（或 init --refresh）创建新绑定；旧 session 保留，创建新 session 研究新快照。不能把 openGauss 结论直接批准为 GaussDB 事实。

## ECS 产图与 Windows 回放

本工程自带产图程序。需真实 Linux 构建环境、原始 CDB、生成头文件、对应 GCC/Clang；GCC 需匹配插件开发头。生产端要求见 [ECS 操作](CALLGRAPH-REPLAY.md)。

```bash
cd /opt/gaussdb-source-knowledge
sh ecs.sh doctor
sh ecs.sh build --source /data/GaussDB --compile-db /data/compile_commands.json --work /data/graph-work --output /data/graph-handoff --jobs 8 --facts calls --frontend auto
```

Windows 的 `graph-job` 也能输出该交接脚本：

```powershell
python -X utf8 $P --paths $C --session $S graph-job
```

将 graph-handoff 的 knowledge.sqlite3、run.json、随附 blobs 和匹配源码交给协调端。Windows 使用原文件只读挂接；不逐成员复制完整图。若 Windows 是协调端，完整图文件仍需在它可读的本地/挂载路径，目前没有自动远程 ECS 图服务。也可在 Linux 做协调端再发模块包。图未覆盖的条件和部分 TU 诊断继续保留，不能通过 CDB 文件存在宣称解析通过。

## 多服务器模块学习及中央汇总

协调端先规划课程，再按**完整模块 ID**分工：

```powershell
E:/kb/engine/kb.cmd --home E:/knowledge/gaussdb team assign --module '<完整模块ID>' --worker member-a --kit E:/exchange/module-a.zip
```

成员接收同版工程和模块包，独立目录学习；不再从全源码另建不相干项目：

```powershell
E:/kb/engine/kb.cmd --home E:/member/module-a team open --kit E:/exchange/module-a.zip
python -X utf8 $P --home E:/member/module-a --session member-session init --worker member-a
python -X utf8 $P --home E:/member/module-a --session member-session next
# 也可 batch --module '<完整模块ID>' --parallel 3；仍使用返回的原生子会话
E:/kb/engine/kb.cmd --home E:/member/module-a team export --task '<已提交的真实任务ID>' --out E:/exchange/result-01.gz
```

协调端导入，进行研究及知识两阶段真实审阅；再推进任务并同步：

```powershell
E:/kb/engine/kb.cmd --home E:/knowledge/gaussdb team receive --input E:/exchange/result-01.gz
# 用上述 review 完成实际审阅
E:/kb/engine/kb.cmd advance --paths E:/kb/engine/local/paths.json --max-tasks 8
E:/kb/engine/kb.cmd --home E:/knowledge/gaussdb team feedback --order E:/exchange/module-a.order.json --out E:/exchange/feedback-01.gz
E:/kb/engine/kb.cmd --home E:/member/module-a team sync --input E:/exchange/feedback-01.gz
```

续学任务由协调端 advance 后反馈同步；本地未协调的新课程/任务会明确拒绝回收，先在协调端协调。签名检查快照、计划、真实成员/子代理、任务范围和知识基线，重复接收幂等，冲突不会覆盖已审知识。缺少跨模块材料时，协调端 feedback 可增加 --include-asset '<冻结资产ID>'；这只补同版可读材料，不伪称补齐了图。

MCP 可直接使用 start 返回的 query.mcp.json。默认使用 get_context(task,query,module)，其余版本信息由工作区绑定；需要显式历史范围时仍可提供 snapshot/profile/run/revision。
