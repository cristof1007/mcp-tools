"""
Configuration management for MCP Translation Server.
Single Responsibility: Load and store configuration from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Application configuration from environment variables.
    
    Environment Variables:
    - MCP_MODEL_NAME: Model name in Ollama (default: "llama3")
    - MCP_API_URL: Ollama API endpoint (default: "http://localhost:11434")
    """

    def __init__(self):
        self.model_name = os.getenv("MCP_MODEL_NAME", "llama3")
        self.api_url = os.getenv("MCP_API_URL", "http://localhost:11434")
        print(f"Loaded configuration: {self}")

    def __repr__(self):
        return f"Config(model={self.model_name}, url={self.api_url})"
