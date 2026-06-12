"""
Translation service - orchestrates translation logic.
Single Responsibility: Business logic for translation requests.
"""

import logging

from ..utils.ollama_backend import OllamaBackend

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Orchestrates translation logic.
    
    Responsibilities:
    - Input validation
    - Model resolution (default or override)
    - Response formatting
    
    Dependencies: OllamaBackend (injected)
    """

    SYSTEM_PROMPT = (
        # "You are a professional translator specializing in Spanish to English translation. "
        "Translate the following Spanish text to English. "
        "Respond with ONLY the English translation, no explanations or additional text."
    )

    def __init__(self, backend: OllamaBackend, default_model: str):
        """
        Initialize translation service.

        Args:
            backend (OllamaBackend): Backend instance for API calls
            default_model (str): Default model name
        """
        self.backend = backend
        self.default_model = default_model
        logger.info("TranslationService initialized | model=%s", default_model)

    async def translate(
        self,
        text: str,
    ) -> dict:
        """
        Translate Spanish text to English.

        Args:
            text (str): Spanish text to translate

        Returns:
            dict: Translation result with 'translation' and 'model' keys

        Raises:
            ValueError: If input is invalid
            RuntimeError: If translation fails
        """
        logger.debug("translate() called | text=%r", text)

        # Validate input
        if not text or not text.strip():
            logger.warning("translate() rejected: empty input")
            raise ValueError("Input text cannot be empty")

        text = text.strip()
        model = self.default_model

        logger.info("Translating | model=%s | text=%r", model, text[:120])

        # Translate via backend
        try:
            translation = await self.backend.generate(text, model, self.SYSTEM_PROMPT)
        except Exception as exc:
            logger.error("Translation failed | model=%s | error=%s", model, exc)
            raise

        logger.info("Translation OK | model=%s | result=%r", model, translation[:120])

        return {
            "translation": translation,
            "model": model,
        }

    def register_tools(self, app) -> None:
        """Register all tools provided by this service with the MCP app."""

        logger.info("Registering tool: translate_spanish_to_english")

        @app.tool()
        async def translate_spanish_to_english(text: str) -> dict:
            """
            Translate Spanish text to English using Ollama.

            Args:
                text (str): The Spanish text to translate

            Returns:
                dict: Translation result with 'translation' and 'model' keys
            """
            logger.info("[MCP] Tool invoked: translate_spanish_to_english | text=%r", text[:120] if text else text)
            result = await self.translate(text)
            logger.info("[MCP] Tool response: translate_spanish_to_english | translation=%r", result.get("translation", "")[:120])
            return result
