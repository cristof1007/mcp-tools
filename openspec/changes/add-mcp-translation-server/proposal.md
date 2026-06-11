## Why

The project needs an MCP (Model Context Protocol) server that enables programmatic text translation from Spanish to English using a local language model. This foundation allows AI systems and client applications to integrate translation capabilities without external API dependencies, providing cost savings, privacy, and control over model selection.

## What Changes

- **MCP Server Architecture**: `mcpserver.py` (entry point) → `src/server.py` (orchestrator) → modular services in `src/tools/` and `src/utils/`
- **Translation Tool**: `translate_spanish_to_english` with required `text` param and optional `model_name`/`api_url` overrides
- **Configuration**: Environment variables (`MCP_MODEL_NAME`, `MCP_API_URL`) + `.env` file support via `python-dotenv`
- **Backend**: Ollama HTTP API for model execution
- **Service Registration**: Auto-registration pattern via `register_tools(app)` method

## Capabilities

### New Capabilities
- `translate_spanish_to_english`: Tool that accepts Spanish text and returns English translation using Ollama
  - **Required**: `text` (string) — Spanish text to translate
  - **Optional**: `model_name` (string) — Override default model (e.g., "llama3", "mistral")
  - **Optional**: `api_url` (string) — Override default Ollama endpoint
  - **Returns**: `{"translation": string, "model": string}`

### Modified Capabilities
None — this is a new feature.

## Impact

- **Code Structure**: `src/` organized as `src/utils/` (config, backends) + `src/tools/` (services)
- **Dependencies**: `mcp[cli]`, `fastmcp`, `httpx`, `python-dotenv`, `ollama` (optional)
- **Operations**: Run with `mcp dev mcpserver.py`; requires Ollama daemon running
- **Interfaces**: MCP protocol over stdio; clients discover and call the translation tool
