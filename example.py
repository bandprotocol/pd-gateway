from os import environ
import requests

from flask import request, current_app

from pdgateway import create_app

# Here, we can create a new Flask app with any preferred configuration,
# which can be set from a constant, environment variables, or files.
app = create_app(config={
    'API_KEY': environ.get('COINGECKO_API_KEY'),
    'BANDCHAIN_REST_ENDPOINT': 'http://localhost:1317',
})

# This is an example of implementation of query function,
# which queries coin prices from CoinGecko.
# Feel free to implement this function in your own way.
@app.route('/', methods=['GET'])
def query():
    # Get CoinGecko's IDs given by data source script
    ids = request.args.getlist('ids')
    params = {
        'ids': ','.join(ids),
        'vs_currencies': 'usd',
    }

    # This is an example of accessing app configuration,
    # which accesses value of API_KEY.
    apiKey = current_app.config['API_KEY']
    current_app.logger.debug('API_KEY:', apiKey)

    # Send an HTTP request to CoinGecko to get coin prices
    resp = requests.get('https://api.coingecko.com/api/v3/simple/price', params=params)
    
    # The response may be directly returned without any modification
    # and allow the data source script to modify it before returning result to oracle script
    return resp.json(), resp.status_code

def main():
    # Run the application listening to port 3000
    app.run('0.0.0.0', 3000)

if __name__ == "__main__":
    main()
