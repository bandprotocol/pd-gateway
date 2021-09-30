#!/usr/bin/env python3
import requests
import sys
import os
import typing

HEADERS = {"Content-Type": "application/json"}

# Reads values from Yoda Executor's environment variables
def set_header_from_env(headers: typing.Dict[str, str], key: str):
    value = os.environ.get(key)
    if value != None:
        headers[key] = value


# Create request verification info as HTTP headers
def set_request_verification_headers(existingHeaders: typing.Dict[str, str]) -> typing.Dict[str, str]:
    newHeaders = existingHeaders.copy()
    set_header_from_env(newHeaders, "BAND_CHAIN_ID")
    set_header_from_env(newHeaders, "BAND_VALIDATOR")
    set_header_from_env(newHeaders, "BAND_REQUEST_ID")
    set_header_from_env(newHeaders, "BAND_EXTERNAL_ID")
    set_header_from_env(newHeaders, "BAND_REPORTER")
    set_header_from_env(newHeaders, "BAND_SIGNATURE")
    return newHeaders


# This data source receives 2 arguments.
# The first argument is Gateway's endpoint, which is used for testing purpose only.
# The seconds argument is a string of comma-separated symbols
def main(endpoint, raw_symbols):
    # Prepare request verification info
    headers = set_request_verification_headers(HEADERS)

    # Get coin IDs to query price from CoinGecko
    symbols = raw_symbols.split(",")
    params = {"symbols": symbols}

    # Send GET request to Premium Data Source's Gateway
    r = requests.get(endpoint, headers=headers, params=params)
    r.raise_for_status()

    # Receive a response constructed by your own implementation of the Gateway
    # For this case, the response is an object with id as key and price as value
    # ordered respectively to given symbols
    prices = r.json()["result"]

    # Construct the result to be handled by Oracle Script
    # For this case, the result should be comma-separated
    return ",".join(prices)


if __name__ == "__main__":
    try:
        print(main(sys.argv[1], sys.argv[2]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
