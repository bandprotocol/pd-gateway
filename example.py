from os import environ
import requests

from flask import Request, Response, current_app

from pdgateway import create_app
from pdgateway.query import UserQuery

# This is an example of implementation on UserQuery
# This class will query data from the exclusive API
class CoinGeckoUserQuery():
    def query(self, request: Request) -> Response:
        # Get coin IDs given by data source script
        ids = request.args.getlist('ids')
        params = {
            'ids': ','.join(ids),
            'vs_currencies': 'usd',
        }

        # Note that sensitive information e.g. API keys can be accessed from
        # Flask's configuration
        print('Config can be accessed here')
        print('API_KEY:', current_app.config['API_KEY'])

        resp = requests.get('https://api.coingecko.com/api/v3/simple/price', params=params)
        # We can return response without any modification
        # and let the data source script modify it before return result to oracle script
        return resp.json(), resp.status_code

def main():
    # Here, we can create a new Flask app with any preferred configuration.
    # We can collect data from environment variable
    # Or, modify `app` instance to fit your needs.
    app = create_app(CoinGeckoUserQuery(), {
        'API_KEY': environ.get('COINGECKO_API_KEY'),
        'BANDCHAIN_REST_ENDPOINT': 'http://localhost:1317',
    })

    # Then, run the app
    app.run('0.0.0.0', 3000)

if __name__ == "__main__":
    main()
