import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List

# Standard headers to mimic a browser
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    Represents a webpage and provides methods to extract its title, text content, and all links.
    Uses Selenium to handle JavaScript-rendered pages by default, with a fallback to requests.
    """

    def __init__(self, url: str, headers: dict = None, use_selenium: bool = True):
        """
        Initializes the Website object by fetching and parsing the content from the given URL.

        Args:
            url (str): The URL of the website to scrape.
            headers (dict, optional): HTTP headers to use for requests or Selenium user-agent.
                                      Defaults to DEFAULT_HEADERS.
            use_selenium (bool, optional): Whether to use Selenium for fetching. Defaults to True.
                                           Set to False to use requests for static pages.

        Raises:
            Exception: If an error occurs during page loading or parsing.
        """
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links: List[str] = [] # Initialize links list

        if headers is None:
            headers = DEFAULT_HEADERS

        if not use_selenium:
            # Fallback to requests for static content if Selenium is not desired
            try:
                print(f"Fetching URL with requests: {self.url}")
                response = requests.get(url, headers=headers, timeout=15) # Increased timeout
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                soup = BeautifulSoup(response.content, 'html.parser')
                self._parse_soup(soup)
            except requests.exceptions.RequestException as e:
                self.text = f"Error fetching URL with requests: {e}"
                print(f"Error fetching URL {self.url} with requests: {e}")
            except Exception as e:
                self.text = f"An unexpected error occurred during requests parsing for {self.url}: {e}"
                print(f"An unexpected error occurred during requests parsing for {self.url}: {e}")
            return

        # --- Selenium Path ---
        driver = None
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
            chrome_options.add_argument("--no-sandbox") # Recommended for running as root/in containers
            chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
            chrome_options.add_argument(f"user-agent={headers['User-Agent']}") # Set user agent
            chrome_options.add_argument("--window-size=1920,1080") # Set a consistent window size
            chrome_options.add_argument("--disable-gpu") # Often recommended for headless on Linux

            # Initialize WebDriver. Assumes chromedriver is in PATH.
            # For more robust WebDriver management, consider 'webdriver_manager' library.
            # Example using webdriver_manager:
            # from webdriver_manager.chrome import ChromeDriverManager
            # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)

            print(f"Fetching URL with Selenium: {self.url}")
            driver.get(url)

            # Wait for the body tag to be present. For complex pages, you might need
            # to wait for specific content elements to appear.
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Optional: Add a small delay to ensure all JS has executed and content is rendered
            # time.sleep(3) # Use sparingly, specific waits are better

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            self._parse_soup(soup)

        except Exception as e:
            self.text = f"Error fetching or processing URL {self.url} with Selenium: {e}"
            print(f"Error with Selenium for {self.url}: {e}")
        finally:
            if driver:
                driver.quit()
                print("Selenium WebDriver closed.")

    def _parse_soup(self, soup: BeautifulSoup):
        """
        Helper method to parse the BeautifulSoup object and extract title, text, and links.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.
        """
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        # Remove irrelevant tags from the body to clean up text content
        if soup.body:
            # Common tags to remove that don't contribute to main content
            tags_to_remove = ["script", "style", "img", "input", "nav", "footer", "aside", "header", "form", "button", "svg", "iframe", "link", "meta"]
            for irrelevant_tag_name in tags_to_remove:
                for tag in soup.body.find_all(irrelevant_tag_name):
                    tag.decompose()

            # Attempt to find main content areas using common selectors (heuristic)
            main_content_selectors = ['main', 'article', '[role="main"]', '.content', '#content', '.main-content', '#main-content']
            content_area = None
            for selector in main_content_selectors:
                if soup.body.select_one(selector):
                    content_area = soup.body.select_one(selector)
                    break

            if content_area:
                self.text = content_area.get_text(separator="\n", strip=True)
            else: # Fallback to full body if no specific main content area is found
                self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = "No body content found."

        if not self.text.strip():
            self.text = "Could not extract meaningful text content."

        # Extract all href attributes from <a> tags
        raw_links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in raw_links if link and link.strip()] # Filter out None or empty strings

    def get_contents(self) -> str:
        """
        Returns a formatted string containing the webpage's title and its cleaned text content.
        This is used to feed the LLM with the page's primary textual information.

        Returns:
            str: The title and text content of the webpage.
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# Example usage (for testing this module directly)
if __name__ == '__main__':
    print("--- Testing web_scraper.py with Selenium and Requests ---")

    test_urls = [
        "https://www.google.com", # Good for Selenium test
        "https://example.com",    # Simple static site for requests test
        "http://nonexistent-domain-12345.com" # Error case
    ]

    for url_to_test in test_urls:
        print(f"\n--- Attempting to scrape: {url_to_test} ---")
        try:
            # Try with Selenium first
            site_selenium = Website(url_to_test, use_selenium=True)
            print(f"Selenium Title: {site_selenium.title}")
            print(f"Selenium Text (first 300 chars): {site_selenium.text[:300].strip()}...")
            print(f"Selenium Links (first 5): {site_selenium.links[:5]}")
            print(f"Total Selenium Links: {len(site_selenium.links)}")

            # Also try with requests for comparison on static sites
            if "example.com" in url_to_test: # Only test requests on a known static site
                site_requests = Website(url_to_test, use_selenium=False)
                print(f"Requests Title: {site_requests.title}")
                print(f"Requests Text (first 300 chars): {site_requests.text[:300].strip()}...")
                print(f"Requests Links (first 5): {site_requests.links[:5]}")
                print(f"Total Requests Links: {len(site_requests.links)}")

        except Exception as e:
            print(f"Could not scrape {url_to_test}: {e}")
        print("---------------------------------------\n")