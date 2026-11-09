# openGauss 2.4 实际输出

这是可行性验证的实际产物。源码版本为本地实验提交 `ed99bbde5308942d4eb062e7a851bdb85dda902f`；公司 GaussDB、完整手册、完整历史特性和数据库运行未在此验收。手册仅一页连接参数样例，特性清单仅4行验证样例，其中含一个明确负例。

- [初始全仓课程 JSON](initial-curriculum.json)：537模块、3,667个功能包候选、2,380个CPP全部有归属。原生初始559项任务，不按函数/TU/调用边/阅读区间各建任务。
- [实际规划指标](planning-validation.json)：首次107.523秒，学习库约81.32MiB，未解析TU、未产生编译图。
- [当前课程 HTML](plan-current/curriculum/index.html) · [Markdown](plan-current/curriculum/PLAN.md) · [JSON](plan-current/curriculum/PLAN.json)：GEQO经源码盘点调整为3个机制包，全仓当前候选数3,668。
- [当前覆盖 HTML](plan-current/whole/index.html) · [逐资产CSV](plan-current/whole/COVERAGE.csv)：真实保留待学、未决、待审，不把已读当学懂。
- [已审 Wiki](wiki/index.html) · [结构化知识](wiki/knowledge.json)：12项已发布知识及源码引用。
- 四角色实际查询：[开发](contexts/coding.json)、[测试](contexts/test_generation.json)、[Review](contexts/review.json)、[运维](contexts/operations.json)。
- [真实学习验证摘要](learning-validation.json) · [全新目录离线验证](offline-smoke.json)。

用户要求判断工程是否可行后，本轮停止继续学习。GEQO尚未全学完：15个CPP对应19个区间，其中4个已有带缺口解释，15个仍open。已发布7个实现结论、2个机制、3个未运行测试义务，涉及入口选择、GUC约束、PlannerInfo临时状态与恢复、计划缓存影响、主循环和代价评估。

开发/测试/review查询具有所需结构字段，有限响应仍可能标partial；运维明确缺配置结构字段。知识不足不会补造事实。审阅由真实不同AI上下文完成，不是人工专家或数据库测试。首轮开发发现的性能、任务膨胀及类型问题已修复，旧实验任务保留来路；新课程不逐open问题建任务。

SQLite是工程权威状态，此处只发布可浏览投影与验证摘要，不发布学习库、私有会话句柄、调用图、客户端日志、模型认证或完整产品源码。冻结引用可能含本地实验路径，它们是来源记录，不是迁移配置。
