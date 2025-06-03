from web_scraper import Website
from prompt_generator import (
    get_default_system_prompt,
    create_user_prompt_for_website,
    format_messages_for_llm
)
from llm_handler import get_llm_chat_completion, initialize_openai_client

def summarize_website(url: str, model: str = "gpt-4o-mini") -> str | None:
    """
    Orchestrates the process of scraping a website and generating its summary using an LLM.

    Args:
        url (str): The URL of the website to summarize.
        model (str, optional): The LLM model to use for summarization.
                               Defaults to "gpt-4o-mini".

    Returns:
        str | None: The generated summary in markdown format, or None if an error occurs
                    or the website content cannot be processed.
    """
    print(f"Starting summarization for URL: {url}")

    try:
        # Ensure OpenAI client is ready before potentially lengthy scraping
        initialize_openai_client()
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}. Aborting summarization.")
        return None

    try:
        print("Step 1: Scraping website...")
        website = Website(url)
        if not website.text or "Error fetching URL" in website.text:
            print(f"Could not retrieve or parse content from {url}. Check website.text.")
            return f"## Error\nCould not retrieve or parse content from {url}.\nDetails: {website.text}"
        print(f"Website scraping successful. Title: {website.title}")

        print("Step 2: Generating prompts...")
        system_prompt = get_default_system_prompt()
        user_prompt = create_user_prompt_for_website(website)
        messages = format_messages_for_llm(system_prompt, user_prompt)
        # print(f"User prompt for LLM (first 200 chars): {user_prompt[:200]}...") # For debugging

        print("Step 3: Calling LLM for summarization...")
        summary = get_llm_chat_completion(messages, model=model)

        if summary:
            print("Summarization successful.")
        else:
            print("Failed to get summary from LLM.")
            return "## Error\nFailed to generate summary from the LLM."

        return summary

    except requests.exceptions.RequestException as e: # from web_scraper potential raise
        print(f"Failed to scrape website {url}: {e}")
        return f"## Error\nFailed to scrape website {url}.\nDetails: {e}"
    except Exception as e:
        print(f"An unexpected error occurred in summarize_website: {e}")
        return f"## Error\nAn unexpected error occurred during summarization.\nDetails: {e}"

if __name__ == '__main__':
    # Example usage (requires .env file with OPENAI_API_KEY):
    # Test with a known accessible URL
    test_urls = [
        "https://www.djangoproject.com/", # Usually scrape-friendly
        "https://edwarddonner.com", # Used in the notebook
        # "https://www.python.org/" # Another example
    ]

    for url_to_test in test_urls:
        print(f"\n--- Summarizing: {url_to_test} ---")
        generated_summary = summarize_website(url_to_test)
        if generated_summary:
            print("\n--- Generated Summary ---")
            print(generated_summary)
        else:
            print("\nNo summary was generated.")
        print("-------------------------------\n")

    # Test with a potentially problematic URL (e.g., one that might block simple scrapers)
    # problematic_url = "https://openai.com" # As mentioned in the notebook
    # print(f"\n--- Summarizing (potentially problematic): {problematic_url} ---")
    # problematic_summary = summarize_website(problematic_url)
    # if problematic_summary:
    #     print("\n--- Generated Summary (Problematic URL) ---")
    #     print(problematic_summary)
    # else:
    #     print("\nNo summary was generated for the problematic URL.")
    # print("-------------------------------\n")