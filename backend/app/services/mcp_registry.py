import logging
from typing import Callable, Dict, Any, Awaitable
from app.core.mcp import MCPRequest, MCPResponse

# Configure logger for this module
logger = logging.getLogger(__name__)

# Handler type alias for readability: accepts a dictionary of parameters and returns anything asynchronously
MCPHandlerType = Callable[[Dict[str, Any]], Awaitable[Any]]

class MCPRegistry:
    """
    Registry for Model Context Protocol (MCP) services.
    Handles service registration, discovery, and message routing.
    """
    def __init__(self):
        self._handlers: Dict[str, MCPHandlerType] = {}
        logger.info("MCPRegistry initialized successfully.")

    def register(self, method: str) -> Callable[[MCPHandlerType], MCPHandlerType]:
        """
        Decorator to register a method handler.
        
        Usage:
            @mcp_registry.register("my_method")
            async def my_handler(params: dict):
                ...
        """
        def decorator(func: MCPHandlerType) -> MCPHandlerType:
            if method in self._handlers:
                logger.warning(f"Overwriting existing handler for MCP method: '{method}'")
            self._handlers[method] = func
            logger.info(f"Registered MCP method handler: '{method}' -> {func.__name__}")
            return func
        return decorator

    async def route_request(self, request: MCPRequest) -> MCPResponse:
        """
        Route an incoming MCPRequest to the appropriate registered handler.
        
        Args:
            request (MCPRequest): The incoming request model.
            
        Returns:
            MCPResponse: The response model containing either result or error.
        """
        logger.info(f"Routing MCP request ID: {request.id}, Method: '{request.method}'")
        
        if request.method not in self._handlers:
            error_msg = f"Method not found: '{request.method}'"
            logger.error(f"Routing failed for request ID: {request.id} - {error_msg}")
            return MCPResponse(
                id=request.id,
                error={"code": -32601, "message": error_msg}
            )
        
        handler = self._handlers[request.method]
        try:
            params = request.params or {}
            logger.debug(f"Executing handler for '{request.method}' with params: {params}")
            
            # Execute the handler asynchronously
            result = await handler(params)
            
            logger.info(f"Successfully processed request ID: {request.id}")
            return MCPResponse(id=request.id, result=result)
            
        except Exception as e:
            error_msg = f"Error executing handler for '{request.method}': {str(e)}"
            logger.exception(f"Exception in request ID {request.id}: {error_msg}")
            return MCPResponse(
                id=request.id,
                error={"code": -32000, "message": str(e)}
            )

# Create a global registry instance for the application
mcp_registry = MCPRegistry()
