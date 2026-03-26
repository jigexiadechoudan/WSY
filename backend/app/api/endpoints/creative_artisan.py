import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import langchain_service
from app.services.image_service import cloud_image_service

router = APIRouter()

class PromptEnrichRequest(BaseModel):
    idea: str
    style: str

class GenerateImageRequest(BaseModel):
    optimized_prompt: str

class GenerateStoryRequest(BaseModel):
    idea: str
    style: str
    image_url: str

@router.post("/enrich-prompt")
async def enrich_prompt(request: PromptEnrichRequest):
    """
    LLM plays a virtual master to enrich the user's idea and generate an English prompt for drawing.
    """
    system_prompt = f"""你现在是一位资深的{request.style}大师，也是一位现代数字文创策划师。
用户有一个简单的文创想法，你需要：
1. 用符合你大师身份的口吻回复用户，给予鼓励，并讲解如何用{request.style}技法表现这个想法（50-100字）。
2. 将这个想法翻译并扩写为一个用于 AI 绘画（Stable Diffusion/Midjourney）的高质量英文提示词（Prompt）。包含{request.style}特有的材质、工艺细节、光影和质感描述。

请严格以 JSON 格式返回，不要有任何 Markdown 代码块包裹，字段如下：
{{
  "master_reply": "大师的回复...",
  "optimized_prompt": "English prompt for image generation..."
}}"""
    
    messages = [{"role": "user", "content": f"我的想法是：{request.idea}"}]
    response = langchain_service.chat(messages, system_prompt)
    
    try:
        # Clean up response if it's wrapped in markdown json block
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3].strip()
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:-3].strip()
            
        data = json.loads(cleaned_response)
        return {"status": "success", "data": data}
    except Exception as e:
        print(f"Failed to parse LLM response: {response}")
        raise HTTPException(status_code=500, detail="Failed to parse master's reply.")

@router.post("/generate-image")
async def generate_image(request: GenerateImageRequest):
    """
    Call Cloud Image Generation API with the optimized prompt.
    """
    try:
        image_url = await cloud_image_service.generate_image(request.optimized_prompt)
        return {
            "status": "success", 
            "image_url": image_url,
            "prompt_used": request.optimized_prompt
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@router.post("/generate-story")
async def generate_story(request: GenerateStoryRequest):
    """
    Generate poem, title and description for the digital artifact.
    """
    system_prompt = f"""你是一位深谙中国传统文化与非遗技艺的文人雅士，同时精通现代数字艺术鉴定。
用户创作了一幅以“{request.idea}”为灵感的{request.style}风格数字艺术品。

请为其创作一段文化赋能的内容，包含：
1. title: 给这幅作品起一个典雅的名称（如：“赛博机甲猫·青花瓷版”或四字雅称）。
2. poem: 一首符合意境的中国风古典诗词（绝句，四句）。
3. description: 一段“文物鉴定/文化解说”文字（100字左右），将{request.idea}与{request.style}的工艺特点完美结合，升华其文化内涵。

请严格以 JSON 格式返回，不要有任何 Markdown 代码块包裹，字段如下：
{{
  "title": "作品名称",
  "poem": "古诗内容...",
  "description": "文化解说..."
}}"""
    
    messages = [{"role": "user", "content": "请为我的作品生成赋能文案。"}]
    response = langchain_service.chat(messages, system_prompt)
    
    try:
        # Clean up response if it's wrapped in markdown json block
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3].strip()
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:-3].strip()
            
        data = json.loads(cleaned_response)
        return {"status": "success", "data": data}
    except Exception as e:
        print(f"Failed to parse LLM response for story: {response}")
        raise HTTPException(status_code=500, detail="Failed to generate cultural story.")
