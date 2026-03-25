from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import vision_mentor, knowledge_curator, creative_artisan, orchestrator
from app.services.orchestrator.mcp_protocol import mcp_server

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vision_mentor.router, prefix=f"{settings.API_V1_STR}/vision", tags=["Vision Mentor"])
app.include_router(knowledge_curator.router, prefix=f"{settings.API_V1_STR}/knowledge", tags=["Knowledge Curator"])
app.include_router(creative_artisan.router, prefix=f"{settings.API_V1_STR}/creative", tags=["Creative Artisan"])
app.include_router(orchestrator.router, prefix=f"{settings.API_V1_STR}/orchestrator", tags=["Master Orchestrator"])

# Register agent methods to MCP Server
async def dummy_vision_analyze(query: str):
    return {"message": "Vision analysis complete", "query": query}

async def dummy_knowledge_qa(query: str):
    return {"message": "Knowledge answer generated", "query": query}

async def dummy_creative_generate(query: str):
    return {"message": "Creative image generated", "query": query}

mcp_server.register_agent("vision_mentor", {
    "analyze_pose": dummy_vision_analyze
})
mcp_server.register_agent("knowledge_curator", {
    "qa": dummy_knowledge_qa
})
mcp_server.register_agent("creative_artisan", {
    "generate": dummy_creative_generate
})

@app.get("/")
def root():
    return {"message": "Welcome to Digital Inheritor API"}
