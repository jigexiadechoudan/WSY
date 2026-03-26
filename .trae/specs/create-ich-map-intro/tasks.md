# Tasks
- [x] Task 1: 搭建入场页基础骨架与路由
  - [x] SubTask 1.1: 在前端项目中创建 `Intro` 页面组件。
  - [x] SubTask 1.2: 配置前端路由，将根路径 `/` 指向该 `Intro` 页面。
  - [x] SubTask 1.3: 引入基础可视化库与动画引擎（如 ECharts, Three.js 或 GSAP，根据当前项目前端技术栈决定）。
- [x] Task 2: 实现中国地图可视化与镜头漫游
  - [x] SubTask 2.1: 集成地图渲染引擎并加载中国地图 GeoJSON 数据或 3D 地形。
  - [x] SubTask 2.2: 设计并实现地图视角的平移、缩放（Fly-to 效果）动画控制逻辑。
  - [x] SubTask 2.3: 定义漫游路径数据源（包含具体经纬度、非遗名称、简介等节点数据）。
- [x] Task 3: 开发非遗信息展示组件与视觉美化
  - [x] SubTask 3.1: 开发极具人文气息（如水墨风、古典排版）的非遗信息卡片组件。
  - [x] SubTask 3.2: 监听地图镜头聚焦事件，在到达目标地点时触发卡片的显隐交互动画。
  - [x] SubTask 3.3: 增加整体画面的滤镜、材质纹理（如纸张纹理遮罩）等视觉打磨。
- [x] Task 4: 转场与系统主界面接入
  - [x] SubTask 4.1: 实现从入场页到系统主界面的平滑过渡动画（如淡出、水墨晕染转场）。
  - [x] SubTask 4.2: 增加“跳过”或“进入探索”按钮及相应的页面跳转逻辑。

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
