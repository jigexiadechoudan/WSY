from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class MCPMessage(BaseModel):
    """Base model for all MCP (Model Context Protocol) messages."""
    version: str = Field(default="1.0", description="Protocol version")

class MCPRequest(MCPMessage):
    """MCP Request model."""
    id: str = Field(..., description="Unique request identifier")
    method: str = Field(..., description="Method to invoke")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Parameters for the method")

class MCPResponse(MCPMessage):
    """MCP Response model."""
    id: str = Field(..., description="Request identifier this response corresponds to")
    result: Optional[Any] = Field(None, description="Result of the successful invocation")
    error: Optional[Dict[str, Any]] = Field(None, description="Error details if the invocation failed")

class MCPNotification(MCPMessage):
    """MCP Notification model (one-way message without response)."""
    method: str = Field(..., description="Notification method")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Notification parameters")
