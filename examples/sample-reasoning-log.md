# Reasoning log: Replace in-process cache with Redis

- **Task ID / link:** CALYX-12
- **Owner(s):** Alex
- **Date started:** 2026-04-28
- **Tags:** `platform`, `reliability`, `reasoning-log`

## Context

Single-node cache causes sticky sessions and stale reads after deploys. We need a shared cache for session flags across API replicas.

## Thought stream

- 2026-04-28 — Considered Memcached vs Redis; ops already runs Redis for queues.
- 2026-04-29 — Worried about latency vs in-memory; need bounded timeouts and circuit breaker.
- 2026-04-29 — **Dead end:** “Just use DB” — load on hot path too high; rejected for v1.

## Options considered

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Redis (managed) | Existing skill, TTL support | Cost, network hop | **Chosen** |
| Memcached | Simple | Second system, no structure | Rejected |
| In-process only | Fast | Wrong for multi-replica | Rejected |

## 10th Man / pre-mortem pointer

See `pre-mortem-redis-cache.md` (summary: failover story, key explosion, auth on Redis).

## Outcome

Implement Redis with 50ms timeout, fallback to “no cache” (degraded, not wrong). Keys prefixed by service name.

## Artifacts

- ADR (if any): `decisions/ADR-0003-redis-session-cache.md`
- PRs / tickets: PR 441, OPS-88
