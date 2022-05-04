from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Products microservice"
    offers_base_url: str
    offers_access_token: str

    class Config:
        env_file = ".env"


settings = Settings()
