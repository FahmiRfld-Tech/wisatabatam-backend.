"""Lazy provider clients and sanitized fallback."""
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class ProviderUnavailable(Exception):
    pass


def ask_groq(key, prompt):
    from openai import OpenAI

    with OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1",
                timeout=15.0, max_retries=0) as client:
        result = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    return result.choices[0].message.content


def ask_gemini(key, prompt):
    from google import genai
    from google.genai import types

    with genai.Client(api_key=key, http_options=types.HttpOptions(timeout=15000)) as client:
        result = client.models.generate_content(model=settings.GEMINI_MODEL, contents=prompt)
    return result.text


def ask_ai_with_fallback(prompt):
    attempts = (
        ("Groq (primary)", settings.GROQ_API_KEY_1, ask_groq),
        ("Groq (secondary)", settings.GROQ_API_KEY_2, ask_groq),
        ("Gemini", settings.GEMINI_API_KEY, ask_gemini),
    )
    for name, key, call in attempts:
        if not key:
            continue
        try:
            answer = call(key, prompt)
            if isinstance(answer, str) and answer.strip():
                return answer.strip()[:8000], name
        except Exception as exc:
            # Never log credentials, prompts, raw provider errors or user data.
            logger.warning("Provider %s failed (%s)", name, type(exc).__name__)
    raise ProviderUnavailable("No configured provider returned an answer.")
