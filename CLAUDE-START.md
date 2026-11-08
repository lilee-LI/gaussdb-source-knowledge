# 直接在 Claude 中使用

在现有 Claude Code 会话中执行源码和手册学习。Claude 自己读、分析、写；工程 Python 助手负责全仓计划、任务状态、证据、入库、Wiki 和查询。**不用从外面调用 Claude，不需要配置 MCP，也不需要模型 SDK。**

准备好本机 Python 3.12、Git、已可使用的 Claude Code，以及完整工程（包含 wheels）。学习工作区与源码、手册、工程目录分开。没有设计文档、没有编译图也能开始；CHM 先解包为 HTML，扫描 PDF 先做 OCR。

## 方式一：直接粘贴，立即开始

无需先运行 PowerShell 命令。在 Claude 中粘贴下面整段，只替换四处路径：

```text
请读取 E:/kb/engine/skills/gauss-knowledge/SKILL.md，按这个 skill 在当前会话执行。

工程：E:/kb/engine
源码：E:/GaussDB/source
用户手册：E:/corpus/manual
学习工作区：E:/knowledge/gaussdb

先创建全仓学习计划，展示领域、模块、初始任务数和计划文件位置；然后从优化器中选一个小子模块，完成第一轮源码与手册盘点，给出按机制归并的后续学习计划。
当前只提供源码和手册，不生成编译索引，不解析 TU。
由当前会话执行，不运行 kb run、claude -p 或另起模型；保留真实证据和待审状态。
```

首次助手会从包内 wheels 准备 `.venv`，仅安装 Python 依赖；不会下载源码或安装 Claude。若 Claude 的工具权限阻止 Python/读写，按其权限提示处理；纯聊天且无本地工具的 Claude 网页窗口不能执行本机工程。

下一轮可以直接说：

```text
继续上面的任务。读取暂存和进度，沿用同一工作区；把机制与跨模块影响学清楚并提交待审。
```

需要本会话完成审阅和可查看的产物时：

```text
请核对刚提交的研究和源码证据，做真实自审；记录 self_reviewed，完成研究与知识两步审阅后导出 Wiki。
然后分别用开发、测试、代码 review 三个角色查询刚学的机制，给出结果和所有产物的路径。
保留未知条件和未运行测试，不冒充独立人工审阅。
```

第一轮若只有盘点和机制提案，就没有知识 Wiki；盘点通过后，继续领取一个机制任务，形成并审阅知识正文，才有 Wiki。

## 方式二：使用 `/gauss-knowledge`

**在本工程目录打开 Claude Code**：工程自带 `.claude/skills/gauss-knowledge/SKILL.md`，新会话直接输入：

```text
/gauss-knowledge 源码=E:/GaussDB/source 手册=E:/corpus/manual 工作区=E:/knowledge/gaussdb。先规划全仓，再学习优化器一个小子模块。
```

如果通常在源码目录或任意其他目录打开 Claude，就在当前 Claude 中说（只需安装一次）：

```text
请用 Python 执行 E:/kb/engine/scripts/install_claude_skill.py，安装本工程的个人 gauss-knowledge skill。
只安装 skill 入口，不改 Claude 的模型、认证或权限配置。
```

新会话里即可使用 `/gauss-knowledge`。该入口指向工程绝对路径，工程移动后重装入口；个人安装不复制客户端、不复制知识库。已有同名但不同入口时先查看差异，再明确替换。

常用输入：

```text
/gauss-knowledge 只展示全仓学习计划
/gauss-knowledge 继续当前模块，从已有草稿续学
/gauss-knowledge 审阅 task:实际ID，发现问题就退回
/gauss-knowledge 查询：修改这个优化器机制，还会影响执行器哪些状态？
```

新会话需要提供已有 `assistant-paths.json` 路径；使用 Claude 的 resume 恢复原会话可保留 session。另一会话不能接管尚未到期的活动租约；未到期且未提交时应由原会话 release，或等到期后重新领取和回读。

## 输出和原工程的关系

| 产物 | 位置及含义 |
| --- | --- |
| 全仓学习计划 | `HOME/whole/PLAN.md`、`PLAN.json`、`index.html` |
| 研究草稿和覆盖 | 同一个 `HOME/knowledge.sqlite3` 的任务/证据/暂存/覆盖账；辅助草稿文件在 `HOME/drafts/` |
| 已审结构化知识 | `HOME/knowledge.sqlite3`、`HOME/wiki.git` 的知识修订；不会另造一份孤立数据库 |
| Wiki | `HOME/wiki/index.html` 和修订目录下的 Markdown；只展示已审入库知识 |
| 开发/测试/review 上下文 | 通过 skill 查询同一已审知识，返回适用条件、消费者、测试预期依据、证据和缺口 |

源码和手册模式可形成源码位置/文本证据支持的关系。没有编译图时，宏配置、重载和间接调用保持待核；不会伪装成编译器确认的调用图。以后在 paths 中接入已有 ECS 图可继续图辅助研究，输入变更按现有版本绑定规则复核。

多人服务器协作仍用原有工作包和签名结果汇总，见[持续学习协议](docs/WHOLE-REPOSITORY.md)。本次当前会话助手绑定路径配置的协调端工作区；已解开的成员包继续使用原有 MCP/whole 操作，不对它重新初始化。外部批处理 `kb run` 仍可选用，与本入口共用状态，但本 skill 不调用它。

Claude Code 的[官方 skill 说明](https://code.claude.com/docs/en/skills)支持个人/项目 skill 与 `/名称` 调用。使用直接粘贴方式时不依赖 skill 自动发现，适合先试跑。
