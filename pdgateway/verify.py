import requests
from flask import json, current_app
from typing import Dict, Tuple
from requests import exceptions
from werkzeug.datastructures import Headers

REQUIRED_HEADERS = [
    "BAND_CHAIN_ID",
    "BAND_VALIDATOR",
    "BAND_REQUEST_ID",
    "BAND_EXTERNAL_ID",
    "BAND_REPORTER",
    "BAND_SIGNATURE",
]

# verify_request verifies incoming requests by sending the info
# to your BandChain node before accessing your exclusive API.
def verify_request(headers: Headers) -> Tuple[bool, Dict]:
    bandchain_url = current_app.config["BANDCHAIN_REST_ENDPOINT"]
    vfrq_url = bandchain_url + "/oracle/v1/verify_request"

    if not all(header_name in headers for header_name in REQUIRED_HEADERS):
        return False, { "error": "There are missing required headers" }

    chain_id = headers.get("BAND_CHAIN_ID")
    validator_addr = headers.get("BAND_VALIDATOR")
    request_id = headers.get("BAND_REQUEST_ID")
    external_id = headers.get("BAND_EXTERNAL_ID")
    reporter = headers.get("BAND_REPORTER")
    signature = headers.get("BAND_SIGNATURE")
    params = {
        "chain_id": chain_id,
        "validator": validator_addr,
        "request_id": request_id,
        "external_id": external_id,
        "reporter": reporter,
        "signature": signature
    }
    print("verify request with {}".format(json.dumps(params)))
    try:
        res = requests.get(url=vfrq_url, params=params)
        if res.status_code == 200:
            return True, res.json()
        else:
            print("request verification is NOT valid: {}".format(res.text))
            return False, res.json()
    except exceptions.RequestException as e:
        print("execption occurred when verify request: {}".format(str(e)))
        return False, { "error": str(e) }