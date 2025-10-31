from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: str = Field("3306", alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    app_port: str = Field("8081", alias="APP_PORT")
    app_host: str = Field("localhost", alias="APP_HOST")
    # JWT settings
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    #Openweather API
    openweather_api_key: str = Field(..., alias="openweather_api_key")

    class Config:
        env_file = ENV_PATH
        extra = "allow"
        populate_by_name = True
        case_sensitive = True

    @property
    def tmp_db(self) -> str:
        return f'{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
    
    @property
    def database_url(self) -> str:
        return f'mysql+aiomysql://{self.tmp_db}'
    
    @property
    def backend_url(self) -> str:
        return f'http://{self.app_host}:{self.app_port}'
    
settings = Settings()