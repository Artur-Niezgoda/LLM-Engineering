import json
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any

from web_scraper import Website
from config_manager import ConfigManager
from openai import OpenAI

# Initialize OpenAI client and model using ConfigManager
try:
    config = ConfigManager()
    OPENAI_API_KEY = config.openai_api_key
    OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_KEY)
    MODEL = 'gpt-4o-mini'
except ValueError as e:
    print(f"Failed to initialize OpenAI client: {e}. Please ensure OPENAI_API_KEY is set.")
    OPENAI_CLIENT = None
    MODEL = None

LINK_SYSTEM_PROMPT = """You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\
You should respond in JSON as in this example:
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
If no relevant links are found based on the criteria, respond with:
{
    "links": []
}
"""

def _get_links_user_prompt(website: Website, links_to_analyze: List[str]) -> str:
    """
    Constructs the user prompt for the LLM to identify relevant links.

    Args:
        website (Website): The Website object (used for base URL).
        links_to_analyze (List[str]): The list of links to include in the prompt.

    Returns:
        str: The formatted user prompt.
    """
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(links_to_analyze)
    return user_prompt

def _resolve_relative_url(base_url: str, relative_url: str) -> str:
    """
    Resolves a relative URL to an absolute URL based on a base URL.

    Args:
        base_url (str): The base URL (e.g., "https://example.com").
        relative_url (str): The relative URL (e.g., "/about" or "careers/jobs").

    Returns:
        str: The absolute URL.
    """
    # Ensure the base_url has a scheme for urljoin to work correctly
    if not urlparse(base_url).scheme:
        base_url = "https://" + base_url

    absolute_url = urljoin(base_url, relative_url).strip()

    # Filter out non-web links (e.g., mailto:, tel:)
    if not absolute_url.startswith(('http://', 'https://')):
        return ""

    return absolute_url


def get_relevant_links(url: str, max_links_to_process: int = 100) -> List[Dict[str, str]]:
    """
    Scrapes a webpage, uses an LLM to identify relevant links for a brochure,
    and resolves relative URLs to absolute URLs. Limits the number of links
    sent to the LLM to avoid context window issues.

    Args:
        url (str): The URL of the main company website.
        max_links_to_process (int): The maximum number of links to send to the LLM.
                                    This helps prevent exceeding token limits on large pages.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary
                              contains "type" and "url" of a relevant link.
                              Returns an empty list if an error occurs or no links are found.
    """
    if OPENAI_CLIENT is None:
        print("OpenAI client not initialized. Cannot get relevant links.")
        return []

    website = Website(url)

    if not website.links:
        print(f"No links found on {url} or an error occurred during scraping.")
        return []

    # Limit the number of links sent to the LLM
    links_to_send = website.links[:max_links_to_process]
    if len(website.links) > max_links_to_process:
        print(f"Warning: Page has {len(website.links)} links. Only processing the first {max_links_to_process} to save tokens.")

    try:
        response = OPENAI_CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": LINK_SYSTEM_PROMPT},
                {"role": "user", "content": _get_links_user_prompt(website, links_to_send)}
            ],
            response_format={"type": "json_object"}
        )
        result_json_str = response.choices[0].message.content
        links_data = json.loads(result_json_str)

        relevant_links = []
        for link_info in links_data.get("links", []):
            if "url" in link_info:
                # Resolve relative URLs to absolute URLs
                absolute_url = _resolve_relative_url(url, link_info["url"])
                if absolute_url: # Only add if it's a valid http/https URL
                    relevant_links.append({"type": link_info.get("type", "unknown"), "url": absolute_url})

        return relevant_links

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from LLM for {url}: {e}")
        print(f"LLM Response was: {result_json_str}")
        return []
    except Exception as e:
        print(f"An error occurred while getting relevant links for {url}: {e}")
        return []

# Example usage (for testing this module directly)
if __name__ == "__main__":
    print("--- Testing link_analyzer.py ---")

    # Ensure you have .env with OPENAI_API_KEY set for this to work

    company_url_1 = "https://huggingface.co"
    print(f"\nAnalyzing links for: {company_url_1}")
    relevant_links_1 = get_relevant_links(company_url_1)
    if relevant_links_1:
        print("Relevant links found:")
        for link in relevant_links_1:
            print(f"  Type: {link['type']}, URL: {link['url']}")
    else:
        print("No relevant links found or an error occurred.")

    company_url_2 = "https://example.com"
    print(f"\nAnalyzing links for: {company_url_2}")
    relevant_links_2 = get_relevant_links(company_url_2)
    if relevant_links_2:
        print("Relevant links found:")
        for link in relevant_links_2:
            print(f"  Type: {link['type']}, URL: {link['url']}")
    else:
        print("No relevant links found or an error occurred.")

    # Test with a URL with many links (expect truncation if > max_links_to_process)
    company_url_3 = "https://www.wikipedia.org"
    print(f"\nAnalyzing links for: {company_url_3} (testing with a large site - expect truncation)")
    # Using a smaller limit for Wikipedia to demonstrate truncation
    relevant_links_3 = get_relevant_links(company_url_3, max_links_to_process=50)
    if relevant_links_3:
        print("Relevant links found:")
        for link in relevant_links_3:
            print(f"  Type: {link['type']}, URL: {link['url']}")
    else:
        print("No relevant links found or an error occurred. This is expected for Wikipedia's content and brochure relevance criteria.")

    company_url_4 = "https://openai.com"
    print(f"\nAnalyzing links for: {company_url_4} (Note: May struggle due to bot detection)")
    relevant_links_4 = get_relevant_links(company_url_4, max_links_to_process=50)
    if relevant_links_4:
        print("Relevant links found:")
        for link in relevant_links_4:
            print(f"  Type: {link['type']}, URL: {link['url']}")
    else:
        print("No relevant links found or an error occurred. This might be due to active bot detection.")
