import json
import re
import logging
from typing import Dict, Any, Tuple
from app.services.llm_service import langchain_service

logger = logging.getLogger("intent_recognition")

class IntentRecognizer:
    """
    User Intent Recognition Module
    Identifies if a user wants to: learn (学习), qa (问答), or create (创作)
    """
    
    INTENTS = {
        "learn": "学习 (如：我想学苏绣、教我兰花指、分析我的身段)",
        "qa": "问答 (如：什么是紫砂壶、苏绣的起源、非遗相关知识查询)",
        "create": "创作 (如：帮我画一张青花瓷、生成线稿、创作一幅画)"
    }
    
    def __init__(self):
        self.fallback_keywords = {
            "learn": ["学", "教我", "练习", "动作", "身段", "纠正", "怎么做", "指导"],
            "qa": ["什么", "起源", "历史", "介绍", "是谁", "哪些", "解释", "讲讲"],
            "create": ["画", "生成", "设计", "创作", "做一张", "搞一张", "图", "照片", "线稿"]
        }
        
    def _fallback_recognition(self, user_query: str) -> str:
        """Rule-based fallback if LLM is unavailable"""
        scores = {"learn": 0, "qa": 0, "create": 0}
        
        for intent, keywords in self.fallback_keywords.items():
            for kw in keywords:
                if kw in user_query:
                    scores[intent] += 1
                    
        # Find intent with max score
        max_intent = max(scores, key=scores.get)
        
        # If score is 0, we can't confidently identify
        if scores[max_intent] == 0:
            return "unknown"
            
        return max_intent

    def recognize(self, user_query: str) -> Tuple[str, float, str]:
        """
        Recognize user intent.
        
        Args:
            user_query: User's input text
            
        Returns:
            Tuple containing:
            - Intent ('learn', 'qa', 'create', or 'unknown')
            - Confidence score (0.0 to 1.0)
            - Friendly response if unknown, else empty string
        """
        logger.info(f"Recognizing intent for: '{user_query}'")
        
        system_prompt = """你是一个智能意图识别引擎，负责将用户的自然语言输入分类到特定的意图。
你需要识别出用户指令属于以下哪一种类别：
1. 'learn' (学习): 用户想要学习技能、练习动作、需要指导或身段分析（例如：我想学苏绣、看看我这个兰花指对不对、教我怎么做）。
2. 'qa' (问答): 用户想了解知识、询问事实、历史或背景（例如：什么是紫砂壶、昆曲的历史、这幅画是谁画的）。
3. 'create' (创作): 用户希望生成图片、画画、设计、创作艺术品（例如：帮我画个青花瓷、根据这幅图生成线稿、设计个图案）。
4. 'unknown' (未知): 无法归类到上述三种意图，或者指令不清晰。

规则：
- 返回结果必须是纯 JSON 格式，不包含 Markdown 标记。
- 格式：{"intent": "learn|qa|create|unknown", "confidence": 0.0-1.0}
- 如果包含“画”、“生成”且不是询问知识，通常是 create。
- 如果包含“学”、“练习”、“对不对”，通常是 learn。
- 如果是纯粹的提问，通常是 qa。
"""
        messages = [{"role": "user", "content": f"请识别以下输入意图：\n{user_query}"}]
        
        try:
            # Check if LLM is initialized
            if langchain_service.llm:
                response = langchain_service.chat(messages, system_prompt)
                
                # Clean up response to parse JSON
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:-3]
                elif cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response[3:-3]
                    
                result = json.loads(cleaned_response)
                intent = result.get("intent", "unknown")
                confidence = float(result.get("confidence", 0.0))
                
                if intent not in ["learn", "qa", "create"]:
                    intent = "unknown"
                    
                logger.info(f"LLM recognized intent: {intent} (confidence: {confidence})")
                
            else:
                # Use fallback rule-based method
                intent = self._fallback_recognition(user_query)
                confidence = 0.8 if intent != "unknown" else 0.0
                logger.info(f"Fallback recognized intent: {intent} (confidence: {confidence})")
                
        except Exception as e:
            logger.error(f"Intent recognition error: {e}")
            intent = self._fallback_recognition(user_query)
            confidence = 0.6 if intent != "unknown" else 0.0
            
        if intent == "unknown" or confidence < 0.5:
            friendly_message = (
                "抱歉，我不太明白您的意思。您可以尝试这样对我说：\n"
                "- 学习指导：「我想学昆曲兰花指」、「帮我看看这个身段对不对」\n"
                "- 知识问答：「什么是紫砂壶？」、「苏绣有什么历史？」\n"
                "- 艺术创作：「帮我画一幅青花瓷风格的画」"
            )
            return "unknown", confidence, friendly_message
            
        return intent, confidence, ""

intent_recognizer = IntentRecognizer()
