from pydantic import  BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes the BaseSettings from pydantic for environment variables.
    """

    postgres_db: str
    postgres_user: str
    postgres_host: str
    postgres_password: str
    postgres_port: int
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O.
    """
    return Settings()