import asyncio
import time
import json
from app.services.intent_service import intent_service

TEST_CASES = [
    {"query": "我想学苏绣的起针技法", "expected": "learning"},
    {"query": "如何制作皮影戏？", "expected": "learning"},
    {"query": "给我制定一个学习紫砂壶的计划", "expected": "learning"},
    {"query": "怎么入门中国结剪纸？", "expected": "learning"},
    
    {"query": "皮影戏的发源地在哪里？", "expected": "QA"},
    {"query": "苏绣有哪些著名的传承人？", "expected": "QA"},
    {"query": "介绍一下四大名绣", "expected": "QA"},
    {"query": "紫砂壶的泥料都有哪些种类？", "expected": "QA"},
    
    {"query": "帮我生成一张苏绣风格的牡丹图", "expected": "creation"},
    {"query": "设计一个关于紫砂壶的宣传海报", "expected": "creation"},
    {"query": "用皮影戏风格画一只老虎", "expected": "creation"},
    {"query": "画一幅水墨画风格的江南水乡", "expected": "creation"},
    
    {"query": "今天天气怎么样？", "expected": "unknown"},
    {"query": "你好，能帮我写个Python代码吗？", "expected": "unknown"},
    {"query": "周末去哪玩比较好", "expected": "unknown"}
]

async def run_test():
    print(f"开始测试意图识别，共 {len(TEST_CASES)} 个测试用例...\n")
    
    correct_count = 0
    total_time = 0
    
    print(f"{'查询 (Query)':<30} | {'预期 (Expected)':<10} | {'实际 (Actual)':<10} | {'耗时 (Time)':<10} | {'结果 (Result)'}")
    print("-" * 85)
    
    for case in TEST_CASES:
        query = case["query"]
        expected = case["expected"]
        
        start_time = time.time()
        result = await intent_service.detect_intent(query)
        end_time = time.time()
        
        cost_time = end_time - start_time
        total_time += cost_time
        
        actual = result.get("intent", "error")
        is_correct = actual == expected
        
        if is_correct:
            correct_count += 1
            res_str = "✅ Pass"
        else:
            res_str = "❌ Fail"
            
        print(f"{query:<30} | {expected:<10} | {actual:<10} | {cost_time:.2f}s     | {res_str}")
        
    accuracy = correct_count / len(TEST_CASES) * 100
    avg_time = total_time / len(TEST_CASES)
    
    print("\n" + "=" * 50)
    print(f"测试完成!")
    print(f"总用例数: {len(TEST_CASES)}")
    print(f"正确识别: {correct_count}")
    print(f"准确率:   {accuracy:.2f}%")
    print(f"总耗时:   {total_time:.2f}s")
    print(f"平均响应: {avg_time:.2f}s")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_test())
