from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ESP32-S3 Vibe Coding AI Agent"
    API_V1_STR: str = "/api/v1"
    
    # LLM Settings
    DOUBAO_API_KEY: str = ""
    DOUBAO_ENDPOINT_ID: str = ""  # Model ID like ep-2024...
    DOUBAO_API_BASE: str = "https://ark.cn-beijing.volces.com/api/v3"
    
    class Config:
        env_file = ".env"

settings = Settings()
