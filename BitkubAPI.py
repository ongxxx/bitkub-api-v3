import hashlib
import hmac
import json
import time
import requests
# import urllib3
# urllib3.disable_warnings()


class BitkubAPI:
    def __init__(self, api_key, api_secret):
        self.host = 'https://api.bitkub.com'
        self.api_key = api_key
        self.api_secret = api_secret

    def gen_sign(self, payload_string):
        return hmac.new(self.api_secret.encode('utf-8'), payload_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def gen_query_param(self, url, query_param):
        req = requests.PreparedRequest()
        req.prepare_url(url, query_param)
        return req.url.replace(url, "")

    def get_ticker(self):
        path = '/api/market/ticker'
        get_data = requests.get(self.host + path).json()
        return get_data

    def get_balances(self):
        path = '/api/v3/market/balances'
        ts = str(round(time.time() * 1000))
        payload = [ts, 'POST', path]
        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.post(self.host + path, headers=headers)
        return response.json()

    def create_buy_order(self, symbol, amount, price):
        path = '/api/v3/market/place-bid'
        ts = str(round(time.time() * 1000))
        body = {
            'sym': symbol,  # {quote}_{base}
            'amt': amount,
            'rat': price,
            'typ': 'limit'  # limit, market
        }
        payload = [ts, 'POST', path, json.dumps(body)]
        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.post(self.host + path, headers=headers, data=json.dumps(body))
        return response.json()

    def create_sell_order(self, symbol, amount, price):
        path = '/api/v3/market/place-ask'
        ts = str(round(time.time() * 1000))
        body = {
            'sym': symbol,  # {quote}_{base}
            'amt': amount,
            'rat': price,
            'typ': 'limit'  # limit, market
        }
        payload = [ts, 'POST', path, json.dumps(body)]
        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.post(self.host + path, headers=headers, data=json.dumps(body))
        return response.json()

    def get_order_info(self, symbol, order_id, side, order_hash=None):
        path = '/api/v3/market/order-info'

        ts = str(round(time.time() * 1000))
        param = {
            'sym': symbol,  # symbol in quote_base format: e.g. btc_thb
            'id': order_id,  # order id
            'sd': side,  # side buy or sell
            # "hash":"", # order hash (optional)
        }
        query_param = self.gen_query_param(self.host + path, param)

        payload = [ts, 'GET', path, query_param]

        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.get(f'{self.host}{path}{query_param}', headers=headers, data={})
        return response.json()

    def get_my_open_order(self, symbol):
        path = '/api/v3/market/my-open-orders'
        param = {
            'sym': symbol
        }
        ts = str(round(time.time() * 1000))
        query_param = self.gen_query_param(self.host + path, param)
        payload = [ts, 'GET', path, query_param]
        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.get(f'{self.host}{path}{query_param}', headers=headers, data={})
        return response.json()

    def cancel_order(self, symbol, order_id, side):
        """
        :param symbol:btc_thb
        :param order_id:string Order id
        :param side:string buy or sell
        """
        path = '/api/v3/market/cancel-order'
        ts = str(round(time.time() * 1000))
        body = {
            'sym': symbol,
            'id': order_id,
            'sd': side,
        }
        payload = [ts, 'POST', path, json.dumps(body)]
        sig = self.gen_sign(''.join(payload))
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-TIMESTAMP': ts,
            'X-BTK-SIGN': sig,
            'X-BTK-APIKEY': self.api_key
        }
        response = requests.post(self.host + path, headers=headers, data=json.dumps(body))
        return response.json()

