# bitkub-api-v3
python bitkub api

import BitkubAPI

api_key = ""
secret_key = ""

bitkub = BitkubAPI.BitkubAPI(api_key=api_key, api_secret=secret_key)

balances = bitkub.get_balances()

print(balances)
