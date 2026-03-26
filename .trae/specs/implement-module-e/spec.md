# 用户档案系统与证书生成 Spec

## Why
目前项目中模块 E (用户档案系统) 的实现处于不完整状态，数据模型（User等）在 `mysql_db.py` 中缺失，导致后端相关接口无法运行。为了提供完整的用户学习追踪、能力雷达图和电子证书生成功能，我们需要修复现有缺失的逻辑，并完整开发模块 E 的业务需求。

## What Changes
- 重新在 `mysql_db.py` 中定义缺失的用户系统数据模型：`User`, `PracticeRecord`, `UserWork`, `UserAbility`, `UserLevel` 等。
- 修复 `migrate_user_system.py` 并保证可以正确创建表与初始化数据。
- 完善并修复 `app/api/endpoints/user_profile.py` 中的进度追踪与雷达图接口。
- 新增电子证书生成服务，支持生成包含用户信息、等级、日期、二维码的证书（支持 PNG/PDF 格式）。
- **BREAKING**: 原有 `user_profile.py` 和数据模型中不完整的逻辑将被重写和清理。

## Impact
- Affected specs: 模块 E（E-001, E-002, E-003, E-004）
- Affected code:
  - `backend/app/db/mysql_db.py`
  - `backend/app/api/endpoints/user_profile.py`
  - `backend/app/db/migrate_user_system.py`
  - `backend/app/services/certificate_service.py` (新增)
  - `backend/app/api/endpoints/certificate.py` (新增)
  - `backend/requirements.txt` (新增 Pillow, qrcode, pdfkit 等依赖)

## ADDED Requirements
### Requirement: 用户数据模型 (E-001)
系统应提供完整的用户、学习记录、作品集表结构。
#### Scenario: 数据库初始化
- **WHEN** 运行迁移脚本
- **THEN** 成功在 MySQL 数据库中创建相应的用户表及关联表，并写入默认测试数据。

### Requirement: 学习进度追踪 (E-002)
系统应能记录每次练习的数据，并统计总时长、平均准确率等。
#### Scenario: 完成练习记录
- **WHEN** 客户端调用添加练习记录接口
- **THEN** 系统更新用户的统计数据及五维能力雷达图。

### Requirement: 电子证书生成 (E-004)
完成学习后，系统应能生成包含二维码验证的电子证书。
#### Scenario: 请求证书
- **WHEN** 客户端调用生成证书接口
- **THEN** 系统生成一张美观的东方美学风格电子证书，支持返回 PNG 或 PDF 格式供下载。

## MODIFIED Requirements
### Requirement: 雷达图数据接口 (E-003)
修复现有的 `/api/v1/user/profile`，确保能够返回完整的用户基本信息与动态计算的能力五维数据。
