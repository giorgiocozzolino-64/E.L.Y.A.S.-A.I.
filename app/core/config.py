from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "E.L.Y.A.S.-A.I."
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+psycopg2://elyas:elyas_password@db:5432/elyas"
    JWT_SECRET: str = "CHANGE_ME_SUPER_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"


settings = Settings()
