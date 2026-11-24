# Security and retirement notes

This backend is a retired prototype, not the live Hallo Batam AI API. Do not expose it to public traffic.

## Changes in this cleanup

- Removed the tracked Django secret fallback; require a fresh environment secret.
- Default debug off, reject wildcard hosts, restrict CORS to an explicit list.
- Require a separate bearer token for chat; signed session handles expire after 24 hours and are refreshed on successful requests. Old unsigned IDs are intentionally incompatible.
- Bound input, use JSON-only parsing and local IP throttling; provider clients are lazy, calls have timeouts, and raw provider errors are not returned.
- Use a single embedding configuration; the ingestion command no longer deletes an index.

## Remaining risks and operational limits

The previous fallback secret remains in Git history. Treat it as disclosed, rotate it wherever used, invalidate affected sessions, and scan all branches/history before archiving. This PR does not rewrite history or rotate external credentials. API provider keys are read from environment; do not publish them.

The shared token is for trusted local/server clients, not user-level authentication. Do not embed it in public JavaScript. IP throttling and session state are in a single-process local cache; they are not durable, distributed or suitable for public production. Configure trusted proxies and a shared limiter/cache before any new deployment. TLS, admin access and outbound provider data handling require separate review.

The sample corpus is historical and not verified travel advice. Retrieval failures fall back to generation without sources; prompt instructions are not a security boundary. No real-provider or embedding-model integration test is included. Dependency bounds are not a lockfile or vulnerability audit.

The live Supabase replacement remains independent of this repository.
