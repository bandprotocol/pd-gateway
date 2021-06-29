from os import environ
import requests

from flask import Request, Response, current_app

from pdgateway import create_app
from pdgateway.query import UserQuery

class CoinGeckoUserQuery():
    def query(self, request: Request) -> Response:
        ids = request.args.getlist('ids')
        params = {
            'ids': ','.join(ids),
            'vs_currencies': 'usd',
        }
        print('Config can be accessed here')
        print('API_KEY:', current_app.config['API_KEY'])
        resp = requests.get('https://api.coingecko.com/api/v3/simple/price', params=params)
        return resp.json(), resp.status_code

def main():
    app = create_app(CoinGeckoUserQuery(), {
        'API_KEY': environ.get('COINGECKO_API_KEY'),
        'BANDCHAIN_REST_ENDPOINT': 'http://localhost:8080',
    })
    app.run('0.0.0.0', 3000)

if __name__ == "__main__":
    main()
