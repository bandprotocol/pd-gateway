from requests.exceptions import RequestException
from pdgateway.query import UserQuery
from pdgateway import create_app
import unittest

import responses
import json
from pdgateway.verify import verify_request

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
    app = create_app(UserQuery(), {
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
                "BAND_CHAIN_ID": "bandchain",
                "BAND_VALIDATOR": "bandcoolvalidator",
                "BAND_REQUEST_ID": "4285",
                "BAND_EXTERNAL_ID": "2",
                "BAND_REPORTER": "bandcoolreporter",
                "BAND_SIGNATURE": "coolsignature",
            })
        self.assertTrue(is_valid)
        self.assertEqual(result, self.success_response_body)
    
    def test_incomplete_params(self):
        # BAND_REQUEST_ID is missing
        with self.app.app_context():
            is_valid, result = verify_request({
                "BAND_CHAIN_ID": "bandchain",
                "BAND_VALIDATOR": "bandcoolvalidator",
                "BAND_EXTERNAL_ID": "2",
                "BAND_REPORTER": "bandcoolreporter",
                "BAND_SIGNATURE": "coolsignature",
            })
        self.assertFalse(is_valid)
        self.assertEqual(result, { "error": "There are missing required headers" })

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
                "BAND_CHAIN_ID": "bandchain",
                "BAND_VALIDATOR": "bandcoolvalidator",
                "BAND_REQUEST_ID": "4285",
                "BAND_EXTERNAL_ID": "2",
                "BAND_REPORTER": "bandcoolreporter",
                "BAND_SIGNATURE": "coolsignature",
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
                "BAND_CHAIN_ID": "bandchain",
                "BAND_VALIDATOR": "bandcoolvalidator",
                "BAND_REQUEST_ID": "4285",
                "BAND_EXTERNAL_ID": "2",
                "BAND_REPORTER": "bandcoolreporter",
                "BAND_SIGNATURE": "coolsignature",
            })
        self.assertFalse(is_valid)
        self.assertEqual(result, { "error": "testexception" })
