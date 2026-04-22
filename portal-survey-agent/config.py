from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AGENT_ENV: str = "development"
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    MCP_SERVER_URL: str = "http://portal-survey-api:8000/mcp"
    API_BASE_URL: str = "http://portal-survey-api:8000"
    ALLOWED_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
