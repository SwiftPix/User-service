import logging
import requests
from datetime import datetime
from settings import settings
from utils.exceptions import ExpensesException

headers = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ExpensesController:
    @staticmethod
    def auth():
        payload = {
            "email": settings.USER_EXPENSES_API,
            "password": settings.PASSWORD_EXPENSES_API
        }

        url = f"{settings.EXPENSES_API}/auth"

        response = requests.post(url, json=payload, headers=headers)
        logger.info(f"Resposta do servidor de despesas: {response.status_code}")
        if response.status_code != 200:
            logger.error("Não foi possível comunicar com o servidor de despesas")
            raise ExpensesException("Não foi possível comunicar com o servidor de despesas")
        return
    
    @staticmethod
    def register(email, password):
        payload = {
            "email": email,
            "password": password
        }

        url = f"{settings.EXPENSES_API}/user/register"

        response = requests.post(url, json=payload, headers=headers)

        logger.info(f"Resposta do servidor de despesas: {response.status_code}")

        if response.status_code != 201:
            logger.error("Não foi possível comunicar com o servidor de despesas")
            raise ExpensesException("Não foi possível comunicar com o servidor de despesas")
        data = response.json()
        return data["id"]
    
    @staticmethod
    def create_expense(user_external_id, reason, value, category):
        payload = {
            "name": reason,
            "amount": value,
            "expiration_date": datetime.now().strftime('%Y-%m-%d'),
            "paid": True,
            "payment_date": datetime.now().strftime('%Y-%m-%d'),
            "category": category
        }

        url = f"{settings.EXPENSES_API}/budget/v1/revenue/create/{user_external_id}/"

        response = requests.post(url, json=payload, headers=headers)

        logger.info(f"Resposta do servidor de despesas: {response.status_code}")

        if response.status_code != 200:
            logger.error("Não foi possível comunicar com o servidor de despesas")
            raise ExpensesException("Não foi possível comunicar com o servidor de despesas")
        data = response.json()
        return data
    
    @staticmethod
    def list_expenses(user_external_id):
        url = f"{settings.EXPENSES_API}/budget/v1/revenue/list/{user_external_id}/"

        response = requests.get(url, headers=headers)

        logger.info(f"Resposta do servidor de despesas: {response.status_code}")

        if response.status_code != 200:
            logger.error("Não foi possível comunicar com o servidor de despesas")
            raise ExpensesException("Não foi possível comunicar com o servidor de despesas")
        data = response.json()
        return data
    
    @staticmethod
    def list_expenses_categories():
        url = f"{settings.EXPENSES_API}/budget/v1/revenue/list-categories/"

        response = requests.get(url, headers=headers)

        logger.info(f"Resposta do servidor de despesas: {response.status_code}")

        if response.status_code != 200:
            logger.error("Não foi possível comunicar com o servidor de despesas")
            raise ExpensesException("Não foi possível comunicar com o servidor de despesas")
        data = response.json()
        return data