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
    Uses Selenium for JavaScript-rendered pages and has a fallback to requests for static pages.
    """

    def __init__(self, url: str, headers: dict = None, use_selenium: bool = True):
        """
        Initializes the Website object by fetching and parsing the content from the given URL.

        Args:
            url (str): The URL of the website to scrape.
            headers (dict, optional): HTTP headers (used for requests and Selenium user-agent).
                                      Defaults to DEFAULT_HEADERS.
            use_selenium (bool, optional): Whether to use Selenium for fetching. Defaults to True.
        """
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links: List[str] = []

        if headers is None:
            headers = DEFAULT_HEADERS

        if not use_selenium:
            # Fallback to requests for static content
            try:
                print(f"Fetching URL with requests: {self.url}")
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                self._parse_soup(soup)
                print(f"Successfully scraped {self.url} with requests.")
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
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--enable-unsafe-swiftshader")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--blink-settings=imagesEnabled=false")

            driver = webdriver.Chrome(options=chrome_options)

            print(f"Fetching URL with Selenium: {self.url}")
            driver.get(url)

            # Wait for the body tag to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            self._parse_soup(soup)
            print(f"Successfully scraped {self.url} with Selenium.")

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
        """
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        # Extract all href attributes from <a> tags
        raw_links = []
        for link_tag in soup.find_all('a', href=True):
            href = link_tag.get('href')
            if href and href.strip():
                raw_links.append(href)
        self.links = raw_links

        # Remove irrelevant tags from the body for text extraction
        if soup.body:
            tags_to_remove = ["script", "style", "img", "input", "nav", "footer", "aside", "header", "form", "button", "svg", "iframe", "link", "meta"]
            for irrelevant_tag_name in tags_to_remove:
                for tag in soup.body.find_all(irrelevant_tag_name):
                    tag.decompose()

            # Attempt to find main content areas using common selectors
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

    def get_contents(self) -> str:
        """
        Returns a formatted string containing the webpage's title and its cleaned text content.
        This is used to feed the LLM with the page's primary textual information.

        Returns:
            str: The title and text content of the webpage.
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# Example usage for testing this module directly
if __name__ == '__main__':
    print("--- Testing web_scraper.py with Link Extraction ---")

    test_urls = [
        "https://huggingface.co",
        "https://example.com",
        "https://www.wikipedia.org",
        "https://openai.com", # Known Cloudflare protected site
        "http://nonexistent-domain-12345.com"
    ]

    for url_to_test in test_urls:
        print(f"\n--- Attempting to scrape: {url_to_test} ---")
        try:
            site = Website(url_to_test, use_selenium=True)
            print(f"Title: {site.title}")
            print(f"Text (first 300 chars of {len(site.text)} total):")
            print(site.text[:300].strip() + "...")
            print(f"Links (first 5 of {len(site.links)} total): {site.links[:5]}")
        except Exception as e:
            print(f"Could not scrape {url_to_test}: {e}")
        print("---------------------------------------\n")