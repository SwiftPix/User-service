import requests
from settings import settings
from utils.exceptions import CryptoException

headers = {"Content-Type": "application/json"}


class CryptController:
    @staticmethod
    def encrypt(message):
        payload = {
            "message": message,
            "public_key": settings.CRYPTO_PUBLIC_KEY
        }

        url = f"{settings.CRYPTO_URL}/rsa/encrypt"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 422:
            return None
        elif response.status_code == 200:
            data = response.json()
            encrypted_message = data["encrypted_message"]
            return encrypted_message
        else:
            raise CryptoException("Não foi possível comunicar com o servidor de criptografia")
        
    @staticmethod
    def decrypt(message):
        payload = {
            "message": message,
            "private_key": settings.CRYPTO_PRIVATE_KEY
        }

        url = f"{settings.CRYPTO_URL}/rsa/decrypt"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 422:
            return None
        elif response.status_code == 200:
            data = response.json()
            decrypted_message = data["decrypted_message"]
            return decrypted_message
        else:
            raise CryptoException("Não foi possível comunicar com o servidor de criptografia")