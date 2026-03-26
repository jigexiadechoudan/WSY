# Tasks
- [x] Task 1: 修复并完善用户数据模型设计 (E-001)
  - [x] SubTask 1.1: 在 `backend/app/db/mysql_db.py` 中补充缺失的 `User`, `PracticeRecord`, `UserWork`, `UserAbility`, `UserLevel` 模型定义。
  - [x] SubTask 1.2: 修复 `backend/app/db/migrate_user_system.py` 脚本，确保可以正确运行并创建数据库表。
- [x] Task 2: 完善学习进度追踪与雷达图接口 (E-002 & E-003)
  - [x] SubTask 2.1: 修复并优化 `backend/app/api/endpoints/user_profile.py` 中记录练习数据及更新能力的逻辑，确保每次练习后自动更新时长和准确率。
  - [x] SubTask 2.2: 确保 `GET /api/v1/user/profile` 正常返回五维数据（稳定性/准确度/速度/创意/知识，0-100分）。
- [x] Task 3: 实现电子证书生成功能 (E-004)
  - [x] SubTask 3.1: 在 `backend/requirements.txt` 中添加证书生成所需依赖（如 `Pillow`, `qrcode`, `reportlab` 或其他适合的 PDF 库）。
  - [x] SubTask 3.2: 创建 `backend/app/services/certificate_service.py`，实现生成带二维码、符合东方美学的电子证书 (PNG/PDF)。
  - [x] SubTask 3.3: 创建 `backend/app/api/endpoints/certificate.py` 提供证书生成和下载接口，并在 `backend/main.py` 或 API 路由中注册。

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
