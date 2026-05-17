# src/piam_ai_core/cli.py
import argparse
import sys
import os
import json
import re
from piam_ai_core.generator import PiamAiGenerator


class BundleStructureManager:
    def __init__(self, base_output_dir: str, table_name: str):
        self.base_dir = base_output_dir
        self.table = table_name
        self.dca_path = os.path.join(self.base_dir, "contao", "dca", f"{self.table}.php")
        self.lang_paths = {
            "de": os.path.join(self.base_dir, "contao", "languages", "de", f"{self.table}.php"),
            "en": os.path.join(self.base_dir, "contao", "languages", "en", f"{self.table}.php"),
            "fr": os.path.join(self.base_dir, "contao", "languages", "fr", f"{self.table}.php")
        }

    def read_existing_context(self) -> dict:
        context = {"dca": "", "languages": {"de": "", "en": "", "fr": ""}}
        if os.path.exists(self.dca_path):
            with open(self.dca_path, "r", encoding="utf-8") as f:
                context["dca"] = f.read()
        for lang, path in self.lang_paths.items():
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    context["languages"][lang] = f.read()
        return context

    def write_bundle_files(self, dca_content: str, lang_contents: dict):
        os.makedirs(os.path.dirname(self.dca_path), exist_ok=True)
        with open(self.dca_path, "w", encoding="utf-8") as f:
            f.write(dca_content)
        for lang, content in lang_contents.items():
            path = self.lang_paths[lang]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


def clean_and_parse_json(raw_string: str) -> dict:
    """
    Robust processing engine to sanitize and parse LLM-generated JSON strings
    even if minor quotation or escaping anomalies occur within the payload.
    """
    # Remove potential markdown block wrappers if model ignores instructions
    cleaned = raw_string.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Fix unescaped internal double quotes specifically in the generated SQL strings
    cleaned = re.sub(r'["\u201c\u201d]sql["\u201c\u201d]\s*=>\s*["\u201c\u201d]([^"\n]+)', r'"sql" => \'\1\'', cleaned)
    cleaned = re.sub(r'\'sql\'\s*=>\s*\"([^\"]+)', r"'sql' => '\1'", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback regex extraction if JSON structural boundaries are completely broken
        dca_match = re.search(r'"dca"\s*:\s*"(.+?)"\s*,\s*"languages"', cleaned, re.DOTALL)
        de_match = re.search(r'"de"\s*:\s*"(.+?)"\s*,\s*"en"', cleaned, re.DOTALL)
        en_match = re.search(r'"en"\s*:\s*"(.+?)"\s*,\s*"fr"', cleaned, re.DOTALL)
        fr_match = re.search(r'"fr"\s*:\s*"(.+?)"\s*}', cleaned, re.DOTALL)

        if dca_match and de_match and en_match and fr_match:
            return {
                "dca": dca_match.group(1).encode().decode('unicode_escape'),
                "languages": {
                    "de": de_match.group(1).encode().decode('unicode_escape'),
                    "en": en_match.group(1).encode().decode('unicode_escape'),
                    "fr": fr_match.group(1).encode().decode('unicode_escape')
                }
            }
        raise


def main():
    parser = argparse.ArgumentParser(description="Piam AI-Core: Automated Multi-File Contao Suite")
    parser.add_argument("--requirements", "-r", required=True, help="The instruction to create, modify or extend.")
    parser.add_argument("--table", "-t", default="tl_content", help="Target Contao table.")

    args = parser.parse_args()
    export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/piamstudio-contao-commerce-v1"))

    manager = BundleStructureManager(export_dir, args.table)
    existing_context = manager.read_existing_context()

    compiled_prompt = f"Existing Project Context:\n{json.dumps(existing_context, indent=2)}\n\nUser Task: {args.requirements}"

    print("==================================================")
    print("      PIAM AI-CORE: MULTI-FILE ARCHITECT ENGINE   ")
    print("==================================================")
    print(f"[INFO] Target Table: {args.table}")
    print("[INFO] Processing local context and running inference...")

    generator = PiamAiGenerator()
    raw_json_response = generator.generate_dca(compiled_prompt)

    try:
        payload = clean_and_parse_json(raw_json_response)
        manager.write_bundle_files(payload["dca"], payload["languages"])

        print("==================================================")
        print("[SUCCESS] All files and translations successfully synchronized autonomously!")
        print(f"[OUTPUT GENERATED AT] {export_dir}")
        print("==================================================")
    except Exception as e:
        print(f"[FATAL] System failed to stabilize JSON structure: {e}", file=sys.stderr)
        print(f"[RAW OUTPUT WAS]\n{raw_json_response}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
