import requests
import json
from config import keys, api_key


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(values):
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        quote, base, amount = values
        if quote == base:
            raise APIException(f"Вы ввели одинаковые валюты: {quote} и {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не верно введено количество {amount}")

        r = requests.get(f"https://free.currconv.com/api/v7/convert?apiKey={api_key}&q={quote_ticker}_{base_ticker}&compact=ultra")
        total_base = (json.loads(r.content)[f'{quote_ticker}_{base_ticker}']) * amount

        return round(total_base, 2)








