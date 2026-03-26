# 数字传承人 (The Digital Inheritor) —— 非遗工艺流程 Agent 交互教学与复原助手

> 本项目为 **中国大学生计算机设计大赛**（软件应用与开发 / 移动应用开发）参赛作品。

“数字传承人”是一款基于多智能体协作 (Multi-Agent) 和多模态交互技术的数字化非物质文化遗产 (非遗) 导师。它致力于打破传统非遗保护中“重记录、轻交互”的痛点，通过 AI 技术实现“能看、能听、会画”的沉浸式非遗技艺教学与体验，让每个人都能成为数字时代的非遗传承人。

## ✨ 项目亮点 (Highlights)

1. **🤖 首创“多智能体协作”非遗教学架构 (Multi-Agent System)**
   - 突破单一 AI 的局限，构建了由 **视觉导师 (Vision-Mentor)**、**知识馆长 (Knowledge-Curator)** 和 **创意艺匠 (Creative-Artisan)** 组成的专业智能体矩阵。
   - 三大 Agent 各司其职，完美模拟真实的“师徒教学”场景，提供动作纠偏、知识问答、创意生成的一站式服务。

2. **⚡ 高效的端侧视觉推理优化 (Edge AI Computing)**
   - 采用 MediaPipe 和 TensorFlow.js 在浏览器端进行实时的手部/骨骼关键点追踪。
   - 实现了 **<100ms 的极低延迟反馈**，无需将视频流上传服务器，既保证了流畅的交互体验，又严格保护了用户隐私，显著降低了服务端算力成本。

3. **🧠 垂直领域的非遗知识图谱与 RAG 系统 (Domain-Specific Knowledge Graph)**
   - 针对通用大模型在专业非遗领域“不懂行、易幻觉”的问题，基于 Neo4j 构建了包含苏绣、紫砂、剪纸、皮影等项目的专属知识图谱。
   - 结合检索增强生成 (RAG) 技术，提供精准、深度的非遗历史、工艺、材料等多模态问答。

4. **🎨 轻量且稳定的 AIGC 创意引擎 (AIGC Integration)**
   - 秉持轻量化、稳定的原则，接入云端高性能生图 API (如 SiliconFlow/Stable Diffusion)，避免了繁重的本地部署。
   - 支持将用户的简单草图快速转化为大师级的非遗风格（如青花瓷、蜡染、刺绣）效果图，极大降低了非遗文创设计的门槛。

5. **📱 极致的东方美学与多模态交互体验 (Oriental Aesthetics & Multimodal UI)**
   - 前端采用 React 19 + Tailwind CSS，深度融合中国传统色配色与东方美学 UI 设计。
   - 支持手势交互、语音/图文问答、视觉展示等多模态体验，适用于高校教学、文创设计、博物馆展览等多种场景。

## 🏗️ 系统架构 (Architecture)

```text
┌─────────────────────────────────────────────────────────┐
│                    主协调器 (Main Orchestrator)          │
│          (基于大模型的意图识别与 Agent 任务路由)            │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Vision        │  │ Knowledge     │  │ Creative      │
│ Mentor Agent  │  │ Curator Agent │  │ Artisan Agent │
│ 视觉导师      │  │ 知识馆长      │  │ 创意艺匠      │
│ (手眼身法)    │  │ (博古通今)    │  │ (妙笔生花)    │
│ - MediaPipe   │  │ - RAG 系统    │  │ - SD/云端生图 │
│ - 姿态追踪    │  │ - Neo4j 图谱  │  │ - ControlNet  │
│ - 实时纠偏    │  │ - 多模态问答  │  │ - 风格迁移    │
└───────────────┘  └───────────────┘  └───────────────┘
```

## 🛠️ 技术栈 (Tech Stack)

*   **前端 (Frontend)**: React 19, TypeScript, Vite, Tailwind CSS, MediaPipe (计算机视觉), Three.js
*   **后端 (Backend)**: Python, FastAPI, LangChain
*   **人工智能 (AI/ML)**: Qwen / GLM-4 (基座大模型), 知识图谱 (Knowledge Graph), 检索增强生成 (RAG)
*   **数据库 (Database)**: Neo4j (图数据库), 向量数据库 (Milvus 等)

## 🚀 快速开始 (Getting Started)

### 前端启动
```bash
cd frontend
npm install
npm run dev
```
前端服务将运行在 `http://localhost:5173`

### 后端启动
```bash
cd backend
pip install -r requirements.txt
# 请确保已在 .env 文件中配置了 NEO4J 和 API_KEY 等相关环境变量
python run.py
```
后端 API 服务将运行在 `http://localhost:8000`

## 📂 项目结构 (Project Structure)

*   `/frontend` - React 前端代码，包含页面组件、手势识别模块和状态管理。
*   `/backend` - FastAPI 后端代码，包含核心 Agent 逻辑、RAG 系统、图谱查询和 API 接口。
*   `/assets` - 项目所需的非遗主题图片和静态资源。
*   `/spec` - 项目的需求规格和任务规划文档。

## 📜 许可证 (License)

本项目仅供中国大学生计算机设计大赛评审与展示使用。
