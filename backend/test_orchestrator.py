from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_orchestrator_qa_intent():
    """
    测试问答意图
    """
    payload = {
        "query": "昆曲的历史是什么？"
    }
    response = client.post("/api/v1/orchestrator/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # 验证意图
    assert data["intent"]["intent"] == "QA"
    
    # 验证任务分解
    tasks = data["tasks"]
    assert len(tasks) > 0
    # 至少有一个任务调用了 rag_query
    assert any(t["method"] == "rag_query" for t in tasks)
    
    # 验证结果汇总
    assert "final_answer" in data
    print("QA Final Answer:", data["final_answer"])


def test_orchestrator_creation_intent():
    """
    测试创作意图
    """
    payload = {
        "query": "帮我生成一张漂亮的传统戏曲脸谱海报"
    }
    response = client.post("/api/v1/orchestrator/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # 验证意图
    assert data["intent"]["intent"] == "creation"
    
    # 验证任务分解
    tasks = data["tasks"]
    assert len(tasks) > 0
    # 至少有一个任务调用了 generate_image
    assert any(t["method"] == "generate_image" for t in tasks)
    
    # 验证结果汇总
    assert "final_answer" in data
    print("Creation Final Answer:", data["final_answer"])


def test_orchestrator_learning_intent():
    """
    测试学习意图
    """
    payload = {
        "query": "我想学习怎么制作皮影，能给我个步骤吗？"
    }
    response = client.post("/api/v1/orchestrator/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # 验证意图
    assert data["intent"]["intent"] == "learning"
    
    # 验证任务分解
    tasks = data["tasks"]
    assert len(tasks) > 0
    # 至少有一个任务调用了 generate_learning_plan
    assert any(t["method"] == "generate_learning_plan" for t in tasks)
    
    # 验证结果汇总
    assert "final_answer" in data
    print("Learning Final Answer:", data["final_answer"])

if __name__ == "__main__":
    print("Running orchestrator tests...")
    print("-" * 50)
    print("Testing QA intent...")
    test_orchestrator_qa_intent()
    print("QA intent test passed.")
    print("-" * 50)
    
    print("Testing Creation intent...")
    test_orchestrator_creation_intent()
    print("Creation intent test passed.")
    print("-" * 50)
    
    print("Testing Learning intent...")
    test_orchestrator_learning_intent()
    print("Learning intent test passed.")
    print("-" * 50)
    
    print("All tests passed successfully!")
