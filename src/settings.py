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

settings = Settings()
