from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List

from app.services.orchestrator.task_orchestrator import task_orchestrator
from app.services.orchestrator.intent_recognition import intent_recognizer

router = APIRouter()

class OrchestratorRequest(BaseModel):
    query: str

class OrchestratorResponse(BaseModel):
    status: str
    original_query: str
    tasks_executed: int
    results: Dict[str, Any]

class IntentRequest(BaseModel):
    query: str

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    message: str

@router.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate_task(request: OrchestratorRequest):
    """
    Main endpoint for orchestrating complex user queries.
    It decomposes the query, routes it to the right agents via MCP, and aggregates results.
    """
    try:
        result = await task_orchestrator.orchestrate(request.query)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recognize-intent", response_model=IntentResponse)
async def recognize_intent(request: IntentRequest):
    """
    Endpoint to explicitly test intent recognition
    """
    try:
        intent, confidence, msg = intent_recognizer.recognize(request.query)
        return IntentResponse(
            intent=intent,
            confidence=confidence,
            message=msg
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
