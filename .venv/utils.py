import requests
import json
from config import keys

class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {quote}.')

        if quote not in keys:
            raise ConvertionException(
                f"Валюта '{quote}' не поддерживается")
        if base not in keys:
            raise ConvertionException(f"Валюта '{base}' не поддерживается.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Количество '{amount}' должно быть числом.")

        quote_ticker = keys[quote]
        base_ticker = keys[base]
        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConvertionException(f"Ошибка при запросе к API: {e}")

        rate = json.loads(r.content).get(base_ticker)
        if rate is None:
            raise ConvertionException(f"Не удалось получить данные о курсе для валюты '{base}'.")

        return rate * amount