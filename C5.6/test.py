import requests
import json

from config import api_key


r = requests.get(f"https://free.currconv.com/api/v7/convert?apiKey=f37fed031b6296950e3c&q=USD_RUB&compact=ultra")
# total_base = (json.loads(r.content)['USD_RUB']) * 10
print(r.content)

