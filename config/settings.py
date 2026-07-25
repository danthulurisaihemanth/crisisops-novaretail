import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    app_name: str = "NovaRetail CrisisOps AI"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    langsmith_tracing: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "novaretail-crisisops")
    data_dir: str = os.getenv("DATA_DIR", "data")

    def __getattr__(self, name: str) -> str:
        return ""

settings = Settings()
