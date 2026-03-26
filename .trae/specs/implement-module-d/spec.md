# 模块 D: 主协调器 (Master Orchestrator) Spec

## Why
目前系统缺乏一个统一的入口来协调各个 Agent（如知识、视觉、创作等），导致复杂任务无法跨 Agent 协作，也无法根据用户意图自动路由。通过引入主协调器，我们能够实现用户意图的精准识别和复杂任务的多 Agent 编排。

## What Changes
- 引入基于 MCP (Model Context Protocol) 概念的服务间通信框架，规范 Agent 间的消息格式，实现服务注册与路由。
- 增加意图识别模块，能够将用户的自然语言输入解析为具体的学习、问答或创作意图，支持模糊指令。
- 增加多 Agent 任务编排引擎，支持任务分解、串行执行和并行执行，并汇总执行结果。
- 在 `backend/app/services` 下增加相关模块，并在 `backend/app/api/endpoints/` 暴露主入口点。

## Impact
- Affected specs: 多 Agent 协同能力，系统入口统一。
- Affected code: 
  - `backend/app/core/` (新增 MCP 通信格式定义)
  - `backend/app/services/` (新增 MCP 通信、意图识别、任务编排服务)
  - `backend/app/api/endpoints/` (新增 orchestrator 入口)
  - `backend/app/main.py` (集成主协调器路由)

## ADDED Requirements
### Requirement: MCP 协议通信框架
系统应提供标准的 Agent 间通信机制。
#### Scenario: 消息路由
- **WHEN** 协调器向特定 Agent 发送任务
- **THEN** 消息按照规范格式传递，Agent 处理后返回标准化结果，且过程被完整记录日志。

### Requirement: 意图识别
系统应能识别用户指令类型。
#### Scenario: 模糊指令识别
- **WHEN** 用户输入“我想了解这个并画一张图”
- **THEN** 系统能识别出包含“学习”和“创作”双重意图，并交由编排器处理。

### Requirement: 多 Agent 任务编排
系统应能分解复杂任务并调度。
#### Scenario: 复杂任务执行
- **WHEN** 协调器接收到多意图任务
- **THEN** 协调器将任务分解，先调用知识问答 Agent 获取信息，再将结果传递给创作 Agent 生成内容，最后汇总返回给用户。
