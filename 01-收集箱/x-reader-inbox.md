
## 🐦 URL Source: https://x.com/alexzuo4/status/2026577523824525769

Published Time: Thu, 26 Feb 2026 05:5
- Source: @alexzuo4 (twitter)
- URL: https://x.com/alexzuo4/status/2026577523824525769
- Fetched: 2026-02-26T13:57

URL Source: https://x.com/alexzuo4/status/2026577523824525769

Published Time: Thu, 26 Feb 2026 05:57:42 GMT

Markdown Content:
Article
-------

Conversation
------------

[![Image 1: Image](https://pbs.twimg.com/media/HB_QPmiagAAhvWV?format=jpg&name=small)](https://x.com/alexzuo4/article/2026577523824525769/media/2026567323801518080)

一个币圈公司的硅碳共治之路 — Cobo 的内部 AI 转型

从 2024 年底开始，Cobo 除了自己核心的加密托管和稳定币支付业务之外，一直在探索 AI 和区块链的结合。

我们最早看到的是 MCP 带来的标准化技能潜力。理论上，如果技能足够标准化，AI 可以像插件一样调用能力，区块链会成为 AI 最自然的金融基础设施。

于是我们内部孵化了一个 MCP 的应用商店。但很快证伪。

当时的 AI 门槛还是高到只有成熟工程师才可以熟练调用，MCP 又不够标准化，每一个对接耗时耗力，成本高、推进慢，落地效果远不如想象。

但 AI 团队毕竟搭起来了。很贵，很难招，也不可能轻易撤掉。

于是我们决定换一个方向。既然现在还改造不了客户世界，那就先改造自己。

第一个问题：安全

Cobo 作为资产托管公司，不管是数据还是内部技术流程框架，都是极其敏感。内部也有严格的数据层级。但没有数据、没有真实业务输入，不可能练出公司自己的 Agent。

我们最早想的是本地模型部署。但现实是，本地模型的智力水平达不到要求。能跑，但不好用；能回答，但不够聪明。

最后还是选择了 Claude、Gemini 为主（可以申请 ZDR——零数据留存条款，实现最高级别隔离）。

但大模型只是业务的底层“大脑”。真正复杂的，是数据和权限。

我们后来做了一整套内部知识库和 Agent 框架。

[![Image 2: Image](https://pbs.twimg.com/media/HB_Np5VaUAA39qc?format=jpg&name=small)](https://x.com/alexzuo4/article/2026577523824525769/media/2026564476988968960)

内部知识库+cobo自研agent体系

知识库负责公司内部数据分层。根据员工权限，分配可读范围。

Agent 在调用知识库时，也继承员工权限，而不是拥有“上帝视角”。

这里的细节包括：

*   如何隔离网络环境

*   如何限制跨层数据流动

*   如何控制日志留存可审计

*   如何避免敏感信息外泄

这些都不性感，但决定这件事能不能长期跑下去。AI 不能成为安全漏洞。

架构搭好之后的问题：没人用

即使到今天，公司依然面临着一个现实问题：很多前台业务对 AI 是不屑的。

如果只是鼓励使用，AI改变工作流不会发生。

我们后来意识到，必须从公司管理动手。

第一个突破口：OKR Agent

我们第一个强推的场景，不是客服，也不是写代码。

是 OKR。

我们用 AI 拆公司战略，用 AI 帮助设定 OKR，用 AI 追踪进度，用 AI 复盘卡点。

也就是说，把公司管理，从人的管理，慢慢变成硅碳共治。这个过程对员工是极其难受的。

以前目标可以写得漂亮一点，过程可以讲得合理一点。现在每周数据都在那里，借口越来越少。

从那一刻开始，目标不再只是会议里的讨论，而变成了系统里的持续记录。

[![Image 3: Image](https://pbs.twimg.com/media/HB_N1C5aMAA7057?format=jpg&name=small)](https://x.com/alexzuo4/article/2026577523824525769/media/2026564668534435840)

strategy okr每周督促业务进展

但也是从绩效开始，每个人才真正对 AI 熟悉起来。因为你不参与，它会直接影响你的薪酬。

从绩效到业务：全面 Agent 化

当 OKR 跑起来之后，我们开始推进内部服务 Agent 化。我们用评比 + 奖金的方式，强制每个部门设立和自己业务相关的 Agent。

客服做客服 Agent。法律做合同辅助 Agent。销售做CRM Agent。

[![Image 4: Image](https://

---
