# bitkub-api-v3

# test
import BitkubAPI

api_key = ""
secret_key = ""

bitkub = BitkubAPI.BitkubAPI(api_key=api_key, api_secret=secret_key)

balances = bitkub.get_balances()

print(balances)
