from typing import List, Dict, Any
from openai import OpenAI
import time
import json
import os

# Try to import IPython display tools and check for an active IPython shell
IPYTHON_AVAILABLE = False
try:
    from IPython.display import Markdown, display, update_display
    from IPython import get_ipython
    if get_ipython() is not None: # Check if there's an active IPython shell
        IPYTHON_AVAILABLE = True
    else:
        print("IPython.display module found, but not running in an interactive IPython shell. Running in non-Jupyter mode.")
except ImportError:
    print("IPython.display module not found. Running in non-Jupyter mode.")

# Mock display functions for non-Jupyter environment if not available
if not IPYTHON_AVAILABLE:
    class MockDisplayHandle:
        def __init__(self):
            self.display_id = None # Mock display_id

    def display(obj, display_id=None):
        if isinstance(obj, Markdown):
            print(obj.data) # Print Markdown content as plain text
        else:
            print(obj)
        return MockDisplayHandle()

    def update_display(obj, display_id):
        if isinstance(obj, Markdown):
            print(obj.data, end='', flush=True)
        else:
            print(obj)

# Assuming web_scraper, link_analyzer, and config_manager are in the same directory
from web_scraper import Website
from link_analyzer import get_relevant_links, LINK_SYSTEM_PROMPT
from config_manager import ConfigManager

# Initialize OpenAI client and model using ConfigManager
try:
    config = ConfigManager()
    OPENAI_API_KEY = config.openai_api_key
    OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_KEY)
    MODEL = 'gpt-4o-mini'
except ValueError as e:
    print(f"Failed to initialize OpenAI client: {e}. Brochure generation will not work.")
    OPENAI_CLIENT = None
    MODEL = None

# System prompt for brochure generation
SYSTEM_PROMPT = """You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."""

# Define the output folder for brochures - set to current directory as requested
BROCHURES_OUTPUT_FOLDER = "." # Saves in the current directory, i.e., marketing-brochures/

