"""
Ollama backend for translation.
Single Responsibility: HTTP communication with Ollama API.
"""

import httpx


class OllamaBackend:
    """
    Handles all HTTP communication with Ollama API.
    
    This class encapsulates the details of calling the Ollama API,
    including error handling and response parsing.
    """

    def __init__(self, api_url: str):
        """
        Initialize Ollama backend.

        Args:
            api_url (str): Base URL of Ollama API (e.g., http://localhost:11434)
        """
        self.api_url = api_url
        self._client = httpx.AsyncClient(timeout=60.0)

    async def generate(self, text: str, model: str, system_prompt: str = "") -> str:
        """
        Generate translation using Ollama.

        Args:
            text (str): Text to translate
            model (str): Model name in Ollama

        Returns:
            str: Generated translation

        Raises:
            RuntimeError: If connection fails or model not found
        """
        payload = {
            "model": model,
            "prompt": text,
            "system": system_prompt,
            "stream": False,
        }

        try:
            response = await self._client.post(
                f"{self.api_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()

        except httpx.ConnectError as e:
            raise RuntimeError(
                f"Failed to connect to Ollama at {self.api_url}. "
                f"Ensure Ollama is running: {e}"
            ) from e

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise RuntimeError(
                    f"Model '{model}' not found in Ollama. "
                    f"Download it with: ollama pull {model}"
                ) from e
            raise RuntimeError(f"Ollama error (HTTP {e.response.status_code}): {e.response.text}") from e

        except Exception as e:
            raise RuntimeError(f"Translation request failed: {str(e)}") from e
