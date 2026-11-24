from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from api.services.providers import ProviderUnavailable, ask_ai_with_fallback

TOKEN = "test-only-" + "a" * 40


@override_settings(CHAT_API_TOKEN=TOKEN, CHAT_RATE="100/min", ALLOWED_HOSTS=["testserver"])
class ChatTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + TOKEN)

    def post(self, payload):
        return self.client.post("/api/chat/", payload, format="json")

    def test_missing_auth(self):
        self.client.credentials()
        self.assertEqual(self.post({"message": "hello"}).status_code, 401)

    @override_settings(CHAT_API_TOKEN="")
    def test_unconfigured_auth_fails_closed(self):
        self.assertEqual(self.post({"message": "hello"}).status_code, 503)

    def test_invalid_payloads(self):
        for payload in ({"message": ""}, {"message": 42}, {"message": "x" * 2001},
                        {"message": "hi", "language": "fr"},
                        {"message": "hi", "language": []}, ["hi"]):
            with self.subTest(payload=payload):
                self.assertEqual(self.post(payload).status_code, 400)

    def test_tampered_session(self):
        self.assertEqual(self.post({"message": "hi", "session_id": "forged"}).status_code, 400)

    @patch("api.views.retrieve", return_value=("sample", ["data_wisata/info_wisata.txt"]))
    @patch("api.views.ask_ai_with_fallback", return_value=("Sample answer", "Gemini"))
    def test_answer_and_signed_session_history(self, provider, retrieval):
        first = self.post({"message": "first", "language": "en"})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.data["sources"], ["data_wisata/info_wisata.txt"])
        self.assertEqual(first["Cache-Control"], "no-store")
        second = self.post({"message": "second", "session_id": first.data["session_id"]})
        self.assertEqual(second.status_code, 200)
        self.assertIn("first", provider.call_args.args[0])
        self.assertIn("Sample answer", provider.call_args.args[0])

    @patch("api.views.retrieve", return_value=("", []))
    @patch("api.views.ask_ai_with_fallback", side_effect=ProviderUnavailable("private details"))
    def test_provider_failure_is_sanitized(self, provider, retrieval):
        response = self.post({"message": "hi"})
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("private details", str(response.data))

    @override_settings(CHAT_RATE="1/min")
    @patch("api.views.retrieve", return_value=("", []))
    @patch("api.views.ask_ai_with_fallback", return_value=("ok", "Gemini"))
    def test_rate_limit(self, provider, retrieval):
        self.assertEqual(self.post({"message": "hi"}).status_code, 200)
        self.assertEqual(self.post({"message": "hi"}).status_code, 429)


class ProviderTests(TestCase):
    @override_settings(GROQ_API_KEY_1="test", GROQ_API_KEY_2="", GEMINI_API_KEY="test")
    @patch("api.services.providers.ask_groq", side_effect=RuntimeError("private"))
    @patch("api.services.providers.ask_gemini", return_value="fallback")
    def test_fallback_skips_missing_key(self, gemini, groq):
        self.assertEqual(ask_ai_with_fallback("prompt"), ("fallback", "Gemini"))
        self.assertEqual(groq.call_count, 1)

    @override_settings(GROQ_API_KEY_1="", GROQ_API_KEY_2="", GEMINI_API_KEY="")
    def test_no_provider(self):
        with self.assertRaises(ProviderUnavailable):
            ask_ai_with_fallback("prompt")
