import requests
from bs4 import BeautifulSoup

# Standard headers to mimic a browser, reducing the chance of being blocked.
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    Represents a webpage and provides methods to extract its title and text content.
    """

    def __init__(self, url: str, headers: dict = None):
        """
        Initializes the Website object by fetching and parsing the content from the given URL.

        Args:
            url (str): The URL of the website to scrape.
            headers (dict, optional): HTTP headers to use for the request.
                                      Defaults to DEFAULT_HEADERS.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the HTTP request.
        """
        self.url = url
        self.title = "No title found"
        self.text = ""

        if headers is None:
            headers = DEFAULT_HEADERS

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            soup = BeautifulSoup(response.content, 'html.parser')

            self.title = soup.title.string if soup.title else "No title found"

            # Remove irrelevant tags like scripts, styles, images, and inputs from the body
            if soup.body:
                for irrelevant_tag in soup.body.find_all(["script", "style", "img", "input", "nav", "footer", "aside"]):
                    irrelevant_tag.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = "No body content found."

        except requests.exceptions.RequestException as e:
            self.text = f"Error fetching URL: {e}"
            print(f"Error fetching URL {self.url}: {e}")
            # Depending on desired behavior, you might want to re-raise or handle differently
            # raise

if __name__ == '__main__':
    # Example usage:
    test_url = "https://www.cnn.com" # A simple site for testing
    print(f"Attempting to scrape: {test_url}")
    try:
        site = Website(test_url)
        print(f"\nTitle: {site.title}")
        print("\nText (first 200 chars):")
        print(site.text[:200] + "...")
    except Exception as e:
        print(f"Could not scrape {test_url}: {e}")
