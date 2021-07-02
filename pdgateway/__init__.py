import os

from typing import Any, Mapping
from flask import Flask, request, jsonify
from .verify import verify_request

def create_app(config: Mapping[str, Any]) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if 'BANDCHAIN_REST_ENDPOINT' not in config:
        raise ValueError("BandChain REST endpoint is required")
    app.config.from_mapping(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.before_request
    def verify():
        is_valid, response = verify_request(request.headers)
        if not is_valid:
            return jsonify({"error": response}), 400

    return app