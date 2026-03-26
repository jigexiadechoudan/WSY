from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.mysql_db import get_db, User
from app.services.certificate_service import certificate_service
from app.core.config import settings

router = APIRouter()

@router.get("/generate/{user_id}")
async def generate_certificate(
    user_id: int,
    format: str = Query("png", description="证书格式，支持 png 或 pdf"),
    db: Session = Depends(get_db)
):
    """
    生成用户的电子证书
    检验标准:
    - [x] 证书包含用户信息、等级、日期
    - [x] 支持二维码验证
    - [x] 可下载 PNG/PDF 格式
    - [x] 模板美观符合东方美学
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 如果经验值太低可能还未获得证书（可选逻辑）
    if user.experience_points < 200:
        pass # 目前不限制，仅供测试

    # 生成二维码验证URL (这里使用本地前端或后端的虚拟URL进行演示)
    verification_url = f"http://localhost:5173/verify-certificate/{user.id}"

    # 生成证书
    try:
        cert_bytes = certificate_service.generate_certificate(
            user_name=user.name,
            level=user.level.value,
            title=user.title,
            date=datetime.now(),
            verification_url=verification_url,
            format_type=format
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"证书生成失败: {str(e)}")

    # 返回相应的格式
    if format.lower() == "pdf":
        return Response(content=cert_bytes, media_type="application/pdf", headers={
            "Content-Disposition": f'attachment; filename="certificate_{user.id}.pdf"'
        })
    else:
        return Response(content=cert_bytes, media_type="image/png", headers={
            "Content-Disposition": f'attachment; filename="certificate_{user.id}.png"'
        })
