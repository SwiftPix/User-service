from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    MONGO_DATABASE_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE_NAME: str = "user-dev"
    USER_COLLECTION: str = "users"
    MONGO_BIOMETRICS_DATABASE_NAME: str = "biometrics-dev"
    BIOMETRICS_COLLECTION: str = "biometrics"
    VALID_DOCUMENTS_EXTENSIONS: list = ['pdf', 'jpg', 'jpeg', 'png']
    CRYPTO_PUBLIC_KEY: str = "public-key"
    CRYPTO_PRIVATE_KEY: str = "private-key"
    CRYPTO_URL: str = "http://crypto-service"

settings = Settings()
