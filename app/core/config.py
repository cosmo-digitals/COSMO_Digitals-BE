from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "my_fastapi_db"

    class Config:
        env_file = ".env"

settings = Settings()
