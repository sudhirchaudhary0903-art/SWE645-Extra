from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Required — no defaults; app will raise ValidationError on startup if missing
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    # Optional with safe defaults
    DB_PORT: int = 3306
    APP_ENV: str = "development"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
