import json
import logging
from typing import Dict, Any, List
from app.services.llm_service import langchain_service

logger = logging.getLogger(__name__)

class IntentService:
    """
    意图识别服务
    负责将用户的自然语言输入解析为结构化的意图信息（learning/QA/creation）
    """
    
    def __init__(self):
        self.llm = langchain_service
        
    async def detect_intent(self, query: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        识别用户意图，支持模糊指令并具备降级逻辑
        
        Args:
            query: 用户输入的文本
            conversation_history: 历史对话记录，格式为 [{"role": "user", "content": "..."}]
            
        Returns:
            结构化的意图识别结果，例如：
            {
                "intent": "QA",  # 可选值：learning, QA, creation, unknown
                "confidence": 0.95,
                "parameters": {
                    "keywords": ["昆曲", "历史"],
                    "action": "查询"
                },
                "reply": "..." # 仅在 unknown 时提供回退提示
            }
        """
        system_prompt = """你是一个智能意图识别助手，专门负责识别用户在非遗文化系统中的意图。
请分析用户的输入，结合上下文，将其分类为以下四种意图之一：
1. learning (学习): 用户希望系统性地学习某种非遗技艺、要求制定学习计划、教程或步骤。
2. QA (问答): 用户询问关于非遗文化的具体事实、历史、人物、剧目等问题。
3. creation (创作): 用户希望创作、生成、设计某些内容（例如：生成一张脸谱图片、写一段唱词、生成海报）。
4. unknown (未知): 无法识别用户的意图，或者输入与非遗文化、学习、问答、创作无关。

请务必以严格的 JSON 格式输出，不要包含任何 markdown 标记或其他文本。
JSON 格式要求如下：
{
    "intent": "learning" | "QA" | "creation" | "unknown",
    "confidence": 0.0到1.0之间的浮点数,
    "parameters": {
        "keywords": ["提取的关键实体或词汇"],
        "action": "用户期望的具体动作（如：生成图片、查询历史、制定计划等）"
    },
    "reply": "如果是 unknown，请给出一个友好的回退提示（如：抱歉，我没能理解您的意图。您可以问我关于非遗的知识，让我帮您制定学习计划，或者为您创作非遗相关的图片）；如果是其他意图，请留空字符串。"
}"""

        # 构造消息
        messages = []
        if conversation_history:
            # 只取最近几条历史以提供上下文，防止 Token 溢出
            for msg in conversation_history[-4:]:
                messages.append(msg)
                
        messages.append({"role": "user", "content": query})
        
        try:
            # 调用 LLM 进行意图识别
            # langchain_service.chat 内部使用了 try/except 并返回默认文本，
            # 这里如果失败会返回 "抱歉..."，所以后续解析 JSON 会失败进入 except
            response_text = self.llm.chat(messages, system_prompt=system_prompt)
            
            # 清理可能的 markdown 标记
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:]
            
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
                
            clean_text = clean_text.strip()
            
            result = json.loads(clean_text)
            
            # 验证返回的结果结构
            intent = result.get("intent", "unknown")
            if intent not in ["learning", "QA", "creation", "unknown"]:
                intent = "unknown"
                result["intent"] = intent
                
            if intent == "unknown" and not result.get("reply"):
                result["reply"] = "抱歉，我不太清楚您想做什么。您可以向我提问关于非遗的知识，让我制定学习计划，或者让我为您创作相关内容。"
                
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Intent JSON parsing failed: {e}. LLM Output: {response_text}")
            return self._get_fallback_result(query)
        except Exception as e:
            logger.error(f"Intent detection failed: {e}")
            return self._get_fallback_result(query)

    def _get_fallback_result(self, query: str) -> Dict[str, Any]:
        """降级逻辑：当意图识别失败时，通过关键词匹配进行保底识别"""
        lower_query = query.lower()
        
        if any(kw in lower_query for kw in ["画", "生成", "创作", "设计", "图片", "图", "海报"]):
            intent = "creation"
            action = "创作"
        elif any(kw in lower_query for kw in ["学", "教程", "步骤", "教我", "计划"]):
            intent = "learning"
            action = "学习"
        elif any(kw in lower_query for kw in ["什么", "谁", "哪", "历史", "介绍", "为什么", "怎么", "了解"]):
            intent = "QA"
            action = "问答"
        else:
            intent = "unknown"
            action = ""
            
        reply = "抱歉，我没能理解您的意图。您可以问我关于非遗的知识，让我帮您制定学习计划，或者为您创作非遗相关的图片。" if intent == "unknown" else ""
            
        return {
            "intent": intent,
            "confidence": 0.5,
            "parameters": {
                "keywords": [],
                "action": action
            },
            "reply": reply
        }

# 全局单例
intent_service = IntentService()
