from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'User Management API'
    PROJECT_VERSION: str = '1.0.3'
    DATABASE_URL: str = 'sqlite:///./test.db'

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = '.env'


settings = Settings()
