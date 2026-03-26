# Tasks

- [x] Task 1: 搭建 MCP 协议通信框架
  - [x] SubTask 1.1: 在 `backend/app/core/` 定义 MCP 消息格式规范 (Request/Response 模型)
  - [x] SubTask 1.2: 在 `backend/app/services/` 实现简单的服务注册与发现机制
  - [x] SubTask 1.3: 实现消息路由逻辑，并添加完整的日志记录

- [x] Task 2: 实现意图识别模块
  - [x] SubTask 2.1: 在 `backend/app/services/` 增加意图识别逻辑（`intent_service.py`）
  - [x] SubTask 2.2: 对接 LLM 服务实现对“学习/问答/创作”意图的识别，支持模糊指令
  - [x] SubTask 2.3: 编写意图识别失败时的友好回退提示逻辑

- [x] Task 3: 实现多 Agent 任务编排引擎
  - [x] SubTask 3.1: 在 `backend/app/services/` 增加任务编排服务（`orchestrator_service.py`）
  - [x] SubTask 3.2: 实现任务分解与执行流控制（支持串行与并行）
  - [x] SubTask 3.3: 汇总各 Agent 结果并格式化返回

- [x] Task 4: API 接口与集成测试
  - [x] SubTask 4.1: 在 `backend/app/api/endpoints/` 新增 `orchestrator.py` 路由并暴露 API
  - [x] SubTask 4.2: 在 `backend/app/main.py` 注册该路由
  - [x] SubTask 4.3: 编写并运行测试脚本，验证整个主协调器的流程（意图识别 -> 任务分发 -> 结果汇总）
