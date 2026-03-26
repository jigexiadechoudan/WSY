# Integrate Orchestrator to Frontend Spec

## Why
目前后端的主协调器 (Master Orchestrator) 和意图识别功能已经开发完成，能够处理自然语言输入、识别意图并拆解为子任务。但是前端界面仍然采用手动点击的路由导航方式，缺乏一个统一的自然语言入口。需要将主协调器嵌入前端，为用户提供一个全局的“智能助手”入口，提升多智能体协同（Multi-Agent Collaborative System）的直观体验。

## What Changes
- 添加全局的智能对话输入框 (Omni-input / Global Orchestrator)，允许用户输入任意复杂的自然语言指令。
- 添加任务执行可视化面板 (Task Pipeline Visualizer)，用于展示：
  1. 意图识别结果 (如：学习、创作)
  2. 任务分解过程 (子任务列表)
  3. 各个 Agent 的执行状态 (并行/串行执行中)
- 接入后端 API `/api/v1/orchestrator/process`，实现前后端数据打通。
- 在首页或其他合适位置提供入口按钮唤起该智能组件。

## Impact
- Affected specs: 模块 D (主协调器) 前端集成
- Affected code:
  - `frontend/src/components/OmniOrchestrator.jsx` (新文件)
  - `frontend/src/components/TaskPipelineVisualizer.jsx` (新文件)
  - `frontend/src/pages/Home.jsx` 或全局 Layout 组件
  - `frontend/src/components/Navbar.jsx` (可能需要在此处添加入口)

## ADDED Requirements
### Requirement: 统一智能入口
系统应提供一个全局可见或易于唤起的输入框，接收用户的自然语言指令。

#### Scenario: 发起复杂指令
- **WHEN** 用户在输入框中输入 "我想学苏绣起针，并生成一张相关海报"，并点击发送
- **THEN** 前端调用后端 orchestrator 接口，并在界面上实时/逐步展示：意图识别为 `learning` 和 `creation`，任务被分解为调用 `rag_query` 和 `generate_image`。

### Requirement: 任务可视化
系统应能直观地展示复杂任务在多 Agent 系统中的流转状态。

#### Scenario: 查看执行结果
- **WHEN** 后端完成所有子任务
- **THEN** 前端面板显示最终汇总的文本结果，以及生成的图片、查询到的知识卡片等可视化结果内容。
