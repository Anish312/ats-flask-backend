import os

class Settings:
    PROJECT_NAME: str = 'Python ML Service'
    VERSION: str = '1.0.0'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))

settings = Settings()
