# Tasks

- [x] Task 1: 创建前端全局协调器组件 (OmniOrchestrator)
  - [x] SubTask 1.1: 创建 `OmniOrchestrator.jsx` 组件，包含悬浮唤起按钮和对话输入面板。
  - [x] SubTask 1.2: 设计美观的输入框 UI，支持回车发送指令，支持加载中状态。
  - [x] SubTask 1.3: 将该组件集成到应用的全局布局 (例如 `Navbar` 旁或全局悬浮位置)。

- [x] Task 2: 创建任务管线可视化组件 (TaskPipelineVisualizer)
  - [x] SubTask 2.1: 创建 `TaskPipelineVisualizer.jsx` 组件，用于接收并解析协调器的返回数据。
  - [x] SubTask 2.2: 实现“意图识别”的 UI 展示 (显示识别到的意图类型和置信度)。
  - [x] SubTask 2.3: 实现“任务分解与执行”的 UI 展示 (使用步骤条或卡片列表展示分解出的 tasks)。
  - [x] SubTask 2.4: 实现“最终结果”的 UI 展示 (包含自然语言回复和结果载荷如图片、链接等)。

- [x] Task 3: 前后端接口联调与数据绑定
  - [x] SubTask 3.1: 在 `OmniOrchestrator` 中编写发送请求的逻辑，调用 `http://localhost:8002/api/v1/orchestrator/process` 接口。
  - [x] SubTask 3.2: 处理接口返回的 JSON 结构 (`intent`, `tasks`, `results`, `final_answer`)。
  - [x] SubTask 3.3: 处理错误状态和超时情况，给予用户友好提示。

# Task Dependencies
- Task 2 依赖于 Task 1 的基础框架。
- Task 3 依赖于 Task 1 和 Task 2 的 UI 完成。
