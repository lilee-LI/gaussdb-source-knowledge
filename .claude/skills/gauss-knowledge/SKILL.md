---
name: gauss-knowledge
description: 在当前 Claude Code 会话中接入源码、手册、历史特性和编译数据库，规划模块功能课程，使用原生子 Agent 并行续学、审阅，输出 SQLite/Wiki 及开发、测试、review、运维知识，不另起 Claude。
argument-hint: "源码=<路径> 手册=<路径> 工作区=<路径>；或：计划 / 学习 <模块> / 继续 / 审阅 <任务> / 查询 <问题>"
user-invocable: true
---

工程根目录为 `${CLAUDE_SKILL_DIR}/../../..`，当前会话 ID 为 `${CLAUDE_SESSION_ID}`。

先读取工程根目录下的 `skills/gauss-knowledge/SKILL.md`，将工程根目录解析为绝对路径，按该协议在**当前会话**执行。用户请求为：$ARGUMENTS

自然语言参数只是请求内容，不当作 shell 命令插值。记住初始化返回的 paths/session/home。不要调用 `kb run`、`whole run`、`claude -p` 或其他模型进程。无需先配置 MCP。
