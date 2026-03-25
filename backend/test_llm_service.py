import asyncio
import os
from app.services.llm_service import langchain_service

async def test_llm_service():
    print("--- 1. Testing ChatPromptTemplate and Memory ---")
    session_id = "test-user-001"
    kg_context = "皮影戏是中国民间古老的传统艺术，老北京人称其为'驴皮影'。"
    
    # Round 1
    question1 = "皮影戏是什么？"
    print(f"\nUser: {question1}")
    answer1, _ = langchain_service.answer_with_context(question1, kg_context, session_id=session_id)
    print(f"Assistant: {answer1}")
    
    # Round 2 - Testing Memory
    question2 = "老北京人叫它什么？"
    print(f"\nUser: {question2}")
    answer2, _ = langchain_service.answer_with_context(question2, kg_context, session_id=session_id)
    print(f"Assistant: {answer2}")
    
    print("\n--- 2. Testing Streaming Response ---")
    question3 = "详细讲讲皮影戏的特点"
    print(f"\nUser: {question3}")
    print("Assistant (Streaming): ", end="", flush=True)
    async for chunk in langchain_service.stream_answer_with_context(question3, kg_context, session_id=session_id):
        print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(test_llm_service())
