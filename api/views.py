"""Restricted local/demo chat API for the retired backend."""
import secrets

from django.conf import settings
from django.core import signing
from django.core.cache import cache
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .services.conversation import (
    CACHE_TIMEOUT, LANGUAGE_INSTRUCTIONS, MAX_HISTORY_TURNS, build_prompt, session_handle,
)
from .services.providers import ProviderUnavailable, ask_ai_with_fallback
from .services.retrieval import retrieve


class ChatThrottle(SimpleRateThrottle):
    scope = "legacy_chat"

    def get_rate(self):
        return settings.CHAT_RATE

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class ChatAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]
    throttle_classes = [ChatThrottle]

    def post(self, request):
        expected = settings.CHAT_API_TOKEN
        if len(expected) < 32:
            return Response({"error": "Chat service is not configured."}, status=503)
        auth = request.headers.get("Authorization", "")
        if not secrets.compare_digest(auth.encode("utf-8"), ("Bearer " + expected).encode("utf-8")):
            return Response({"error": "Unauthorized."}, status=401,
                            headers={"WWW-Authenticate": "Bearer"})

        if not isinstance(request.data, dict):
            return Response({"error": "Expected a JSON object."}, status=400)
        message = request.data.get("message")
        language = request.data.get("language", "id")
        if not isinstance(message, str) or not message.strip() or len(message) > 2000:
            return Response({"error": "Message must contain 1–2000 characters."}, status=400)
        if not isinstance(language, str) or language not in LANGUAGE_INSTRUCTIONS:
            return Response({"error": "Language must be id or en."}, status=400)
        try:
            session_id, token = session_handle(request.data.get("session_id"))
        except (signing.BadSignature, ValueError, TypeError):
            return Response({"error": "Invalid or expired session."}, status=400)

        key = f"chat_history_{session_id}"
        history = cache.get(key, [])
        message = message.strip()
        context, sources = retrieve(message)
        prompt = build_prompt(message, language, history, context)
        try:
            answer, provider = ask_ai_with_fallback(prompt)
        except ProviderUnavailable:
            return Response({"error": "AI service temporarily unavailable."}, status=503)

        cache.set(key, (history + [{"user": message, "ai": answer}])[-MAX_HISTORY_TURNS:],
                  CACHE_TIMEOUT)
        return Response({"response": answer, "provider_used": provider, "language": language,
                         "sources": sources, "session_id": token},
                        headers={"Cache-Control": "no-store"})
