# Tasks
- [x] Task 1: 升级 LLM 基础配置并创建 Prompt 模板系统
  - [x] SubTask 1.1: 在 `llm_service.py` 中使用 `ChatPromptTemplate` 重构原有的硬编码 Prompt，包括 system prompt 和 human prompt。
  - [x] SubTask 1.2: 确保 DeepSeek API 密钥和 BaseURL 从环境变量/Config 正确加载。
- [x] Task 2: 实现对话历史记忆 (Memory)
  - [x] SubTask 2.1: 引入 `BaseChatMessageHistory` 或相关 LangChain 记忆组件。
  - [x] SubTask 2.2: 使用 `RunnableWithMessageHistory` 将模型调用和对话历史结合，以 session_id 隔离不同用户的对话上下文。
- [x] Task 3: 实现流式响应 (Streaming)
  - [x] SubTask 3.1: 在 `llm_service.py` 中添加 `stream_chat` 或类似的方法，利用 `.astream()` 异步流式输出。
  - [x] SubTask 3.2: 确保支持在 FastAPI 中结合 `StreamingResponse` 进行测试调用。
- [x] Task 4: 编写测试脚本验证 B-004 功能
  - [x] SubTask 4.1: 编写测试文件以验证连续对话记忆是否生效（例如通过多轮问答测试上下文）。
  - [x] SubTask 4.2: 编写代码测试流式响应的 token 逐个打印。
- [x] Task 5: 更新项目任务状态
  - [x] SubTask 5.1: 在 `TASKS.md` 中将 `B-004` 的所有检验标准打钩，状态标记为已完成。

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 2 and Task 3
- Task 5 depends on Task 4
