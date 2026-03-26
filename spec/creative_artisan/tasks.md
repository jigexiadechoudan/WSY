# 创意艺匠 (Creative Artisan) 任务拆解

### Task 1: 云端生图 API 调研与接入准备
- [ ] 确定一家提供稳定云端文生图（Text-to-Image）服务的 API 提供商（例如：智谱 CogView, 阿里云通义万相, 硅基流动 SiliconFlow 等，考虑到稳定性与轻量级）。
- [ ] 在 `d:\computer-design\backend\.env` 中配置相应的 `IMAGE_API_KEY`。

### Task 2: 后端提示词优化接口 (Prompt Enrichment)
- [ ] 在 `backend/app/api/endpoints/creative_artisan.py` 中创建 `/enrich-prompt` 接口。
- [ ] 编写 LLM 的 System Prompt，设定“非遗匠人”角色。接收用户的简短创意（Idea）和所选的非遗流派（Style）。
- [ ] 返回 JSON 数据，包含：`master_reply`（匠人对话回复）和 `optimized_prompt`（英文或优化后的中文绘画提示词，带有非遗质感描述）。

### Task 3: 后端云端生图接口 (Cloud Image Generation)
- [ ] 在 `backend/app/api/endpoints/creative_artisan.py` 中创建 `/generate-image` 接口。
- [ ] 接收 `optimized_prompt` 并调用云端 API。
- [ ] 处理 API 返回结果，提取并返回图片的 URL 或 Base64 字符串。

### Task 4: 后端文化赋能接口 (Cultural Story Generation)
- [ ] 在 `backend/app/api/endpoints/creative_artisan.py` 中创建 `/generate-story` 接口。
- [ ] 传入生成的图片 URL（或使用视觉大模型分析），或者传入 `Idea` 与 `Style`，让 LLM 创作：
  - `title`（如：“赛博机甲猫·青花瓷版”）
  - `poem`（四句中国风古诗词）
  - `description`（如“此物将未来科技与千年瓷韵结合，笔触细腻...”）

### Task 5: 前端“创意工坊”界面开发 (Creative Workshop UI)
- [ ] 创建 `frontend/src/pages/CreativeWorkshop.jsx` 页面。
- [ ] 顶部导航栏增加“创意工坊”入口。
- [ ] 开发左侧“创意灵感区”：用户输入想法（Idea），选择非遗流派，与“AI 大师”进行对话（展示 `master_reply`）。
- [ ] 开发右侧“创作画板区”：点击“开始创作”后显示 Loading 动画，依次调用生图和赋能接口。

### Task 6: 前端数字藏品卡片组件 (Digital Artifact Card)
- [ ] 创建 `frontend/src/components/ArtifactCard.jsx`。
- [ ] 将获取的图片、诗词、背景故事精美排版（支持古典风格边框或纸张纹理背景）。
- [ ] 增加“一键下载/分享”功能（可使用 `html2canvas` 库导出）。

### Task 7: 联调与测试
- [ ] 启动前后端服务进行整体链路测试。
- [ ] 调整 LLM Prompt，确保生成的诗词意境优美、绘画提示词能准确反映非遗特征（如“丝线反光”、“裂纹釉面”等）。
