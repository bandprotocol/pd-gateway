import os

from typing import Any, Mapping
from flask import Flask, Response, request, jsonify
from .verify import check_required_headers, verify_request
from .cache import LRUCache

def create_app(config: Mapping[str, Any]) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if 'BANDCHAIN_REST_ENDPOINT' not in config:
        raise ValueError("BandChain REST endpoint is required")
    app.config.from_mapping(config)

    cache = LRUCache(maxsize=128)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a hook function to verify requests before doing other things
    @app.before_request
    def verify():
        app.logger.info(request.headers)
        if check_required_headers(request.headers):
            app.logger.info('miss')
            return jsonify({ "error": "there are missing required headers" }), 400

        if cache.is_hit(request.headers.get("BAND_SIGNATURE")):
            return jsonify({"error": "duplicated request not allowed"}), 403

        is_valid, response = verify_request(request.headers)
        if not is_valid:
            return jsonify({"error": response}), 400

    # a hook function to temporarily remember request to prevent from
    # duplicated requests.
    @app.after_request
    def update_cache(response: Response) -> Response:
        if response.status_code == 200:
            cache.put(key=request.headers.get("BAND_SIGNATURE"), val=None)
        return response

    return app
