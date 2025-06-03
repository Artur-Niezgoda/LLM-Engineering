# Web Page Summarizer

This project implements a Python application that acts as a "Reader's Digest of the internet." Give it a URL, and it will fetch the web page's content and provide a summary using a Large Language Model (LLM).

## Project Goal

The primary goal is to create a tool that can quickly summarize the main content of a web page, demonstrating a practical application of LLMs for information extraction and condensation.

## Features

* **Web Content Fetching:** Retrieves HTML content from a given URL.
* **Text Extraction:** Parses HTML to extract meaningful text, attempting to remove boilerplate like navigation, scripts, and styles.
* **LLM-Powered Summarization:** Uses an LLM (e.g., OpenAI's GPT models) to generate a concise summary of the extracted text.
* **Markdown Output:** Summaries are formatted in Markdown for readability.
* **Modular Code:** The application is structured into several Python modules for clarity and maintainability.
* **API Key Management:** Securely handles API keys using a `.env` file.
* **Command-Line Interface:** Allows users to specify URLs directly from the command line.

## Technology Stack

* Python 3.x
* **OpenAI API:** For accessing LLM capabilities (e.g., `gpt-4o-mini`).
* **Requests:** For making HTTP requests to fetch web pages.
* **BeautifulSoup4:** For parsing HTML and extracting text content.
* **python-dotenv:** For managing environment variables (especially the `OPENAI_API_KEY`).
* **Selenium:** For browser automation to handle JavaScript-rendered web pages.

## Setup and Installation

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <URL_of_LLM-Engineering_repository>
    cd LLM-Engineering/Web-page-summarizer
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    A `requirements.txt` file is provided. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, you can create it with the content provided below or install manually: `pip install openai requests beautifulsoup4 python-dotenv`)*

4.  **Set Up Your OpenAI API Key:**
    Create a file named `.env` in the `Web-page-summarizer` directory. Add your OpenAI API key to this file:
    ```env
    OPENAI_API_KEY='your_actual_openai_api_key_here'
    ```
    Replace `your_actual_openai_api_key_here` with your valid OpenAI API key (e.g., `sk-proj-...`).

## How to Run

Once the setup is complete, you can run the application from your terminal within the `Web-page-summarizer` directory. The general command format is:

```bash
python main.py <URL_TO_SUMMARIZE> [--model MODEL_NAME]
```


You are absolutely right! My apologies. I seem to have made an error in my previous responses by not ensuring every fenced code block was properly closed. That would definitely cause rendering issues on GitHub.

Let's try this again with the corrected, complete Readme.md content. I've double-checked all the fenced code blocks (bash ...) to ensure they are properly closed.

Markdown

# Web Page Summarizer

This project implements a Python application that acts as a "Reader's Digest of the internet." Give it a URL, and it will fetch the web page's content and provide a summary using a Large Language Model (LLM).

## Project Goal

The primary goal is to create a tool that can quickly summarize the main content of a web page, demonstrating a practical application of LLMs for information extraction and condensation.

## Features

