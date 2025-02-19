from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class to load environment variables from .env file.
    """

    fastapi_host: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    settings = Settings()
    print(f"FASTAPI_HOST: {settings.fastapi_host}")

except ValueError as e:
    print(f"Error loading settings: {e}")
    # Ensure .env file exists.  Create a dummy one if it doesn't.
    env_file_path = Path(".env")
    if not env_file_path.exists():
        print(".env file not found. Creating a dummy one.")
        with open(".env", "w") as f:
            f.write("FASTAPI_HOST=http://127.0.0.1")
