import requests
from flask import json, current_app
from typing import Dict, Tuple
from requests import exceptions
from werkzeug.datastructures import Headers

REQUIRED_HEADERS = [
    "Band-Chain-Id",
    "Band-Validator",
    "Band-Request-Id",
    "Band-External-Id",
    "Band-Reporter",
    "Band-Signature",
]

def check_required_headers(headers: Headers) -> bool:
    current_app.logger.info('test required_headers')
    current_app.logger.info('REQUIRED_HEADERS:' + str(REQUIRED_HEADERS))
    current_app.logger.info([h for h in headers])
    if all(header_name in headers for header_name in REQUIRED_HEADERS):
        return True
    else:
        return False

# verify_request verifies incoming requests by sending the info
# to your BandChain node before accessing your exclusive API.
def verify_request(headers: Headers) -> Tuple[bool, Dict]:
    bandchain_url = current_app.config["BANDCHAIN_REST_ENDPOINT"]
    vfrq_url = bandchain_url + "/oracle/v1/verify_request"

    chain_id = headers.get("Band-Chain-Id")
    validator_addr = headers.get("Band-Validator")
    request_id = headers.get("Band-Request-Id")
    external_id = headers.get("Band-External-Id")
    reporter = headers.get("Band-Reporter")
    signature = headers.get("Band-Signature")
    params = {
        "chain_id": chain_id,
        "validator": validator_addr,
        "request_id": request_id,
        "external_id": external_id,
        "reporter": reporter,
        "signature": signature
    }
    current_app.logger.info(bandchain_url)
    current_app.logger.info("verify request with {}".format(json.dumps(params)))
    try:
        res = requests.get(url=vfrq_url, params=params)
        if res.status_code == 200:
            return True, res.json()
        else:
            current_app.logger.warning("request verification is NOT valid: {}".format(res.text))
            return False, res.json()
    except exceptions.RequestException as e:
        current_app.logger.error("execption occurred when verify request: {}".format(str(e)))
        return False, { "error": str(e) }