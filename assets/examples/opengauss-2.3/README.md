# openGauss 2.3实际输出样本

这些文件由工程全仓入口、模块材料包、真实Claude Code研究、源码编辑/审阅和知识查询生成，不是GaussDB初始化数据。

- [全仓计划](PLAN.md)：15,629资产、535模块、初始557任务；当前还包含3项经审机制任务。
- [完整任务及依赖](PLAN.json)／[逐资产覆盖](COVERAGE.csv)／[任务工作包](WORK-PACKAGES.csv)。
- [实际Wiki](wiki/index.html)：10个当前SQL Patch单元；另保留61个历史GEQO单元用于展示版本漂移，它们已标stale，不计当前覆盖。
- [当前SQL Patch结构化知识](accepted-sqlpatch-knowledge.json)。
- [开发上下文](coding-context.json)／[测试上下文](test_generation-context.json)／[review上下文](review-context.json)。
- [三角色实际回读](use-check.json)／[模块未决覆盖](sqlpatch-coverage.json)。

真实客户端为Claude Code 2.1.310，路由模型DeepSeek v4.1 Flash。先生成盘点，再依据审阅生成3项深度任务，本轮实际完成其中的序号与计划缓存机制。模型原文的回滚、快照与并发推测经Codex AI源码编辑限定，editorial_provenance保留来源；不是独立人工专家审核。本文不宣称整个SQL Patch模块或整个openGauss已学完。

全仓和本模块验收均为incomplete：两个深度主题、构建文件、部分源码区间、双端契约和未决问题继续阻断。实际三类检索检查通过只证明必要知识ID进入上下文，不能证明SQL运行或盲测准确率。

不附5GB调用图、源码仓库、SQLite工作库、工作单密钥、会话日志或模型认证。源码节选来自公开openGauss，见OPENGAUSS-LICENSE.txt；本样本不应用到GaussDB的已学比例。
