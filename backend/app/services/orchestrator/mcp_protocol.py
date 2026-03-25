import json
import logging
from typing import Dict, Any, Callable, Optional, List
from pydantic import BaseModel, Field
import uuid
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_protocol")

class MCPMessage(BaseModel):
    """
    MCP Message Format Specification
    Following a JSON-RPC 2.0 like structure
    """
    jsonrpc: str = "2.0"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    method: str  # e.g., "vision_mentor.analyze_pose"
    params: Dict[str, Any] = Field(default_factory=dict)

class MCPResponse(BaseModel):
    """
    MCP Response Format Specification
    """
    jsonrpc: str = "2.0"
    id: str
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

class MCPServer:
    """
    MCP Server / Router
    Handles Service Registration, Discovery, and Routing
    """
    def __init__(self):
        self.registry: Dict[str, Dict[str, Callable]] = {}
        logger.info("MCP Server initialized")

    def register_agent(self, agent_name: str, methods: Dict[str, Callable]):
        """
        Service Registration
        """
        self.registry[agent_name] = methods
        logger.info(f"Registered agent: {agent_name} with methods: {list(methods.keys())}")

    def discover_services(self) -> Dict[str, List[str]]:
        """
        Service Discovery
        """
        return {agent: list(methods.keys()) for agent, methods in self.registry.items()}

    async def route_message(self, message: MCPMessage) -> MCPResponse:
        """
        Message Routing
        """
        logger.info(f"Routing message: id={message.id}, method={message.method}")
        start_time = time.time()
        
        try:
            parts = message.method.split('.')
            if len(parts) != 2:
                raise ValueError("Method must be in format 'agent_name.method_name'")
            
            agent_name, method_name = parts
            
            if agent_name not in self.registry:
                raise ValueError(f"Agent '{agent_name}' not found")
                
            if method_name not in self.registry[agent_name]:
                raise ValueError(f"Method '{method_name}' not found in agent '{agent_name}'")
                
            handler = self.registry[agent_name][method_name]
            
            # Execute the handler (assuming async for future proofing)
            import inspect
            if inspect.iscoroutinefunction(handler):
                result = await handler(**message.params)
            else:
                result = handler(**message.params)
                
            elapsed = time.time() - start_time
            logger.info(f"Message {message.id} processed successfully in {elapsed:.3f}s")
            
            return MCPResponse(id=message.id, result=result)
            
        except Exception as e:
            logger.error(f"Error processing message {message.id}: {str(e)}")
            return MCPResponse(
                id=message.id,
                error={"code": -32000, "message": str(e)}
            )

# Global MCP Server Instance
mcp_server = MCPServer()