def save_brochure_to_file(company_name: str, brochure_content: str, folder: str = BROCHURES_OUTPUT_FOLDER, filename: str = None):
    """
    Saves the generated brochure content to a Markdown file.

    Args:
        company_name (str): The name of the company, used for default filename.
        brochure_content (str): The Markdown content of the brochure.
        folder (str): The folder where the file should be saved. Defaults to BROCHURES_OUTPUT_FOLDER.
        filename (str, optional): The specific filename (e.g., "my_brochure.md").
                                  If None, a default filename will be generated.
    """
    # Ensure the output folder exists (it will be the current directory if folder='.')
    os.makedirs(folder, exist_ok=True)

    if filename is None:
        # Sanitize company name for a valid filename
        safe_company_name = "".join(c if c.isalnum() else "_" for c in company_name).lower()
        filename = f"{safe_company_name}_brochure.md"

    file_path = os.path.join(folder, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(brochure_content)
        print(f"Brochure saved to: {os.path.abspath(file_path)}")
    except IOError as e:
        print(f"Error saving brochure to file {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving the file: {e}")


def get_all_details(base_url: str, max_llm_links: int = 50) -> str:
    """
    Fetches content from the base URL and its LLM-identified relevant sub-links.

    Args:
        base_url (str): The primary URL of the company website.
        max_llm_links (int): The maximum number of links to send to the LLM for relevance analysis.

    Returns:
        str: A concatenated string of content from the landing page and relevant sub-pages.
             Returns an empty string if base URL content cannot be fetched.
    """
    all_content = []

    # Get content from the landing page
    print(f"Fetching content from landing page: {base_url}")
    landing_page = Website(base_url)
    if landing_page.text.strip():
        all_content.append(f"Landing page:\n{landing_page.get_contents()}")
    else:
        print(f"Warning: Could not fetch content for landing page {base_url}. Skipping.")
        return "" # If landing page fails, it's hard to proceed meaningfully

    # Get relevant links and then content from those links
    print(f"Identifying relevant links for {base_url}...")
    relevant_links = get_relevant_links(base_url, max_links_to_process=max_llm_links)

    if relevant_links:
        print(f"Found {len(relevant_links)} relevant links.")
        for link_info in relevant_links:
            link_type = link_info.get("type", "unknown page")
            link_url = link_info.get("url")

            if link_url:
                print(f"Fetching content from {link_type} page: {link_url}")
                sub_page = Website(link_url)
                if sub_page.text.strip():
                    all_content.append(f"\n\n--- {link_type.upper()} ---\nURL: {link_url}\n{sub_page.get_contents()}")
                else:
                    print(f"Warning: Could not fetch content for {link_type} page {link_url}. Skipping.")
                time.sleep(1) # Small delay to be polite to websites and avoid rate limits
            else:
                print(f"Warning: Relevant link found with no URL: {link_info}. Skipping.")
    else:
        print("No additional relevant links identified by LLM or an error occurred during link analysis.")

    return "\n".join(all_content)

def get_brochure_user_prompt(company_name: str, url: str) -> str:
    """
    Constructs the user prompt for the LLM to create the brochure.

    Args:
        company_name (str): The name of the company.
        url (str): The base URL of the company website.

    Returns:
        str: The formatted user prompt for brochure generation.
    """
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"

    all_company_details = get_all_details(url)
    if not all_company_details.strip():
        print(f"Error: No content obtained for {company_name} from {url}. Brochure will be empty.")
        return "No content available to create a brochure."

    MAX_PROMPT_CHARS = 80000
    if len(all_company_details) > MAX_PROMPT_CHARS:
        print(f"Warning: Total content is {len(all_company_details)} chars, truncating to {MAX_PROMPT_CHARS} chars.")
        user_prompt += all_company_details[:MAX_PROMPT_CHARS]
        user_prompt += "\n\n[Content truncated due to length limitations]"
    else:
        user_prompt += all_company_details

    return user_prompt

def create_brochure(company_name: str, url: str, save_to_file: bool = True, filename: str = None):
    """
    Generates and displays a static brochure for a given company and URL.
    Optionally saves the brochure to a Markdown file.

    Args:
        company_name (str): The name of the company.
        url (str): The base URL of the company website.
        save_to_file (bool): If True, saves the brochure to a Markdown file.
        filename (str, optional): The filename for the saved brochure. If None, a default is generated.
    """
    if OPENAI_CLIENT is None:
        print("OpenAI client not initialized. Cannot create brochure.")
        return

    user_prompt = get_brochure_user_prompt(company_name, url)
    if user_prompt == "No content available to create a brochure.":
        print("Cannot create brochure due to lack of content.")
        return

    print(f"\nGenerating brochure for {company_name}...")
    try:
        response = OPENAI_CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        result = response.choices[0].message.content

        if IPYTHON_AVAILABLE:
            display(Markdown(result))
        else:
            print("\n--- Generated Brochure (Markdown) ---")
            print(result)
            print("-------------------------------------")

        if save_to_file:
            save_brochure_to_file(company_name, result, folder=BROCHURES_OUTPUT_FOLDER, filename=filename)

    except Exception as e:
        print(f"Error generating brochure with LLM: {e}")
        if "maximum context length" in str(e):
            print("Tip: The prompt might be too long. Try reducing MAX_PROMPT_CHARS or max_links_to_process.")
        elif "rate limit" in str(e):
            print("Tip: You might be hitting rate limits. Wait a bit before retrying.")
        else:
            print("Please check your API key and network connection.")

def stream_brochure(company_name: str, url: str, save_to_file: bool = True, filename: str = None):
    """
    Generates and streams the brochure for a given company and URL,
    displaying it with a typewriter animation.
    Optionally saves the brochure to a Markdown file after streaming is complete.

    Args:
        company_name (str): The name of the company.
        url (str): The base URL of the company website.
        save_to_file (bool): If True, saves the brochure to a Markdown file.
        filename (str, optional): The filename for the saved brochure. If None, a default is generated.
    """
    if OPENAI_CLIENT is None:
        print("OpenAI client not initialized. Cannot stream brochure.")
        return

    user_prompt = get_brochure_user_prompt(company_name, url)
    if user_prompt == "No content available to create a brochure.":
        print("Cannot stream brochure due to lack of content.")
        return

    print(f"\nStreaming brochure for {company_name}...")
    full_response_content = "" # Accumulate streamed content for saving
    try:
        stream = OPENAI_CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            stream=True,
            temperature=0.7,
            max_tokens=2000
        )

        if IPYTHON_AVAILABLE:
            display_handle = display(Markdown(""), display_id=True)
            for chunk in stream:
                content_chunk = chunk.choices[0].delta.content or ''
                full_response_content += content_chunk
                cleaned_chunk = content_chunk.replace("```markdown", "").replace("```", "")
                update_display(Markdown(full_response_content.replace("```markdown", "").replace("```", "")), display_id=display_handle.display_id)
        else:
            print("\n--- Streaming Generated Brochure ---")
            for chunk in stream:
                content_chunk = chunk.choices[0].delta.content or ''
                full_response_content += content_chunk
                content_chunk = content_chunk.replace("```markdown", "").replace("```", "")
                print(content_chunk, end='', flush=True)
            print("\n------------------------------------")

        print("\nBrochure streaming complete.")

        if save_to_file:
            save_brochure_to_file(company_name, full_response_content, folder=BROCHURES_OUTPUT_FOLDER, filename=filename)

    except Exception as e:
        print(f"Error streaming brochure with LLM: {e}")
        if "maximum context length" in str(e):
            print("Tip: The prompt might be too long. Try reducing MAX_PROMPT_CHARS or max_links_to_process.")
        elif "rate limit" in str(e):
            print("Tip: You might be hitting rate limits. Wait a bit before retrying.")
        else:
            print("Please check your API key and network connection.")


# Example usage (for testing this module directly)
if __name__ == "__main__":
    print("--- Testing brochure_generator.py ---")

    # Example 1: HuggingFace (streamed and saved to 'marketing-brochures/huggingface_brochure.md')
    print("\nAttempting to stream brochure for HuggingFace and save to file...")
    stream_brochure("HuggingFace", "https://huggingface.co", save_to_file=True)
    print("\n------------------------------------------------------")

    # Example 2: Example.com (streamed and saved to 'marketing-brochures/example_corp_custom_name.md')
    print("\nAttempting to stream brochure for Example.com and save to file...")
    stream_brochure("Example Corp", "https://example.com", save_to_file=True, filename="example_corp_custom_name.md")
    print("\n------------------------------------------------------")