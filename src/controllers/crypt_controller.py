import logging
import requests
from settings import settings
from utils.exceptions import CryptoException

headers = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
            logger.info(f"Resposta do crypto: {response.text}")
            return None
        elif response.status_code == 200:
            try:
                data = response.json()
                encrypted_message = data.get("encrypted_message")
                if not encrypted_message:
                    logger.error("Resposta inválida do servidor de criptografia")
                    raise CryptoException("Resposta inválida do servidor de criptografia: falta 'encrypted_message'")
                logger.info("Criptografado com sucesso.")
                return encrypted_message
            except Exception as e:
                logger.error(f"Erro ao processar resposta do servidor de criptografia: {e}")
                raise CryptoException(f"Erro ao processar resposta do servidor de criptografia: {e}")
        else:
            logger.error("Não foi possível comunicar com o servidor de criptografia")
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
                    logger.error("Resposta inválida do servidor de criptografia")
                    raise CryptoException("Resposta inválida do servidor de criptografia: falta 'decrypted_message'")
                logger.info("Descriptografado com sucesso.")
                return decrypted_message
            except Exception as e:
                logger.error(f"Erro ao processar resposta do servidor de criptografia: {e}")
                raise CryptoException(f"Erro ao processar resposta do servidor de criptografia: {e}")
        else:
            logger.error("Não foi possível comunicar com o servidor de criptografia")
            raise CryptoException("Não foi possível comunicar com o servidor de criptografia")
