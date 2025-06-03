import argparse
from summarizer_service import summarize_website # Assumes summarizer_service.py is in the same directory

def display_summary_cli(summary_markdown: str, url: str):
    """
    Displays the summary in a command-line friendly format.
    For this version, it prints the markdown directly.
    In a Jupyter environment, one might use IPython.display.Markdown.

    Args:
        summary_markdown (str): The summary text, expected to be in markdown.
        url (str): The URL that was summarized.
    """
    print(f"\n--- Summary for: {url} ---\n")
    print(summary_markdown)
    print("\n---------------------------\n")

def main():
    """
    Main function to run the website summarizer.
    Parses command-line arguments for the URL to summarize.
    """
    parser = argparse.ArgumentParser(description="Summarize a website using an LLM.")
    parser.add_argument(
        "url",
        nargs='?',
        help="The URL of the website to summarize.",
        default=None # No default, will check if None later
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="The OpenAI model to use for summarization (e.g., gpt-4o-mini, gpt-4)."
    )

    args = parser.parse_args()

    if not args.url:
        # If no URL is provided via command line, use example URLs or prompt the user
        print("No URL provided. Running with example URLs from the notebook.")
        example_urls = [
            "https://edwarddonner.com",
            # "https://cnn.com", # CNN can be tricky due to dynamic content/blocks
            # "https://anthropic.com"
        ]
        if not example_urls:
            print("No example URLs configured and no URL provided. Exiting.")
            print("Usage: python main.py <URL_TO_SUMMARIZE>")
            return

        for url_to_summarize in example_urls:
            print(f"\nAttempting to summarize: {url_to_summarize}")
            summary = summarize_website(url_to_summarize, model=args.model)
            if summary:
                display_summary_cli(summary, url_to_summarize)
            else:
                print(f"Could not generate a summary for {url_to_summarize}.")
    else:
        url_to_summarize = args.url
        print(f"Attempting to summarize: {url_to_summarize}")
        summary = summarize_website(url_to_summarize, model=args.model)
        if summary:
            display_summary_cli(summary, url_to_summarize)
        else:
            print(f"Could not generate a summary for {url_to_summarize}.")

if __name__ == "__main__":
    main()