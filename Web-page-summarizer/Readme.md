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