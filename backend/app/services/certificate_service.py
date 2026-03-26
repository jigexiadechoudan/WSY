import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
from app.core.config import settings

class CertificateService:
    def __init__(self):
        # We will use a standard Windows font for Chinese characters
        self.font_path = "C:\\Windows\\Fonts\\simkai.ttf"
        if not os.path.exists(self.font_path):
            self.font_path = "C:\\Windows\\Fonts\\simhei.ttf"
        if not os.path.exists(self.font_path):
            self.font_path = "arial.ttf"  # Fallback

        # Generate a simple base template if no image is provided
        self.bg_color = (250, 243, 232)  # 暖白色，宣纸质感
        self.text_color = (51, 51, 51)   # 深灰/水墨黑
        self.accent_color = (184, 59, 59) # 朱砂红 (用于印章等)
        self.border_color = (200, 160, 100) # 雅金色边框

    def generate_certificate(self, user_name: str, level: str, title: str, date: datetime, verification_url: str, format_type: str = "png") -> bytes:
        """
        生成电子证书并返回字节流
        """
        # 1. 创建基础图像 (A4 尺寸横向 297x210 mm，按 96dpi 约 1123x794 像素)
        width, height = 1123, 794
        img = Image.new('RGB', (width, height), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        # 2. 绘制边框 (东方美学风格：双线边框)
        margin = 40
        draw.rectangle([margin, margin, width - margin, height - margin], outline=self.border_color, width=4)
        inner_margin = 55
        draw.rectangle([inner_margin, inner_margin, width - inner_margin, height - inner_margin], outline=self.border_color, width=1)

        # 加载字体
        try:
            title_font = ImageFont.truetype(self.font_path, 60)
            subtitle_font = ImageFont.truetype(self.font_path, 36)
            text_font = ImageFont.truetype(self.font_path, 28)
            small_font = ImageFont.truetype(self.font_path, 20)
        except Exception:
            title_font = subtitle_font = text_font = small_font = ImageFont.load_default()

        # 3. 绘制标题
        cert_title = "非物质文化遗产学习证书"
        # 居中计算
        title_bbox = draw.textbbox((0, 0), cert_title, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_w) / 2, 120), cert_title, font=title_font, fill=self.text_color)

        # 4. 绘制正文
        content_y = 280
        line1 = f"授予: {user_name}"
        draw.text((180, content_y), line1, font=subtitle_font, fill=self.text_color)

        content_y += 80
        line2 = f"在非遗技艺学习中表现优异，已达到【{title}】水平。"
        draw.text((180, content_y), line2, font=text_font, fill=self.text_color)

        content_y += 60
        line3 = f"特发此证，以资鼓励，望继续传承发扬中华优秀传统文化。"
        draw.text((180, content_y), line3, font=text_font, fill=self.text_color)

        # 5. 绘制落款和日期
        date_str = date.strftime("%Y年%m月%d日")
        draw.text((700, 550), "数字非遗传承中心", font=text_font, fill=self.text_color)
        draw.text((720, 600), date_str, font=text_font, fill=self.text_color)

        # 绘制印章 (模拟)
        stamp_text = "非遗\n传承"
        stamp_x, stamp_y = 880, 530
        draw.rectangle([stamp_x, stamp_y, stamp_x+80, stamp_y+80], outline=self.accent_color, width=3)
        draw.text((stamp_x+15, stamp_y+10), stamp_text, font=subtitle_font, fill=self.accent_color)

        # 6. 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=1,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # 将二维码粘贴到证书上
        qr_pos = (180, 520)
        img.paste(qr_img, qr_pos)
        draw.text((180, 650), "扫码验证证书", font=small_font, fill=self.text_color)

        # 7. 导出字节流
        img_byte_arr = io.BytesIO()
        if format_type.lower() == 'pdf':
            img.save(img_byte_arr, format='PDF', resolution=96.0)
        else:
            img.save(img_byte_arr, format='PNG')
            
        return img_byte_arr.getvalue()

certificate_service = CertificateService()
