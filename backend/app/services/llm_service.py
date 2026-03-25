"""
LangChain LLM 服务封装
支持 DeepSeek 模型调用
实现流式响应、历史记忆和 Prompt 模板
"""

from typing import List, Tuple, Dict, Any, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.core.config import settings

class LangChainService:
    """LangChain LLM 服务"""

    def __init__(self):
        """初始化 LLM"""
        try:
            # 基础 LLM 实例
            self.llm = ChatOpenAI(
                model_name=settings.DEEPSEEK_MODEL,
                openai_api_key=settings.DEEPSEEK_API_KEY,
                openai_api_base=settings.DEEPSEEK_BASE_URL,
                temperature=0.7,
                max_tokens=1024,
                streaming=True  # 启用流式支持
            )
            
            # 用于保存不同 session 的历史记忆
            self.store: Dict[str, BaseChatMessageHistory] = {}
            
            # 建立带历史记忆的问答 Chain
            self._setup_qa_chain()
            
            print("LangChain LLM initialized successfully with DeepSeek")
        except Exception as e:
            print(f"Failed to initialize LangChain LLM: {e}")
            self.llm = None
            self.qa_chain_with_history = None

    def _setup_qa_chain(self):
        """配置基于知识图谱问答的 Prompt 模板和 Chain"""
        system_prompt = """你是一位非遗文化知识馆长，博学且友善。你的职责是根据提供的知识图谱信息回答用户关于非物质文化遗产的问题。

回答规则：
1. 基于提供的知识图谱信息回答，不要编造信息
2. 如果知识图谱中没有相关信息，诚实地告诉用户
3. 回答要清晰、详细，但不要过于冗长（200-300 字为宜）
4. 保持友善、专业的语气
5. 适当引导用户了解更多细节"""

        human_prompt = """以下是从知识图谱中检索到的相关信息：
{context}

如果上述信息中没有包含用户问题的答案，请诚实地告知用户。

用户问题：{question}"""

        # 使用 ChatPromptTemplate 创建模板
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", human_prompt)
        ])
        
        # 组装 Chain
        chain = self.qa_prompt | self.llm
        
        # 封装带记忆的 Chain
        self.qa_chain_with_history = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """获取或创建特定 session 的对话历史"""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """
        进行简单对话 (保留向后兼容)
        """
        if not self.llm:
            return "抱歉，AI 服务暂时不可用。"

        langchain_messages = []
        if system_prompt:
            langchain_messages.append(SystemMessage(content=system_prompt))

        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        try:
            response = self.llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            print(f"LLM chat error: {e}")
            return "抱歉，我现在无法回答您的问题，请稍后再试。"

    def generate_follow_up_questions(self, context: str, user_query: str, answer: str) -> list:
        """生成追问选项"""
        prompt = f"""你是一个非遗文化知识助手的追问生成器。根据以下对话内容，生成 3 个用户可能感兴趣的追问问题。

上下文信息：
{context}

用户问题：{user_query}

助手回答：{answer}

请生成 3 个相关的追问问题，要求：
1. 问题应该与上下文和回答相关
2. 问题应该具体、明确
3. 问题应该是用户可能真正想知道的
4. 每个问题控制在 30 字以内

直接输出 3 个问题，用 | 分隔，不要输出其他内容。"""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            questions = [q.strip() for q in response.content.split('|') if q.strip()]
            return questions[:3]
        except Exception as e:
            print(f"Generate follow-up questions error: {e}")
            return [
                "这个技艺的历史起源是什么？",
                "有哪些代表性的传承人？",
                "现代如何保护和发展这项技艺？"
            ]

    def answer_with_context(self, question: str, kg_context: str, conversation_history: list = None, session_id: str = "default") -> tuple:
        """
        基于知识图谱上下文回答问题 (结合历史记忆)
        """
        if not self.qa_chain_with_history:
            return "抱歉，AI 服务未正确初始化。", []
            
        # 同步传入的 conversation_history 到 LangChain Memory
        history = self.get_session_history(session_id)
        if conversation_history and not history.messages:
            for msg in conversation_history:
                if msg["role"] == "user":
                    history.add_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    history.add_ai_message(msg["content"])
                    
        try:
            response = self.qa_chain_with_history.invoke(
                {"context": kg_context, "question": question},
                config={"configurable": {"session_id": session_id}}
            )
            answer = response.content
            
            # 生成追问
            follow_ups = self.generate_follow_up_questions(kg_context, question, answer)
            return answer, follow_ups
        except Exception as e:
            print(f"Answer with context error: {e}")
            return "抱歉，我现在无法回答您的问题，请稍后再试。", []

    async def stream_answer_with_context(self, question: str, kg_context: str, session_id: str = "default") -> AsyncGenerator[str, None]:
        """
        异步流式回答问题 (结合历史记忆)
        """
        if not self.qa_chain_with_history:
            yield "抱歉，AI 服务未正确初始化。"
            return
            
        try:
            async for chunk in self.qa_chain_with_history.astream(
                {"context": kg_context, "question": question},
                config={"configurable": {"session_id": session_id}}
            ):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            print(f"Stream answer error: {e}")
            yield "抱歉，流式输出发生错误，请稍后再试。"


# 全局实例
langchain_service = LangChainService()
