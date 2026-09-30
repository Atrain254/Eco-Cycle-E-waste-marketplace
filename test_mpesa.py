import base64
import os
import unittest
from unittest.mock import Mock, patch

from ecocycle.mpesa_utlis import initiate_stk_push


class MpesaPaymentTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "MPESA_CONSUMER_KEY": "test-consumer-key",
            "MPESA_CONSUMER_SECRET": "test-consumer-secret",
            "MPESA_SHORTCODE": "174379",
            "MPESA_PASSKEY": "test-passkey",
            "MPESA_CALLBACK_URL": "https://example.com/mpesa/callback/",
        },
        clear=False,
    )
    @patch("ecocycle.mpesa_utlis.requests.post")
    @patch("ecocycle.mpesa_utlis.requests.get")
    def test_initiate_stk_push_builds_expected_request(
        self, mock_get, mock_post
    ):
        token_response = Mock()
        token_response.json.return_value = {"access_token": "test-access-token"}
        mock_get.return_value = token_response

        stk_response = Mock()
        stk_response.json.return_value = {
            "ResponseCode": "0",
            "CheckoutRequestID": "ws_CO_test_123",
        }
        mock_post.return_value = stk_response

        result = initiate_stk_push("254712345678", 150, "ECO-ITEM-1")

        mock_get.assert_called_once_with(
            "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
            auth=("test-consumer-key", "test-consumer-secret"),
        )

        mock_post.assert_called_once()
        request_args, request_kwargs = mock_post.call_args
        self.assertEqual(
            request_args[0],
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        )
        self.assertEqual(
            request_kwargs["headers"],
            {
                "Authorization": "Bearer test-access-token",
                "Content-Type": "application/json",
            },
        )

        payload = request_kwargs["json"]
        self.assertEqual(payload["BusinessShortCode"], "174379")
        self.assertEqual(payload["Amount"], 150)
        self.assertEqual(payload["PartyA"], "254712345678")
        self.assertEqual(payload["PhoneNumber"], "254712345678")
        self.assertEqual(payload["AccountReference"], "ECO-ITEM-1")
        self.assertEqual(payload["CallBackURL"], "https://example.com/mpesa/callback/")

        decoded_password = base64.b64decode(payload["Password"]).decode()
        self.assertTrue(decoded_password.startswith("174379test-passkey"))
        self.assertEqual(result, stk_response.json.return_value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
