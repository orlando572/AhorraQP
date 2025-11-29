from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "AhorraQP"
    DEBUG: bool = False
    
    # Configuración de scraping
    SCRAPER_TIMEOUT: int = 30
    HEADLESS_BROWSER: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()