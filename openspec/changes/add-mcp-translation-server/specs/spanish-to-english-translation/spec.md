## Implementation Status

✅ **COMPLETE** — All requirements implemented and tested with `mcp dev mcpserver.py`

## ADDED Requirements

### Requirement: Translate Spanish text to English
The MCP server SHALL provide a tool that accepts Spanish-language text and returns the English translation using a local language model.

#### Scenario: Successful translation
- **WHEN** a client invokes the `translate_spanish_to_english` tool with Spanish text
- **THEN** the tool returns the English translation of that text

#### Scenario: Empty text handling
- **WHEN** a client invokes the tool with empty or whitespace-only text
- **THEN** the tool returns an error indicating that input text cannot be empty

#### Scenario: Non-Spanish text
- **WHEN** a client invokes the tool with text that is not in Spanish
- **THEN** the tool attempts translation (behavior depends on model capability); the translation may be inaccurate or untranslated if the model detects non-Spanish content

### Requirement: Parametrized model selection
The tool SHALL support selecting which local model to use for translation, with configurable defaults.

#### Scenario: Default model from environment
- **WHEN** the server starts and environment variable `MCP_MODEL_NAME` is set (e.g., "llama3" or "mistral")
- **THEN** the tool uses the specified model as the default for all translation requests

#### Scenario: Override model per request
- **WHEN** a client invokes the tool with an optional `model_name` parameter
- **THEN** the tool uses the specified model for that request, overriding the environment default

#### Scenario: Fallback to hardcoded default
- **WHEN** the server starts and no `MCP_MODEL_NAME` environment variable is set
- **THEN** the tool defaults to a predefined model name (e.g., "llama3" or equivalent)

### Requirement: Configurable backend endpoint
The tool SHALL allow configuration of the model backend endpoint (e.g., Ollama API URL).

#### Scenario: Default Ollama endpoint
- **WHEN** the server starts with no `MCP_API_URL` environment variable
- **THEN** the tool targets the default Ollama endpoint `http://localhost:11434`

#### Scenario: Custom endpoint from environment
- **WHEN** environment variable `MCP_API_URL` is set (e.g., "http://192.168.1.100:11434")
- **THEN** the tool sends translation requests to the specified endpoint

#### Scenario: Per-request endpoint override
- **WHEN** a client invokes the tool with an optional `api_url` parameter
- **THEN** the tool uses the specified endpoint for that request, overriding the environment default

### Requirement: Error handling and diagnostics
The tool SHALL gracefully handle failures and return informative error messages.

#### Scenario: Model not available
- **WHEN** the tool attempts to use a model that is not downloaded/available on the local backend
- **THEN** the tool returns an error message indicating the missing model and suggesting the user run `ollama pull <model-name>`

#### Scenario: Backend connection failure
- **WHEN** the tool attempts to connect to the model backend (e.g., Ollama) and the connection fails
- **THEN** the tool returns an error message indicating that the backend is unreachable (e.g., "Failed to connect to http://localhost:11434")

#### Scenario: Translation failure
- **WHEN** the backend responds with an error during translation
- **THEN** the tool captures the error and returns a descriptive message to the client without crashing the server

### Requirement: MCP tool exposure
The translation capability SHALL be exposed as an MCP tool that clients can invoke over the MCP protocol.

#### Scenario: Tool discovery
- **WHEN** an MCP client connects to the server and requests tool list
- **THEN** the server returns the `translate_spanish_to_english` tool with its name, description, and input schema

#### Scenario: Tool invocation
- **WHEN** an MCP client invokes the `translate_spanish_to_english` tool with required parameters
- **THEN** the server processes the request and returns the tool result (translation or error) to the client
