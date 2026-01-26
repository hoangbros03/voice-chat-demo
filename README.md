# voice-chat-demo

A small demo project exploring voice-driven agents, real-time streams, and vector search.

## Overview

This repository contains multiple services used in the demo:

- `services/fastrtc_core` — real-time audio/video handling, agent graph, and stream handlers.
- `services/mcp_server` — MCP signaling/server component used by clients and core services.
- `services/vector_search` — semantic vector search (Superlinked) for National Olympic Committee (NOC) statistics.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
pip install uv
uv venv .venv
. .\.venv\Scripts\Activate
```

2. Install repository packages and dependencies:

```powershell
uv sync
```

3. Configure required environment variables by copy .env.dev then add env:

```powershell
cp .env.dev .env
```

4. Run a service (from repo root or change into the service folder):

```powershell
# MCP server
cd services\mcp_server && uv run python main.py

# Vector search (see services/vector_search/README.md for details)
cd services\vector_search && uv run python main.py

# Real-time core
cd services\fastrtc_core && uv run python -m test.test_service # To run gradio that we can start talking directly 
cd services\fastrtc_core && uv run main.py # or if you have a way to connect to this webrtc server
```

## Tests

Run tests from the repository root:

```powershell
pytest -q
```

## Notes & troubleshooting

- If you see errors like `Unindexed fields with filter found`, ensure fields used in `.filter()` are registered as filterable index fields in the corresponding `sl.Index` (see `services/vector_search/indexes/noc_index.py`).
- Check service-specific READMEs for more details (for example, `services/vector_search/README.md`).

