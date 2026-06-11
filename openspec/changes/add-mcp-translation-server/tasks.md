## 1. Setup and Dependencies

- [x] 1.1 Review and finalize `requirements.txt` (confirm `fastmcp`, `httpx`, `python-dotenv`, `mcp[cli]`)
- [x] 1.2 Create `.env.example` file documenting environment variables: `MCP_MODEL_NAME`, `MCP_API_URL`
- [x] 1.3 Install `python-dotenv` for `.env` file support

## 2. Project Structure

- [x] 2.1 Reorganize code: `src/utils/` (config, ollama_backend) + `src/tools/` (traslation_service)
- [x] 2.2 Create `mcpserver.py` entry point in project root
- [x] 2.3 Implement service auto-registration pattern via `register_tools(app)` method

## 3. Configuration and Environment Loading

- [x] 3.1 Implement `Config` class to load `MCP_MODEL_NAME`, `MCP_API_URL` from `.env`
- [x] 3.2 Set sensible defaults: model="llama3", api_url="http://localhost:11434"
- [x] 3.3 Support runtime overrides via optional tool parameters

## 4. Ollama Backend Implementation

- [x] 4.1 Implement `OllamaBackend` HTTP client using `httpx` AsyncClient
- [x] 4.2 Reuse persistent `httpx.AsyncClient` for connection pooling
- [x] 4.3 Implement prompt engineering: craft system prompt for Spanish→English translation
- [x] 4.4 Add error handling: connection failures, model not found, translation errors
- [x] 4.5 Support per-request `api_url` override in `generate()` method

## 5. Tool Implementation

- [x] 5.1 Implement `TranslationService` with business logic and async translation method
- [x] 5.2 Add input validation: reject empty or None text
- [x] 5.3 Implement error handling: gracefully catch and return user-friendly error messages
- [x] 5.4 Implement tool registration: `translate_spanish_to_english(text, model_name=\"\", api_url=\"\")`
- [x] 5.5 Support per-request parameter overrides for model and API endpoint
- [x] 5.6 Return structured response: `{\"translation\": ..., \"model\": ...}`

## 6. Testing with MCP Inspector

- [x] 6.1 Start the server: `mcp dev mcpserver.py` (verify it runs without errors)
- [x] 6.2 Connect MCP Inspector and verify `translate_spanish_to_english` is discoverable
- [ ] 6.3 Test successful translation with Ollama: send sample Spanish text
- [ ] 6.4 Test error scenarios: invalid model, unreachable backend, empty text
- [ ] 6.5 Test per-request parameter overrides: model_name and api_url

## 7. Documentation

- [ ] 7.1 Create/update `README.md` with setup instructions
- [ ] 7.2 Document how to run the server and connect with MCP Inspector
- [ ] 7.3 Add examples of calling the translation tool
- [ ] 7.4 Update OpenSpec documents to reflect final implementation
- [x] 8.4 Document supported backends (Ollama, transformers) and how to switch between them

## 9. Integration and Cleanup

- [x] 9.1 Verify `server.py` follows project conventions and is production-ready
- [x] 9.2 Run any linting/formatting (if applicable to the project)
- [x] 9.3 Update `.gitignore` if needed (e.g., model cache, env files)
