from requests.exceptions import RequestException
from pdgateway import create_app
import unittest

import responses
import json
from pdgateway.verify import check_required_headers, verify_request


class TestCheckRequiredHeaders(unittest.TestCase):
    def test_success(self):
        # Band-Request-Id is missing
        is_valid = check_required_headers({
            "Band-Chain-Id": "bandchain",
            "Band-Validator": "bandcoolvalidator",
            "Band-External-Id": "2",
            "Band-Reporter": "bandcoolreporter",
            "Band-Signature": "coolsignature",
            "Band-Request-Id": "1",
        })
        self.assertTrue(is_valid)

    def test_incomplete_params(self):
        # Band-Request-Id is missing
        is_valid = check_required_headers({
            "Band-Chain-Id": "bandchain",
            "Band-Validator": "bandcoolvalidator",
            "Band-External-Id": "2",
            "Band-Reporter": "bandcoolreporter",
            "Band-Signature": "coolsignature",
        })
        self.assertFalse(is_valid)

class TestRequestVerification(unittest.TestCase):
    success_response_body = {
        "chain_id":       "bandchain",
        "validator":      "bandvalidatoraddress1234",
        "request_id":     "1234",
        "external_id":    "3",
        "data_source_id": "2",
    }
    failed_response_body = {
        "code": 3,
        "message": "rpc error: error of example",
        "details": [],
    }
    app = create_app({
        'TESTING': True,
        "BANDCHAIN_REST_ENDPOINT": "http://localhost.example"
    })

    def tearDown(self) -> None:
        return super().tearDown()

    @responses.activate
    def test_success(self):
        responses.add(**{
            "method": responses.GET,
            "url": "http://localhost.example/oracle/v1/verify_request",
            "body": json.dumps(self.success_response_body),
            "status": 200,
            "content_type": "application/json",
        })
        with self.app.app_context():
            is_valid, result = verify_request({
                "Band-Chain-Id": "bandchain",
                "Band-Validator": "bandcoolvalidator",
                "Band-Request-Id": "4285",
                "Band-External-Id": "2",
                "Band-Reporter": "bandcoolreporter",
                "Band-Signature": "coolsignature",
            })
        self.assertTrue(is_valid)
        self.assertEqual(result, self.success_response_body)

    @responses.activate
    def test_invalid_request(self):
        responses.add(**{
            "method": responses.GET,
            "url": "http://localhost.example/oracle/v1/verify_request",
            "body": json.dumps(self.failed_response_body),
            "status": 400,
            "content_type": "application/json",
        })
        with self.app.app_context():
            is_valid, result = verify_request({
                "Band-Chain-Id": "bandchain",
                "Band-Validator": "bandcoolvalidator",
                "Band-Request-Id": "4285",
                "Band-External-Id": "2",
                "Band-Reporter": "bandcoolreporter",
                "Band-Signature": "coolsignature",
            })
        self.assertFalse(is_valid)
        self.assertEqual(result, self.failed_response_body)

    @responses.activate
    def test_exception(self):
        responses.add(**{
            "method": responses.GET,
            "url": "http://localhost.example/oracle/v1/verify_request",
            "body": RequestException('testexception'),
        })
        with self.app.app_context():
            is_valid, result = verify_request({
                "Band-Chain-Id": "bandchain",
                "Band-Validator": "bandcoolvalidator",
                "Band-Request-Id": "4285",
                "Band-External-Id": "2",
                "Band-Reporter": "bandcoolreporter",
                "Band-Signature": "coolsignature",
            })
        self.assertFalse(is_valid)
        self.assertEqual(result, { "error": "testexception" })
