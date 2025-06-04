# Marketing Brochures Generator

This project is a Python application designed to automatically generate marketing brochures for companies based on their public websites. It leverages web scraping techniques to gather information and Large Language Models (LLMs) to synthesize that information into a concise, Markdown-formatted brochure.

## Project Goal

The primary goal is to demonstrate a practical application of LLMs combined with web scraping to automate content generation for business and marketing purposes. It creates a "snapshot" summary of a company suitable for prospective clients, investors, or potential recruits.

## Features

* **Intelligent Web Scraping:** Fetches content from a primary URL and identifies relevant sub-pages (e.g., "About Us," "Careers," "Pricing") using an LLM to refine the search.
* **Hybrid Scraping Approach:** Employs both `requests` for static content and `Selenium` with headless Chrome for JavaScript-rendered pages, providing robust fetching capabilities.
* **LLM-Powered Content Aggregation:** Gathers textual information from the main page and relevant sub-pages.
* **Dynamic Brochure Generation:** Uses an LLM (OpenAI's GPT models) to create a marketing brochure in Markdown format.
* **Streaming Output:** Displays the brochure content in real-time in the console or Jupyter Notebook.
* **Markdown File Saving:** Automatically saves the generated brochure as a `.md` file in the project folder for easy sharing and version control.
* **Modular Design:** Organized into separate Python modules for clarity, maintainability, and reusability.

## Technology Stack

* **Python 3.x**
* **OpenAI API:** For Large Language Model capabilities (e.g., `gpt-4o-mini`).
* **`requests`:** For making HTTP requests to fetch web pages.
* **`beautifulsoup4`:** For parsing HTML content and extracting text/links.
* **`selenium`:** For controlling a headless Chrome browser to scrape JavaScript-rendered content.
* **`python-dotenv`:** For securely managing environment variables (like API keys).
* **`argparse`:** For handling command-line arguments.

## Setup and Installation

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone [https://github.com/your-username/LLM-Engineering.git](https://github.com/your-username/LLM-Engineering.git) # Replace with your repo URL
    cd LLM-Engineering/marketing-brochures
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows
    source venv/bin/activate # On macOS/Linux
    ```
    *Make sure your virtual environment is activated whenever you run the scripts.*

3.  **Install Dependencies:**
    Create a `requirements.txt` file in the `marketing-brochures` directory with the following content:
    ```
    requests
    beautifulsoup4
    selenium
    openai
    python-dotenv
    ```
    Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You'll also need to have [Google Chrome](https://www.google.com/chrome/) installed and a compatible [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) available in your system's PATH for Selenium to work.*

4.  **Set Up Your OpenAI API Key:**
    Create a file named `.env` in the `marketing-brochures` directory (the same folder where your Python scripts are). Add your OpenAI API key to this file:
    ```env
    OPENAI_API_KEY='your_actual_openai_api_key_here'
    ```
    Replace `'your_actual_openai_api_key_here'` with your valid OpenAI API key (e.g., `sk-proj-...`).

## How to Run

Navigate to the `marketing-brochures` directory in your activated virtual environment and run the `main.py` script:

```bash
cd path/to/LLM-Engineering/marketing-brochures

# Ensure your venv is activated: .\venv\Scripts\activate or source venv/bin/activate

python main.py <COMPANY_NAME> <COMPANY_URL> [OPTIONS]
```
# Arguments:

* <COMPANY_NAME>: The name of the company (e.g., "HuggingFace"). Enclose in quotes if it contains spaces.
* <COMPANY_URL>: The primary URL of the company's website (e.g., "https://huggingface.co"). Enclose in quotes.

# Options:

* `--no-save`: Do not save the generated brochure to a Markdown file.
* `--filename <FILENAME>`: Specify a custom filename for the saved brochure (e.g., "my_brochure.md"). If not provided, a default name like company_name_brochure.md will be used.

## Examples:

* Generate a brochure for HuggingFace and save it (default behavior):
```bash
python main.py "HuggingFace" "[https://huggingface.co](https://huggingface.co)"
```

* Generate a brochure for Example Corp and save it with a custom name:

```bash
python main.py "Example Corp" "[https://example.com](https://example.com)" --filename "example_company_profile.md"
```

* Generate a brochure without saving the file:
```bash
python main.py "Test Company" "[https://www.testcompany.com](https://www.testcompany.com)" --no-save
```
* Get help/see all options:
```bash
python main.py --help
```
## File Structure
The project is organized into the following Python modules:

* `main.py`: The command-line entry point of the application. It parses arguments and orchestrates the brochure generation process.
* `brochure_generator.py`: Contains the core logic for fetching content from multiple pages, constructing the LLM prompt, making API calls (for static or streaming output), and saving the final brochure.
* `link_analyzer.py`: Manages the LLM-driven identification of relevant sub-links from a given webpage, including resolving relative URLs.
* `web_scraper.py`: Provides the Website class responsible for fetching and parsing HTML content from URLs, employing both requests and Selenium for robust scraping.
* `config_manager.py`: Handles the secure loading and validation of API keys from .env files.
* `.env` (you create this): Stores your OPENAI_API_KEY.
* `requirements.txt`: Lists all Python dependencies for the project.

## Troubleshooting & Limitations

* API Key Issues: Ensure your OPENAI_API_KEY is correctly set in the .env file and is active with sufficient quota.
ChromeDriver / Selenium: If you encounter errors related to Chrome/Chromium or ChromeDriver, ensure:
    * Chrome browser is installed.
    * The chromedriver executable matches your Chrome browser version.
        chromedriver is accessible in your system's PATH.
    * For headless environments, flags like --disable-gpu and --enable-unsafe-swiftshader (already in web_scraper.py) are crucial.
* Bot Detection (e.g., Cloudflare): Some websites (like openai.com) employ advanced bot detection. The current scraping setup might struggle or be blocked by these measures, returning incomplete content or challenge pages. For such sites, more sophisticated bypassing techniques would be required.
* LLM Context Length: For very large websites, even with link truncation, the combined text content might exceed the LLM's input token limit. Monitor warnings about truncation and consider reducing max_llm_links in brochure_generator.py if needed.
* Rate Limits: Frequent API calls might hit OpenAI's rate limits. The script includes a small time.sleep but further delays might be needed for heavy use.

## Acknowledgements

This project is a continuation and refactoring of concepts explored in an LLM engineering course, building upon initial lab exercises for web content summarization and generation.