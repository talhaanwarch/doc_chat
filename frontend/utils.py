from pydantic import  BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes the BaseSettings from pydantic for environment variables.
    """

    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    bucket_name: str
    secret_key: str
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O.
    """
    return Settings()