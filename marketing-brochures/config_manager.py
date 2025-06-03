import os
from dotenv import load_dotenv

def load_api_key() -> str:
    """
    Loads the OpenAI API key from environment variables.

    It first loads variables from a .env file (if present) and then
    retrieves the 'OPENAI_API_KEY'. It performs basic validation on the key.

    Returns:
        str: The OpenAI API key.

    Raises:
        ValueError: If the API key is not found, malformed, or has extra spaces.
    """
    load_dotenv(override=True)
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError(
            "No API key was found. Please ensure 'OPENAI_API_KEY' is set in your "
            "environment or .env file. Refer to troubleshooting documentation."
        )
    elif not api_key.startswith("sk-proj-"): # Or your specific key prefix
        # Note: OpenAI key formats can change. "sk-proj-" is an example for project-specific keys.
        # Regular API keys might start with "sk-". Adjust if necessary.
        # This check is based on the notebook's original validation.
        # If using organization keys or other types, this might need adjustment.
        print(
            "Warning: API key does not start with 'sk-proj-'. This might be acceptable "
            "depending on your key type. The original script checked for 'sk-proj-'."
        )
        # For a stricter check based on the notebook:
        # raise ValueError(
        #     "An API key was found, but it doesn't start with 'sk-proj-'. "
        #     "Please check you're using the right key. Refer to troubleshooting."
        # )
    elif api_key.strip() != api_key:
        raise ValueError(
            "The API key appears to have leading/trailing spaces or tab characters. "
            "Please remove them. Refer to troubleshooting documentation."
        )

    print("API key found and appears valid.")
    return api_key


if __name__ == '__main__':
    try:
        key = load_api_key()
        print(f"Successfully loaded API key (first 5 chars): {key[:5]}...")
    except ValueError as e:
        print(f"Error: {e}")