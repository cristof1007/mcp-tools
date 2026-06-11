## Context

The `mcp-tools` project implements an MCP (Model Context Protocol) server for Spanish-to-English translation using local models via Ollama. The implementation is complete with a modular architecture: `src/utils/` contains configuration and backends, `src/tools/` contains service implementations, and `src/server.py` acts as the orchestrator.

## Implemented Architecture

```
mcpserver.py (entry point)
  └─ src/server.py (FastMCP orchestrator)
      ├─ Config (loads .env variables)
      ├─ OllamaBackend (HTTP communication)
      └─ TranslationService (business logic + tool registration)
          └─ translate_spanish_to_english tool
```

## Key Implementation Details

### 1. Backend Strategy: Ollama HTTP API
- Single backend: Ollama HTTP API (no transformers fallback needed currently)
- Rationale: Lightweight, parametrizable, supports model switching without code changes
- Configuration: `MCP_API_URL` (default: `http://localhost:11434`)

### 2. Tool Parameters
- **Required**: `text` (Spanish text to translate)
- **Optional**: `model_name` (override default from `MCP_MODEL_NAME` env var)
- **Optional**: `api_url` (override default from `MCP_API_URL` env var)
- Enables per-request parametrization while maintaining sensible defaults

### 3. Configuration: Environment Variables + .env Support
- `MCP_MODEL_NAME`: Model to use (default: "llama3")
- `MCP_API_URL`: Ollama endpoint (default: "http://localhost:11434")
- Loaded via `python-dotenv` for `.env` file support

### 4. Service Registration Pattern
- Each service implements `register_tools(app)` method
- Server calls `service.register_tools(app)` to auto-register tools
- Enables scalability: add new services without modifying server entry point
- Falls back to sensible defaults (ollama, `http://localhost:11434`)

### 4. Error Handling: Graceful failures with informative messages
**Decision**: Catch connection/model errors and return structured error messages to the client instead of crashing.

**Rationale**:
- MCP clients expect tool errors to be captured and reported, not server crashes
- Users need diagnostic info (e.g., "Ollama not reachable at localhost:11434")

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Ollama dependency**: Users must run Ollama daemon separately | Provide clear documentation; offer transformers fallback for offline users |
| **Model availability**: Selected model may not be downloaded/installed locally | Tool error message clearly indicates missing model; user can run `ollama pull <model>` |
| **Performance variance**: Translation time depends on model size and hardware | Document expected latencies for common models; no promises in tool description |
| **Network latency to Ollama**: If Ollama is remote, HTTP calls may be slow | Default is localhost; users can configure endpoint; async tool prevents blocking |

## Migration Plan

1. Implement `server.py` with FastMCP scaffold and translation tool
2. Test locally with MCP Inspector using Ollama (if available) or transformers
3. Document setup instructions (installing Ollama, pulling models, running server)
4. Users can run: `python server.py` to start the MCP server

No rollback needed; this is a new service.

## Open Questions

- Should we include a built-in lightweight model (e.g., `Helsinki-NLP/opus-mt-es-en`) in requirements.txt or keep transformers as optional?
- Should the tool support batch translation (multiple texts at once) for future extensibility?
- Do we need structured logging or just stderr output?
