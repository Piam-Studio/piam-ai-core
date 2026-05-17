# src/piam_ai_core/cli.py
import argparse
import sys
import os
from pydantic import BaseModel, Field
from piam_ai_core.generator import PiamAiGenerator


class ParsedRequirement(BaseModel):
    """
    Data structure representing the cleaned and structured client requirement
    before it gets passed to the underlying LLM logic.
    """
    raw_text: str
    target_table: str = Field(default="tl_content")  # Default to Contao content elements
    output_filename: str


class InputParser:
    """
    Responsible for sanitizing, validating, and structuring raw inputs
    received from the CLI or external bridges.
    """

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Cleans the incoming text requirement from hazardous characters
        and trims unnecessary whitespaces.
        """
        if not text:
            return ""
        return text.strip().replace('"', '\\"')

    def parse(self, raw_input: str, table_name: str, file_name: str) -> ParsedRequirement:
        """
        Transforms raw string arguments into a validated ParsedRequirement object.
        """
        clean_text = self.sanitize_input(raw_input)

        if not clean_text:
            print("[ERROR] The provided requirement text is empty.", file=sys.stderr)
            sys.exit(1)

        # Guarantee that the file extension is always .php
        if not file_name.endswith(".php"):
            file_name = f"{file_name}.php"

        return ParsedRequirement(
            raw_text=clean_text,
            target_table=table_name,
            output_filename=file_name
        )


def main():
    """
    The main CLI entry point for the piam-ai-core suite.
    Handles native command line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Piam AI-Core: Production-ready Contao DCA Code Generator"
    )

    # Define execution arguments
    parser.add_argument(
        "--requirements", "-r",
        required=True,
        help="The raw text briefing or requirement specification from the client."
    )
    parser.add_argument(
        "--table", "-t",
        default="tl_content",
        help="The target Contao database table (e.g., tl_content, tl_news). Default: tl_content"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="The name of the target output file (e.g., tl_content_teaser.php)."
    )

    args = parser.parse_args()

    # 1. Process and parse the input data
    input_parser = InputParser()
    structured_data = input_parser.parse(
        raw_input=args.requirements,
        table_name=args.table,
        file_name=args.output
    )

    print("==================================================")
    print("        PIAM AI-CORE: INTERFACE PROCESSING        ")
    print("==================================================")
    print(f"[INFO] Target Table: {structured_data.target_table}")
    print(f"[INFO] Target File:  {structured_data.output_filename}")
    print("[INFO] Initializing generator engine...")

    # 2. Trigger the local AI inference engine
    generator = PiamAiGenerator()

    print("[INFO] Model loaded. Processing local code generation... Please wait.")
    generated_php = generator.generate_dca(structured_data.raw_text)

    # 3. Save the generated code directly into a local export directory
    export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))
    os.makedirs(export_dir, exist_ok=True)

    target_file_path = os.path.join(export_dir, structured_data.output_filename)

    with open(target_file_path, "w", encoding="utf-8") as php_file:
        php_file.write(generated_php)

    print("==================================================")
    print("[SUCCESS] Contao DCA File successfully written!")
    print(f"[LOCATION] {target_file_path}")
    print("==================================================")


if __name__ == "__main__":
    main()
