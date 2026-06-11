#!/usr/bin/env python3
"""
Entry point for MCP Translation Server.

This script runs the translation server. Can be invoked as:
  python server.py
  or
  .venv\Scripts\python server.py
  or
  mcp dev server.py
"""

from src.server import app

if __name__ == "__main__":
    app.run()
