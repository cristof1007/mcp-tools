#!/usr/bin/env python3
"""
MCP Translation Server - Spanish to English

A Model Context Protocol server that provides Spanish-to-English translation
powered by Ollama, a local language model runtime.

Configuration via environment variables:
- MCP_MODEL_NAME: Model name (default: "llama3")
- MCP_API_URL: Ollama API endpoint (default: "http://localhost:11434")
"""

import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP

from .utils.config import Config
from .utils.ollama_backend import OllamaBackend
from .tools.traslation_service import TranslationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration once at module level
config = Config()
logger.info(f"Configuration: {config}")

# Initialize backend and service
backend = OllamaBackend(config.api_url)
service = TranslationService(backend, config.model_name)

# Create MCP server as a global for mcp dev
app = FastMCP("translation-server")

# Auto-register tools from all services
service.register_tools(app)


async def main():
    """Run the MCP server."""
    logger.info("MCP Server started. Listening for connections...")
    app.run()


if __name__ == "__main__":
    app.run()
