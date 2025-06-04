import os
from dotenv import load_dotenv

class ConfigManager:
    """
    Manages configuration settings, primarily loading API keys from environment variables.
    """
    def __init__(self):
        """
        Initializes the ConfigManager by loading environment variables and retrieving the OpenAI API key.
        """
        load_dotenv(override=True)
        self.openai_api_key = self._get_openai_api_key()

    def _get_openai_api_key(self) -> str:
        """
        Retrieves the OpenAI API key from environment variables.

        Returns:
            str: The OpenAI API key.

        Raises:
            ValueError: If the API key is not found or is in an invalid format.
        """
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")

        # Basic validation for OpenAI API key format
        if not (api_key.startswith('sk-proj-') and len(api_key) > 10):
            print("Warning: OPENAI_API_KEY format looks unusual. Please double-check your key in the .env file.")

        return api_key

# Example usage (for testing this module directly)
if __name__ == "__main__":
    try:
        config = ConfigManager()
        print(f"OpenAI API Key loaded successfully (first 5 chars): {config.openai_api_key[:5]}...")
    except ValueError as e:
        print(f"Configuration Error: {e}")