* **Web Content Fetching:** Retrieves HTML content from a given URL.
* **Text Extraction:** Parses HTML to extract meaningful text, attempting to remove boilerplate like navigation, scripts, and styles.
* **LLM-Powered Summarization:** Uses an LLM (e.g., OpenAI's GPT models) to generate a concise summary of the extracted text.
* **Markdown Output:** Summaries are formatted in Markdown for readability.
* **Modular Code:** The application is structured into several Python modules for clarity and maintainability.
* **API Key Management:** Securely handles API keys using a `.env` file.
* **Command-Line Interface:** Allows users to specify URLs directly from the command line.

## Technology Stack

* Python 3.x
* **OpenAI API:** For accessing LLM capabilities (e.g., `gpt-4o-mini`).
* **Requests:** For making HTTP requests to fetch web pages.
* **BeautifulSoup4:** For parsing HTML and extracting text content.
* **python-dotenv:** For managing environment variables (especially the `OPENAI_API_KEY`).
* **Selenium:** For browser automation to handle JavaScript-rendered web pages.

## Setup and Installation

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <URL_of_LLM-Engineering_repository>
    cd LLM-Engineering/Web-page-summarizer
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    A `requirements.txt` file is provided. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```


4.  **Set Up WebDriver for Selenium:**
    Selenium requires a WebDriver to interact with your chosen browser.
    * **Download WebDriver:**
        * For **Chrome**: Download [ChromeDriver](https://chromedriver.chromium.org/downloads) that matches your Chrome browser version.
        * For **Firefox**: Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases) that matches your Firefox browser version.
        * For other browsers, find the appropriate WebDriver.
    * **Make WebDriver Accessible:**
        * **Option 1 (Recommended for simplicity):** Place the downloaded WebDriver executable (e.g., `chromedriver.exe` on Windows, `chromedriver` on Linux/macOS) in a directory that is part of your system's **PATH** environment variable.
        * **Option 2:** Alternatively, you can modify the `web_scraper.py` script to point directly to the WebDriver executable's path (this is less portable).
            ```python
            # Example for Chrome in web_scraper.py
            # from selenium.webdriver.chrome.service import Service as ChromeService
            # service = ChromeService(executable_path='/path/to/your/chromedriver')
            # driver = webdriver.Chrome(service=service, options=chrome_options)
            ```
    * **Note:** The provided `web_scraper.py` currently assumes the WebDriver (specifically ChromeDriver) is in your system's PATH. For more automated WebDriver management in Python projects, consider using the `webdriver-manager` package, though it's not included in this basic setup to keep dependencies minimal initially.

5.  **Set Up Your OpenAI API Key:**
    Create a file named `.env` in the `Web-page-summarizer` directory. Add your OpenAI API key to this file:
    ```env
    OPENAI_API_KEY='your_actual_openai_api_key_here'
    ```
    Replace `your_actual_openai_api_key_here` with your valid OpenAI API key (e.g., `sk-proj-...`).

## How to Run

Once the setup is complete, you can run the application from your terminal within the `Web-page-summarizer` directory. The general command format is:

```bash
python main.py <URL_TO_SUMMARIZE> [--model MODEL_NAME]
```
## Examples:

* Summarize a specific website using the default model (`gpt-4o-mini`):

```bash
python main.py "[https://www.example.com](https://www.example.com)"
```

* Summarize a website and specify a different model:

```bash
python main.py "[https://edwarddonner.com](https://edwarddonner.com)" --model gpt-4
```

(Note: Ensure the specified model is compatible and you have access to it via your API key.)

* If you run python main.py without a URL, it may process pre-defined example URLs as coded in main.py.

## File Structure
The project is organized into the following Python modules:

* `main.py`: Entry point of the application; handles command-line arguments and orchestrates the summarization.
* `summarizer_service.py`: Core service layer that coordinates web scraping, prompt generation, and LLM interaction.
* `llm_handler.py`: Manages communication with the LLM API (e.g., OpenAI).
* `prompt_generator.py`: Creates and formats the system and user prompts for the LLM.
* `web_scraper.py`: Contains the Website class responsible for fetching and parsing web page content.
* `config_manager.py`: Handles loading and validation of the API key from the .env file.
* `requirements.txt`: Lists project dependencies.
* `.env` (to be created by you): Stores your OPENAI_API_KEY.

## Troubleshooting & Limitations
* API Key: Ensure your OPENAI_API_KEY is correctly set in the .env file and is active.
* Website Compatibility:
    * This tool uses a basic approach for web scraping. Websites heavily reliant on JavaScript for rendering content may not be summarized accurately. Consider tools like Selenium for such cases.
    * Some websites may block scraping attempts (e.g., via Cloudflare or other security measures), leading to errors or incomplete content.
* Content Quality: The quality of the summary depends on the LLM used and the clarity of the extracted text.
* **Selenium WebDriver Issues**:
    * Ensure you have the correct WebDriver installed and that it's accessible via your system's PATH or explicitly configured in the code.
    * The WebDriver version must match your browser version.
    * Headless mode (used by default) can sometimes behave differently than a full browser; for complex sites, you might need to experiment with Selenium options.

## Potential Future Enhancements
* Integration with Selenium or Playwright for better JavaScript-rendered page handling.
* More sophisticated text cleaning and extraction logic.
* Option for users to specify summary length or style.
* Error handling for a wider range of web scraping issues.
* Batch summarization of multiple URLs.

## Acknowledgements

This project is based on the "YOUR FIRST LAB" exercise from an LLM engineering course by Edward Donner. The foundational concepts and initial goal were inspired by this lab.