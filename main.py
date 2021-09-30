from os import environ
import requests
from requests.auth import HTTPBasicAuth

from flask import request, current_app

from pdgateway import create_app

# Here, we can create a new Flask app with any preferred configuration,
# which can be set from a constant, environment variables, or files.
app = create_app(
    config={
        "API_KEY": environ.get("API_KEY"),
        "BANDCHAIN_REST_ENDPOINT": "http://localhost:1317",
        "PREMIUM_ENDPOINT": environ.get("PREMIUM_ENDPOINT"),
    }
)

# This is an example of implementation of query function,
# which queries coin prices from CoinGecko.
# Feel free to implement this function in your own way.
@app.route("/", methods=["GET"])
def query():
    # Get CoinGecko's IDs given by data source script
    symbols = request.args.getlist("symbols")
    params = {
        "symbols": symbols,
    }

    # This is an example of accessing app configuration,
    # which accesses value of API_KEY.
    api_key = current_app.config["API_KEY"]
    current_app.logger.debug("API_KEY:", api_key)
    auth = HTTPBasicAuth(apiKey, api_key)

    endpoint = current_app.config["PREMIUM_ENDPOINT"]

    # Send an HTTP request to CoinGecko to get coin prices
    resp = requests.get(endpoint, params=params, auth=auth)

    # The response may be directly returned without any modification
    # and allow the data source script to modify it before returning result to oracle script
    return resp.json(), resp.status_code


def main():
    # Run the application listening to port 3000
    app.run("0.0.0.0", 3000)


if __name__ == "__main__":
    main()
