# MCP Translation Server

A Model Context Protocol (MCP) server that provides Spanish-to-English translation powered by Ollama.

## Features

- **Ollama-Powered**: Uses local language models via Ollama
- **Simple Configuration**: Just two environment variables
- **Clean Architecture**: SOLID principles, dependency injection
- **Error Handling**: Clear, diagnostic error messages
- **Async Processing**: Non-blocking translation requests

## Architecture

The server is modularized into clean, testable components following SOLID principles:

```
src/
├── __init__.py           # Public API exports
├── config.py             # Configuration (env vars)
├── backends.py           # Ollama API communication
├── service.py            # Translation business logic
└── server.py             # MCP server setup & tools

server.py                # Root entry point
ARCHITECTURE.md          # Detailed design documentation
```

**Each module has a single responsibility:**
- `config.py`: Loads environment variables
- `backends.py`: HTTP communication with Ollama
- `service.py`: Input validation, model resolution, response formatting
- `server.py`: MCP tool definition and server lifecycle

Dependencies are **injected**, making code testable and extensible.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design and extension patterns.

## Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Virtual environment: `.venv`

### Setup

1. **Install dependencies:**
   ```bash
   .venv\Scripts\pip install -r requirements.txt
   ```

2. **Configure (optional):**
   ```bash
   cp .env.example .env
   # Edit .env if you want different model or endpoint
   ```

3. **Start Ollama (in one terminal):**
   ```bash
   ollama serve
   ```

4. **Pull a model:**
   ```bash
   ollama pull llama3
   ```

5. **Start the MCP server (in another terminal):**
   ```bash
   .venv\Scripts\python server.py
   ```

## Configuration

Two environment variables control the server:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_MODEL_NAME` | `llama3` | Model name in Ollama |
| `MCP_API_URL` | `http://localhost:11434` | Ollama API endpoint |

### Examples

**Default setup:**
```bash
.venv\Scripts\python server.py
```
Uses llama3 on localhost:11434

**Custom model:**
```bash
set MCP_MODEL_NAME=mistral
.venv\Scripts\python server.py
```

**Remote Ollama:**
```bash
set MCP_API_URL=http://192.168.1.100:11434
.venv\Scripts\python server.py
```

## Usage

### Tool Signature

```
translate_spanish_to_english(
    text: str,                      # Spanish text to translate
    model_name: str | None          # Optional: override default model
) -> {
    "translation": str,             # English translation
    "model": str                    # Model used
}
```

### Example: With MCP Inspector

1. Start the server (as above)
2. In another terminal:
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```
3. In the Inspector UI:
   - Go to **Tools**
   - Click `translate_spanish_to_english`
   - Enter Spanish text
   - Run

### Example Requests

**Basic translation:**
```json
{
  "text": "Hola, ¿cómo estás?"
}
```
Response:
```json
{
  "translation": "Hello, how are you?",
  "model": "llama3"
}
```

**Override model per request:**
```json
{
  "text": "Buenas noches",
  "model_name": "mistral"
}
```

## Supported Models

Any model available via `ollama pull`:

- `llama3` - High quality, larger (~4GB)
- `mistral` - Balanced speed/quality (~4GB)
- `neural-chat` - Lightweight (~3GB)
- `qwen2:7b` - Fast, good quality
- And many others from [Ollama library](https://ollama.ai/library)

## Troubleshooting

### "Failed to connect to Ollama at http://localhost:11434"

**Problem**: Ollama is not running

**Solution**:
```bash
# Install Ollama from https://ollama.ai
# Then start it:
ollama serve
```

### "Model 'llama3' not found in Ollama"

**Problem**: Model hasn't been downloaded

**Solution**:
```bash
ollama pull llama3
```

### "Input text cannot be empty"

**Problem**: Text parameter is empty or whitespace

**Solution**: Provide non-empty text

## Code Structure

```
server.py
├── Config class
│   └── Loads MCP_MODEL_NAME, MCP_API_URL
├── OllamaBackend class
│   └── async generate(text, model)
├── TranslationService class
│   └── async translate(text, model_override)
└── MCP tool: translate_spanish_to_english()
```

**Adding features:**

1. Modify `OllamaBackend.generate()` for different API calls
2. Modify `TranslationService.translate()` for business logic
3. Add new `@mcp.tool()` functions as needed

## Development

### Syntax check:
```bash
.venv\Scripts\python -m py_compile server.py
```

### Test server startup:
```bash
.venv\Scripts\python server.py &
# Should log: "MCP Translation Server started. Listening for connections..."
```

## Performance

- **Startup**: ~1 second (Ollama connection check)
- **Translation**: 1-30 seconds (depends on model size and hardware)
  - llama3 on GPU: ~2 seconds
  - llama3 on CPU: ~10 seconds
  - mistral on GPU: ~1 second

## Contributing

Use OpenSpec for changes:

```bash
openspec new change "feature-name"
openspec status --change "feature-name"
openspec apply --change "feature-name"
```

## License

(Add license here)

