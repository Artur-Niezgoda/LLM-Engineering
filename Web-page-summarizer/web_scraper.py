import requests # Keep for fallback or non-JS sites if desired, though not used in Selenium path here
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Standard headers to mimic a browser, less critical for Selenium but good practice
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    Represents a webpage and provides methods to extract its title and text content.
    Uses Selenium to handle JavaScript-rendered pages.
    """

    def __init__(self, url: str, headers: dict = None, use_selenium: bool = True):
        """
        Initializes the Website object by fetching and parsing the content from the given URL.

        Args:
            url (str): The URL of the website to scrape.
            headers (dict, optional): HTTP headers (less critical for Selenium but kept for structure).
                                      Defaults to DEFAULT_HEADERS.
            use_selenium (bool, optional): Whether to use Selenium for fetching. Defaults to True.

        Raises:
            Exception: If an error occurs during page loading or parsing with Selenium.
        """
        self.url = url
        self.title = "No title found"
        self.text = ""

        if headers is None:
            headers = DEFAULT_HEADERS # Not directly used by Selenium driver.get but kept for consistency

        if not use_selenium:
            # Fallback to requests if Selenium is not desired (original behavior)
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                self._parse_soup(soup)
            except requests.exceptions.RequestException as e:
                self.text = f"Error fetching URL with requests: {e}"
                print(f"Error fetching URL {self.url} with requests: {e}")
            return

        # --- Selenium Path ---
        driver = None
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
            chrome_options.add_argument("--no-sandbox") # Recommended for running as root/in containers
            chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
            chrome_options.add_argument(f"user-agent={headers['User-Agent']}") # Set user agent

            # Assumes chromedriver is in PATH.
            # For more robust WebDriver management, consider webdriver_manager:
            # from webdriver_manager.chrome import ChromeDriverManager
            # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

            # Simpler assumption: chromedriver is in PATH or specified directly
            # If chromedriver is not in PATH, you'd use:
            # service = ChromeService(executable_path='/path/to/chromedriver')
            # driver = webdriver.Chrome(service=service, options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)

            print(f"Fetching URL with Selenium: {self.url}")
            driver.get(url)

            # Wait for the page to load, specifically for the body tag to be present.
            # You might need more sophisticated waits for specific elements on complex pages.
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Optional: Add a small delay to ensure all JS has executed
            # time.sleep(3) # Adjust as needed, or use more specific waits

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            self._parse_soup(soup)

        except Exception as e:
            self.text = f"Error fetching or processing URL {self.url} with Selenium: {e}"
            print(f"Error with Selenium for {self.url}: {e}")
            # Depending on desired behavior, you might want to re-raise
            # raise
        finally:
            if driver:
                driver.quit()
                print("Selenium WebDriver closed.")

    def _parse_soup(self, soup: BeautifulSoup):
        """
        Helper method to parse the BeautifulSoup object and extract title and text.
        """
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        # Remove irrelevant tags like scripts, styles, images, and inputs from the body
        if soup.body:
            # Common tags to remove, can be expanded
            tags_to_remove = ["script", "style", "img", "input", "nav", "footer", "aside", "header", "form", "button", "svg", "iframe", "link", "meta"]
            for irrelevant_tag_name in tags_to_remove:
                for tag in soup.body.find_all(irrelevant_tag_name):
                    tag.decompose()

            # Attempt to find main content areas if possible (heuristic)
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


if __name__ == '__main__':
    # Example usage:
    test_urls = [
        "https://openai.com", # This should work better with Selenium
        "https://example.com" # Simple site
    ]

    for url_to_test in test_urls:
        print(f"\n--- Attempting to scrape: {url_to_test} ---")
        try:
            site = Website(url_to_test)
            print(f"Title: {site.title}")
            print(f"\nText (first 300 chars of {len(site.text)} total):")
            print(site.text[:300].strip() + "...")
        except Exception as e:
            print(f"Could not scrape {url_to_test}: {e}")
        print("---------------------------------------\n")
