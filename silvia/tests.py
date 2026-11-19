
from unittest.mock import patch

from rest_framework.test import APISimpleTestCase
from rest_framework import status


class SilviaHealthTests(APISimpleTestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ok"})


class SilviaChatTests(APISimpleTestCase):
    def test_valid_chat_request(self):
        response = self.client.post(
            "/api/chat",
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["assistant"], "Silvia")
        self.assertIn("reply", response.data)

    def test_missing_message_is_rejected(self):
        response = self.client.post(
            "/api/chat",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_message_is_rejected(self):
        response = self.client.post(
            "/api/chat",
            {"message": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_message_exceeding_limit_is_rejected(self):
        response = self.client.post(
            "/api/chat",
            {"message": "A" * 1001},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unexpected_fields_are_rejected(self):
        response = self.client.post(
            "/api/chat",
            {"message": "Hello", "admin": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_malformed_json_is_rejected(self):
        response = self.client.generic(
            "POST",
            "/api/chat",
            data='{"message":',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_json_keys_are_rejected(self):
        response = self.client.generic(
            "POST",
            "/api/chat",
            data='{"message":"Hello","message":"Override"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_json_array_is_rejected(self):
        response = self.client.generic(
            "POST",
            "/api/chat",
            data='["Hello"]',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_json_string_is_rejected(self):
        response = self.client.generic(
            "POST",
            "/api/chat",
            data='"Hello"',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_json_number_is_rejected(self):
        response = self.client.generic(
            "POST",
            "/api/chat",
            data='123',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "silvia.views.answer",
        side_effect=RuntimeError("Internal failure"),
    )
    def test_chat_internal_error_is_handled(self, mock_answer):
        response = self.client.post(
            "/api/chat",
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        self.assertEqual(
            response.data,
            {"error": "internal_server_error"},
        )
