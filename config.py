from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_URL: str
    API_KEY: str
    TARGET_NETWORK_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()