import asyncio
import logging
from typing import List, Dict, Any
from app.services.orchestrator.mcp_protocol import mcp_server, MCPMessage
from app.services.orchestrator.intent_recognition import intent_recognizer

logger = logging.getLogger("task_orchestrator")

class TaskNode:
    """Represents a decomposed task unit"""
    def __init__(self, task_id: str, intent: str, query: str, dependencies: List[str] = None):
        self.task_id = task_id
        self.intent = intent
        self.query = query
        self.dependencies = dependencies or []
        self.status = "pending"
        self.result = None

class TaskOrchestrator:
    """
    Multi-Agent Task Orchestration Module
    """
    
    def decompose_task(self, user_query: str) -> List[TaskNode]:
        """
        Decompose a complex task into multiple sub-tasks.
        E.g. "学这个并画出来" -> [Task1: learn, Task2: create]
        """
        logger.info(f"Decomposing task: {user_query}")
        
        # Simple rule-based decomposition for now
        # Could be enhanced with LLM parsing
        sub_tasks = []
        
        # Split by keywords
        # If "并", "然后", "再" are in query, we might have multiple tasks
        if "并" in user_query or "然后" in user_query:
            parts = user_query.replace("然后", "并").split("并")
            
            for i, part in enumerate(parts):
                part = part.strip()
                if not part:
                    continue
                    
                intent, conf, _ = intent_recognizer.recognize(part)
                
                # If unknown, default to QA or skip if too short
                if intent == "unknown":
                    if len(part) > 2:
                        intent = "qa"
                    else:
                        continue
                        
                deps = [sub_tasks[-1].task_id] if sub_tasks else []
                node = TaskNode(f"task_{i}", intent, part, deps)
                sub_tasks.append(node)
                
        else:
            intent, conf, msg = intent_recognizer.recognize(user_query)
            if intent != "unknown":
                sub_tasks.append(TaskNode("task_0", intent, user_query))
            else:
                # If unknown, just return an empty list or a special task
                sub_tasks.append(TaskNode("task_unknown", "unknown", user_query))
                
        return sub_tasks

    async def execute_task_node(self, node: TaskNode) -> Any:
        """
        Execute a single task node by routing it via MCP Protocol
        """
        node.status = "running"
        logger.info(f"Executing {node.task_id} with intent {node.intent}: {node.query}")
        
        # Mapping intent to corresponding agent's entry method
        agent_method_map = {
            "learn": "vision_mentor.analyze_pose",
            "qa": "knowledge_curator.qa",
            "create": "creative_artisan.generate"
        }
        
        method = agent_method_map.get(node.intent)
        if not method:
            node.status = "failed"
            return {"error": f"Unsupported intent: {node.intent}"}
            
        message = MCPMessage(
            method=method,
            params={"query": node.query}
        )
        
        response = await mcp_server.route_message(message)
        
        node.status = "completed" if not response.error else "failed"
        node.result = response.result if not response.error else response.error
        
        return node.result

    async def orchestrate(self, user_query: str) -> Dict[str, Any]:
        """
        Main orchestration entry point
        """
        # 1. Task Decomposition
        sub_tasks = self.decompose_task(user_query)
        
        if not sub_tasks:
            return {"status": "error", "message": "无法解析任务意图"}
            
        if len(sub_tasks) == 1 and sub_tasks[0].intent == "unknown":
            _, _, msg = intent_recognizer.recognize(user_query)
            return {"status": "error", "message": msg}
            
        logger.info(f"Task decomposed into {len(sub_tasks)} sub-tasks")
        
        # 2. Execution Engine (Support for serial/parallel)
        # For simplicity, we execute nodes based on their dependencies.
        # If a node has no dependencies or its dependencies are completed, it can run.
        
        results = {}
        pending_tasks = sub_tasks.copy()
        completed_task_ids = set()
        
        while pending_tasks:
            runnable_tasks = [
                t for t in pending_tasks 
                if all(dep in completed_task_ids for dep in t.dependencies)
            ]
            
            if not runnable_tasks:
                # Deadlock or cyclic dependency
                logger.error("Deadlock detected in task orchestration")
                break
                
            # Execute runnable tasks in parallel
            execution_coroutines = [self.execute_task_node(t) for t in runnable_tasks]
            batch_results = await asyncio.gather(*execution_coroutines, return_exceptions=True)
            
            for task, result in zip(runnable_tasks, batch_results):
                results[task.task_id] = {
                    "intent": task.intent,
                    "query": task.query,
                    "result": result
                }
                completed_task_ids.add(task.task_id)
                pending_tasks.remove(task)
                
        # 3. Result Aggregation
        return {
            "status": "success",
            "original_query": user_query,
            "tasks_executed": len(completed_task_ids),
            "results": results
        }

task_orchestrator = TaskOrchestrator()
