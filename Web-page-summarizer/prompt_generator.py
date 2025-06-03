from web_scraper import Website

def get_default_system_prompt() -> str:
    """
    Returns the default system prompt for the website summarization task.

    Returns:
        str: The system prompt.
    """
    return (
        "You are an assistant that analyzes the contents of a website. "
        "Your goal is to provide a short, concise summary of the main content, "
        "ignoring text that appears to be navigation, boilerplate, or advertisements. "
        "Respond in markdown format. If the website contains news or announcements, "
        "please highlight the key ones."
    )

def create_user_prompt_for_website(website: Website) -> str:
    """
    Creates a user prompt for the LLM, including the website's title and text.

    Args:
        website (Website): The Website object containing the scraped title and text.

    Returns:
        str: The user prompt.
    """
    user_prompt = f"You are looking at a website titled: '{website.title}'\n\n"
    user_prompt += "The relevant text content of this website is as follows:\n"
    user_prompt += "---------------------------------------------------------\n"
    user_prompt += f"{website.text}\n"
    user_prompt += "---------------------------------------------------------\n\n"
    user_prompt += ("Please provide a short summary of this website in markdown. "
                    "Focus on the primary purpose and key information. "
                    "If it includes significant news or announcements, summarize these too.")
    return user_prompt

def format_messages_for_llm(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
    """
    Formats the system and user prompts into the message structure required by OpenAI's API.

    Args:
        system_prompt (str): The content of the system prompt.
        user_prompt (str): The content of the user prompt.

    Returns:
        list[dict[str, str]]: A list of message dictionaries.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

if __name__ == '__main__':
    # Example usage:
    # Create a dummy Website object for testing
    class DummyWebsite:
        def __init__(self, title, text):
            self.title = title
            self.text = text
            self.url = "http://dummy.com"

    dummy_site = DummyWebsite(
        title="Test Site for Prompts",
        text="This is the main content of the test site. It has some news about LLMs advancing rapidly."
    )

    system_p = get_default_system_prompt()
    print("--- System Prompt ---")
    print(system_p)

    user_p = create_user_prompt_for_website(dummy_site)
    print("\n--- User Prompt ---")
    print(user_p)

    messages = format_messages_for_llm(system_p, user_p)
    print("\n--- Formatted Messages ---")
    import json
    print(json.dumps(messages, indent=2))