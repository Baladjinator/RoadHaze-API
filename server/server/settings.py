from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int

    class Config:
        env_file = '.env'

settings = Settings()