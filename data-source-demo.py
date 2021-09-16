#!/usr/bin/env python3
import requests
import sys
import os
import typing

# List of supported coins as demonstration
COINS_LIST = {
  "ETH": "ethereum",
  "BTC": "bitcoin",
  "BNB": "binancecoin",
  "UNI": "uniswap",
  "USDT": "tether",
  "BAND": "band-protocol",
}

HEADERS = {"Content-Type": "application/json"}

# Reads values from Yoda Executor's environment variables
def set_header_from_env(headers: typing.Dict[str, str], key: str):
  value = os.environ.get(key)
  if value != None:
    headers[key] = value

# Create request verification info as HTTP headers
def set_request_verification_headers(existingHeaders: typing.Dict[str, str]) -> typing.Dict[str, str]:
  newHeaders = existingHeaders.copy()
  set_header_from_env(newHeaders, "Band-Chain-Id")
  set_header_from_env(newHeaders, "Band-Validator")
  set_header_from_env(newHeaders, "Band-Request-Id")
  set_header_from_env(newHeaders, "Band-External-Id")
  set_header_from_env(newHeaders, "Band-Reporter")
  set_header_from_env(newHeaders, "Band-Signature")
  return newHeaders

# Convert symbols to coin IDs based on `/coins/list` of CoinGecko
def get_ids_from_symbols(symbols: typing.List[str]) -> typing.List[str]:
  ids = []
  for symbol in symbols:
    if symbol in COINS_LIST:
      ids.append(COINS_LIST[symbol])
  return ids

# This data source receives 2 arguments.
# The first argument is Gateway's endpoint, which is used for testing purpose only.
# The seconds argument is a string of comma-separated symbols
def main(endpoint, raw_symbols):
  # Prepare request verification info 
  headers = set_request_verification_headers(HEADERS)

  # Get coin IDs to query price from CoinGecko
  symbols = raw_symbols.split(",")
  ids = get_ids_from_symbols(symbols)
  params = { "ids": ids }

  # Send GET request to Premium Data Source's Gateway
  r = requests.get(endpoint, headers=headers, params=params)
  r.raise_for_status()

  # Receive a response constructed by your own implementation of the Gateway
  # For this case, the response is an object with id as key and price as value
  # ordered respectively to given symbols
  result = r.json()
  priceList = []
  for id in ids:
    priceList.append(str(result[id]["usd"]))

  if len(priceList) != len(symbols):
    raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")

  # Construct the result to be handled by Oracle Script
  # For this case, the result should be comma-separated
  return ",".join(priceList)

if __name__ == "__main__":
  try:
    print(main(sys.argv[1], sys.argv[2]))
  except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
