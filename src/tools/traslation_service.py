"""
Translation service - orchestrates translation logic.
Single Responsibility: Business logic for translation requests.
"""

from ..utils.ollama_backend import OllamaBackend


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
        # Validate input
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        text = text.strip()
        model = self.default_model

        # Translate via backend
        translation = await self.backend.generate(text, model, self.SYSTEM_PROMPT)

        return {
            "translation": translation,
            "model": model,
        }

    def register_tools(self, app) -> None:
        """Register all tools provided by this service with the MCP app."""

        @app.tool()
        async def translate_spanish_to_english(text: str) -> dict:
            """
            Translate Spanish text to English using Ollama.

            Args:
                text (str): The Spanish text to translate

            Returns:
                dict: Translation result with 'translation' and 'model' keys
            """
            return await self.translate(text)
