import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Digital Inheritor Backend"
    API_V1_STR: str = "/api/v1"

    # Neo4j Settings
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "fusu2023yzcm")

    # MySQL Settings
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = os.getenv("MYSQL_PORT", 3306)
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "123456")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "inheritor_db")

    # LLM Settings - DeepSeek
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "sk-ef663e51e8224d99803c7fbc6f137a86")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # Elasticsearch Settings
    ES_URL: str = os.getenv("ES_URL", "http://localhost:9200")
    ES_INDEX_NAME: str = os.getenv("ES_INDEX_NAME", "ich_knowledge")

    # Image Generation Settings (Cloud API)
    IMAGE_API_KEY: str = os.getenv("IMAGE_API_KEY", "")
    IMAGE_API_URL: str = os.getenv("IMAGE_API_URL", "https://api.siliconflow.cn/v1/images/generations")
    IMAGE_MODEL: str = os.getenv("IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

    class Config:
        case_sensitive = True

settings = Settings()
