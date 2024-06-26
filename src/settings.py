import os

class Settings:
    def __init__(self):
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
        self.MONGO_DATABASE_URI = os.getenv("MONGO_DATABASE_URI", "mongodb://localhost:27017")
        self.MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "user-dev")
        self.USER_COLLECTION = "users"
        self.MONGO_BIOMETRICS_DATABASE_NAME = os.getenv("MONGO_BIOMETRICS_DATABASE_NAME", "biometrics-dev")
        self.BIOMETRICS_COLLECTION = "biometrics"
        self.VALID_DOCUMENTS_EXTENSIONS = ["doc", "docx", "pdf", "jpg", "jpeg", "png", "xml"]
        self.CRYPTO_PUBLIC_KEY = os.getenv("CRYPTO_PUBLIC_KEY", "public-key")
        self.CRYPTO_PRIVATE_KEY = os.getenv("CRYPTO_PRIVATE_KEY", "private-key")
        self.CRYPTO_URL = "https://5a7udyuiimjx3rngjs7lp4dxee0phmbl.lambda-url.us-east-1.on.aws"
        self.EXPENSES_API = "https://back-end-d5im.onrender.com"
        self.USER_EXPENSES_API = os.getenv("USER_EXPENSES_API" ,"email-expanses")
        self.PASSWORD_EXPENSES_API = os.getenv("PASSWORD_EXPENSES_API" ,"123")

settings = Settings()
