import json
import uuid
import asyncio
import logging
from typing import Dict, Any, List
from app.services.intent_service import intent_service
from app.services.llm_service import langchain_service
from app.services.mcp_registry import mcp_registry
from app.core.mcp import MCPRequest

logger = logging.getLogger(__name__)

class OrchestratorService:
    """
    多 Agent 任务编排引擎
    负责将意图识别结果分解为具体任务，通过 MCP 协议分发执行（支持串行与并行），并汇总最终结果。
    """
    def __init__(self):
        self.intent_service = intent_service
        self.llm = langchain_service
        
    async def process_request(self, query: str, session_id: str = None, history: List[Dict] = None) -> Dict[str, Any]:
        """
        处理用户请求的核心流程
        1. 意图识别
        2. 任务分解
        3. 任务执行（调度）
        4. 结果汇总
        """
        logger.info(f"Processing request: {query}")
        
        # 1. 意图识别
        intent_result = await self.intent_service.detect_intent(query, history)
        intent = intent_result.get("intent", "unknown")
        logger.info(f"Detected intent: {intent}")
        
        # 2. 任务分解
        tasks = await self._decompose_tasks(query, intent_result)
        logger.info(f"Decomposed into {len(tasks)} tasks")
        
        # 3. 任务执行 (支持串行与并行)
        results = await self._execute_tasks(tasks)
        logger.info("Task execution completed")
        
        # 4. 结果汇总
        final_answer = await self._aggregate_results(query, tasks, results)
        logger.info("Result aggregation completed")
        
        return {
            "intent": intent_result,
            "tasks": tasks,
            "results": results,
            "final_answer": final_answer
        }
        
    async def _decompose_tasks(self, query: str, intent_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根据用户查询和意图，利用 LLM 进行任务分解。
        """
        system_prompt = """你是一个任务编排引擎。根据用户的输入和意图，将其分解为一系列可以通过工具执行的子任务。
可用的 MCP 方法（工具）包括：
- rag_query: 用于查询非遗相关的知识、历史、人物、剧目等。参数: {"query": "查询的具体内容"}
- generate_image: 用于生成图片、海报等。参数: {"prompt": "生成图片的提示词(英文)"}
- generate_learning_plan: 用于制定非遗技艺的学习计划。参数: {"topic": "学习主题"}
- chat_reply: 用于闲聊或当不涉及具体业务逻辑时的直接回复。参数: {"message": "回复内容"}

请输出严格的 JSON 数组，每个任务包含以下字段：
- id: 任务的唯一标识（如 "task_1"）
- method: 调用的 MCP 方法名
- params: 传递给方法的参数字典
- dependencies: 依赖的任务 id 列表（空列表表示可以并行执行）

示例：
[
  {
    "id": "task_1",
    "method": "rag_query",
    "params": {"query": "昆曲的历史"},
    "dependencies": []
  },
  {
    "id": "task_2",
    "method": "generate_image",
    "params": {"prompt": "A beautiful traditional Chinese opera stage"},
    "dependencies": []
  }
]
"""
        messages = [{"role": "user", "content": f"用户输入: {query}\n意图识别结果: {json.dumps(intent_result, ensure_ascii=False)}\n请进行任务分解。"}]
        response = self.llm.chat(messages, system_prompt=system_prompt)
        
        try:
            clean_text = response.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            tasks = json.loads(clean_text)
            return tasks
        except Exception as e:
            logger.error(f"Task decomposition failed: {e}. Fallback to default tasks.")
            # 降级逻辑
            intent = intent_result.get("intent")
            if intent == "QA":
                return [{"id": "task_1", "method": "rag_query", "params": {"query": query}, "dependencies": []}]
            elif intent == "creation":
                return [{"id": "task_1", "method": "generate_image", "params": {"prompt": query}, "dependencies": []}]
            elif intent == "learning":
                return [{"id": "task_1", "method": "generate_learning_plan", "params": {"topic": query}, "dependencies": []}]
            else:
                return [{"id": "task_1", "method": "chat_reply", "params": {"message": query}, "dependencies": []}]

    async def _execute_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        根据任务依赖关系执行任务流，支持并发执行无依赖的任务。
        """
        results = {}
        pending_tasks = {t["id"]: t for t in tasks}
        completed_tasks = set()
        
        while pending_tasks:
            # 找出所有依赖已满足的任务
            executable = []
            for task_id, task in pending_tasks.items():
                deps = task.get("dependencies", [])
                if all(dep in completed_tasks for dep in deps):
                    executable.append(task)
            
            if not executable:
                logger.error("Deadlock detected in task execution: unresolved dependencies.")
                break
                
            # 并发执行满足条件的任务
            async def run_task(task):
                try:
                    req = MCPRequest(
                        id=str(uuid.uuid4()),
                        method=task["method"],
                        params=task["params"]
                    )
                    res = await mcp_registry.route_request(req)
                    if res.error:
                        return task["id"], f"Error: {res.error.get('message', 'Unknown error')}"
                    return task["id"], res.result
                except Exception as e:
                    logger.exception(f"Error executing task {task['id']}")
                    return task["id"], f"Exception: {str(e)}"
                
            tasks_futures = [run_task(t) for t in executable]
            batch_results = await asyncio.gather(*tasks_futures)
            
            for task_id, result in batch_results:
                results[task_id] = result
                completed_tasks.add(task_id)
                del pending_tasks[task_id]
                
        return results

    async def _aggregate_results(self, query: str, tasks: List[Dict[str, Any]], results: Dict[str, Any]) -> str:
        """
        汇总各个任务的执行结果，生成最终的自然语言回复。
        """
        system_prompt = "你是一个专业的结果汇总助手。请根据用户的原始查询和各个子任务的执行结果，组织成最终的自然语言回复给用户。要求回答连贯、自然，符合语境。"
        
        context = f"用户查询: {query}\n\n子任务执行结果:\n"
        for task in tasks:
            task_id = task["id"]
            method = task["method"]
            res = results.get(task_id, "无结果")
            
            # 如果结果过长（例如完整的RAG回答），截取或者转换为字符串
            res_str = str(res)
            if len(res_str) > 1000:
                res_str = res_str[:1000] + "...(省略)"
                
            context += f"- 任务 [{method}]: {res_str}\n"
            
        messages = [{"role": "user", "content": context}]
        final_answer = self.llm.chat(messages, system_prompt=system_prompt)
        return final_answer

# 全局单例
orchestrator_service = OrchestratorService()

# 注册默认的 MCP 方法供 Orchestrator 使用
import asyncio
from app.services.rag_service import rag_service
from app.services.image_service import cloud_image_service

@mcp_registry.register("rag_query")
async def handle_rag_query(params: dict):
    query = params.get("query", "")
    # rag_service.query 是同步方法，使用 to_thread 避免阻塞
    return await asyncio.to_thread(rag_service.query, query)

@mcp_registry.register("generate_image")
async def handle_generate_image(params: dict):
    prompt = params.get("prompt", "")
    return await cloud_image_service.generate_image(prompt)

@mcp_registry.register("generate_learning_plan")
async def handle_generate_learning_plan(params: dict):
    topic = params.get("topic", "")
    prompt = f"请为主题 '{topic}' 制定一个非遗学习计划。"
    return langchain_service.chat([{"role": "user", "content": prompt}])

@mcp_registry.register("chat_reply")
async def handle_chat_reply(params: dict):
    message = params.get("message", "")
    return langchain_service.chat([{"role": "user", "content": message}])

