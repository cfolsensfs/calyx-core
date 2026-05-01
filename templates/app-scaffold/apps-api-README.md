# API (`apps/api`)

HTTP API: auth, domain logic, persistence, calls to LLM/MCP as needed.

**Contracts:** Owns database access and server-side secrets. Expose only what `apps/web` (and MCP tools, if any) require.
