import argparse
import os
import sys
from brochure_generator import stream_brochure

def main():
    """
    Main function to parse command-line arguments and generate a marketing brochure.
    """
    parser = argparse.ArgumentParser(
        description="Generate a marketing brochure for a company from its website.",
        formatter_class=argparse.RawTextHelpFormatter # For nicer help formatting
    )

    parser.add_argument(
        "company_name",
        type=str,
        help="The name of the company for which to generate the brochure."
    )
    parser.add_argument(
        "url",
        type=str,
        help="The primary URL of the company's website (e.g., 'https://example.com')."
    )
    parser.add_argument(
        "--no-save",
        action="store_false",
        dest="save_to_file",
        help="Do not save the generated brochure to a Markdown file."
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help=(
            "Optional: Specify the filename for the saved brochure (e.g., 'my_company_brochure.md').\n"
            "If not provided, a default name like 'company_name_brochure.md' will be used."
        )
    )

    args = parser.parse_args()

    print(f"Starting brochure generation for {args.company_name} from {args.url}...")

    stream_brochure(
        company_name=args.company_name,
        url=args.url,
        save_to_file=args.save_to_file,
        filename=args.filename
    )

    print("\nBrochure generation process completed.")

if __name__ == "__main__":
    main()
