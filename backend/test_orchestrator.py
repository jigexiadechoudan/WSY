import asyncio
import httpx
import json

API_BASE_URL = "http://127.0.0.1:8002/api/v1/orchestrator"

async def test_intent_recognition():
    print("\n--- Testing Intent Recognition ---")
    queries = [
        "我想学昆曲兰花指，帮我看看身段",
        "什么是紫砂壶的泥料？",
        "帮我画一幅苏绣风格的猫",
        "随便聊聊天"
    ]
    
    async with httpx.AsyncClient() as client:
        for query in queries:
            response = await client.post(
                f"{API_BASE_URL}/recognize-intent",
                json={"query": query}
            )
            result = response.json()
            print(f"Query: {query}")
            print(f"Intent: {result['intent']} (Confidence: {result['confidence']})")
            if result['message']:
                print(f"Message: {result['message']}")
            print("-" * 30)

async def test_task_orchestration():
    print("\n--- Testing Task Orchestration ---")
    queries = [
        "给我讲讲什么是青花瓷", # Single task
        "我想学这个兰花指并把它画出来", # Multi-task decomposition
    ]
    
    async with httpx.AsyncClient() as client:
        for query in queries:
            print(f"\nOrchestrating Query: {query}")
            response = await client.post(
                f"{API_BASE_URL}/orchestrate",
                json={"query": query}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"Status: {result['status']}")
                print(f"Tasks Executed: {result['tasks_executed']}")
                print("Results:")
                print(json.dumps(result['results'], indent=2, ensure_ascii=False))
            else:
                print(f"Error: {response.text}")
            print("-" * 30)

async def main():
    print("Starting Orchestrator Tests...")
    await test_intent_recognition()
    await test_task_orchestration()
    print("\nTests Completed.")

if __name__ == "__main__":
    asyncio.run(main())
