from openai import OpenAI, OpenAIError
from config_manager import load_api_key # Assumes config_manager.py is in the same directory

# Global OpenAI client instance
_openai_client = None

def initialize_openai_client() -> OpenAI:
    """
    Initializes and returns a global OpenAI client instance using the API key
    from environment variables.

    If the client is already initialized, it returns the existing instance.

    Returns:
        OpenAI: The initialized OpenAI client.

    Raises:
        ValueError: If the API key cannot be loaded.
        OpenAIError: If there's an issue initializing the client with OpenAI.
    """
    global _openai_client
    if _openai_client is None:
        try:
            api_key = load_api_key()
            _openai_client = OpenAI(api_key=api_key)
            print("OpenAI client initialized successfully.")
        except ValueError as ve:
            print(f"Error loading API key: {ve}")
            raise
        except OpenAIError as oe:
            print(f"Error initializing OpenAI client: {oe}")
            raise
    return _openai_client

def get_llm_chat_completion(
    messages: list[dict[str, str]],
    model: str = "gpt-4o-mini",  # Default model from the notebook
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> str | None:
    """
    Sends a chat completion request to the OpenAI API.

    Args:
        messages (list[dict[str, str]]): A list of message objects,
            typically including system and user roles.
        model (str, optional): The model to use for the completion.
            Defaults to "gpt-4o-mini".
        temperature (float, optional): Controls randomness. Lower is more deterministic.
            Defaults to 0.7.
        max_tokens (int, optional): The maximum number of tokens to generate.
            Defaults to 1000.

    Returns:
        str | None: The content of the LLM's response, or None if an error occurs.
    """
    try:
        client = initialize_openai_client() # Ensure client is initialized
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            print("Warning: No response content received from LLM.")
            return None
    except OpenAIError as e:
        print(f"An API error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during LLM call: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    print("Attempting to initialize OpenAI client and make a test call...")
    try:
        # This will implicitly initialize the client if not already done
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2 + 2?"}
        ]
        response_content = get_llm_chat_completion(test_messages)
        if response_content:
            print("\n--- LLM Test Response ---")
            print(response_content)
        else:
            print("\nFailed to get a response from LLM for the test.")

        # Second call to show client is reused
        # test_messages_2 = [
        #     {"role": "system", "content": "You are a poetic assistant."},
        #     {"role": "user", "content": "Describe a sunset."}
        # ]
        # response_content_2 = get_llm_chat_completion(test_messages_2, max_tokens=50)
        # if response_content_2:
        #     print("\n--- LLM Poetic Response ---")
        #     print(response_content_2)
        # else:
        #     print("\nFailed to get a poetic response from LLM.")

    except ValueError:
        print("Failed to run example due to API key configuration issue.")
    except OpenAIError:
        print("Failed to run example due to OpenAI API issue.")
    except Exception as e:
        print(f"An unexpected error occurred in the example: {e}")