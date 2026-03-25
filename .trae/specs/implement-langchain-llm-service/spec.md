# 知识馆长 LLM 服务封装 (LangChain) Spec

## Why
在任务 `TASKS.md` 中，B-004 要求使用 LangChain 封装大语言模型（LLM）服务以支撑知识馆长 Agent 的工作。为了提供更智能、连贯的问答体验，需要将当前的简单调用升级为基于 LangChain 体系的完整实现，包括流式响应、对话历史记忆和 Prompt 模板系统，以应对非遗知识的检索和回答。

## What Changes
- 完善 `backend/app/services/llm_service.py` 的架构，使其深度集成 LangChain 核心组件。
- 配置并使用 DeepSeek 模型的 API 密钥（利用 `ChatOpenAI` 兼容层）。
- 使用 LangChain 的 `ChatPromptTemplate` 替代原有的字符串拼接实现 Prompt 模板系统。
- 引入 LangChain 的 Memory 机制（如 `ConversationBufferMemory` 或 `RunnableWithMessageHistory`）来维护用户会话级别的历史记忆。
- 添加支持流式响应（Streaming）的方法，以便在生成长文本时能够实时返回给前端（可结合 FastAPI `StreamingResponse`）。
- **注意**：由于前置任务（向量数据库部署）尚未完成，在本次实现中保留支持 RAG（检索增强）的占位逻辑，使其能独立于数据库直接进行问答测试。

## Impact
- Affected specs: 知识馆长 Agent 的知识问答核心功能。
- Affected code: 
  - `backend/app/services/llm_service.py`
  - `backend/app/api/endpoints/knowledge_curator.py`（若需测试流式响应接口）

## ADDED Requirements
### Requirement: Prompt 模板系统
The system SHALL provide 结构化的 Prompt 模板，明确区分 System Prompt 和 Human Prompt。

#### Scenario: 动态上下文注入
- **WHEN** 收到带有检索片段的用户提问
- **THEN** 系统能使用 `ChatPromptTemplate` 自动将上下文注入到提示词中。

### Requirement: 对话历史记忆
The system SHALL provide 对话记忆功能。

#### Scenario: 连续追问
- **WHEN** 用户针对上一个回答进行代词指代提问（如“它的历史是什么？”）
- **THEN** 模型能结合记忆上下文正确回答。

### Requirement: 流式响应支持
The system SHALL provide 流式输出支持。

#### Scenario: 流式输出体验
- **WHEN** 前端请求流式接口
- **THEN** 服务能以 SSE (Server-Sent Events) 的形式实时输出生成的 token。
