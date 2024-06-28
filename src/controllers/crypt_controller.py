import requests
from settings import settings
from utils.exceptions import CryptoException

headers = {"Content-Type": "application/json"}

class CryptController:
    @staticmethod
    def encrypt(message):
        # Certifique-se de que a mensagem tem até 180 caracteres e está no formato correto
        if len(message) > 180:
            raise CryptoException("A mensagem deve ter 180 caracteres ou menos.")
        
        payload = {
            "message": message,
            "public_key": settings.CRYPTO_PUBLIC_KEY
        }

        url = f"{settings.CRYPTO_URL}/rsa/encrypt"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 422:
            return None
        elif response.status_code == 200:
            try:
                data = response.json()
                encrypted_message = data.get("encrypted_message")
                if not encrypted_message:
                    raise CryptoException("Resposta inválida do servidor de criptografia: falta 'encrypted_message'")
                return encrypted_message
            except Exception as e:
                raise CryptoException(f"Erro ao processar resposta do servidor de criptografia: {e}")
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
            try:
                data = response.json()
                decrypted_message = data.get("decrypted_message")
                if not decrypted_message:
                    raise CryptoException("Resposta inválida do servidor de criptografia: falta 'decrypted_message'")
                return decrypted_message
            except Exception as e:
                raise CryptoException(f"Erro ao processar resposta do servidor de criptografia: {e}")
        else:
            raise CryptoException("Não foi possível comunicar com o servidor de criptografia")
