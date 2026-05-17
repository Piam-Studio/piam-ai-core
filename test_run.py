# test_run.py
import sys
import time
from src.piam_ai_core.generator import PiamAiGenerator


def main():
    print("==================================================")
    print("     PIAM AI-CORE - INITIAL INTEGRATION TEST      ")
    print("==================================================")
    print("[INFO] Initializing engine and loading GGUF model into RAM...")

    start_time = time.time()

    try:
        # Initialize our custom generator architecture
        generator = PiamAiGenerator()
        init_duration = time.time() - start_time
        print(f"[SUCCESS] Model loaded successfully in {init_duration:.2f} seconds.")

    except Exception as e:
        print(f"[FATAL] Failed to initialize PiamAiGenerator: {e}", file=sys.stderr)
        sys.exit(1)

    # Simple testing requirement for Contao
    test_requirement = "Ein Inhaltselement für eine Textbox mit Überschrift und Fließtext."

    print("\n[INFO] Sending test requirement to local LLM...")
    print(f"Requirement: \"{test_requirement}\"")
    print("[INFO] Processing (Running on Intel i9 CPU)... Please wait.\n")

    generation_start = time.time()

    # Execute the local inference loop
    generated_php = generator.generate_dca(test_requirement)

    generation_duration = time.time() - generation_start

    print("==================================================")
    print("            GENERATED PHP CODE OUTPUT             ")
    print("==================================================")
    print(generated_php)
    print("==================================================")
    print(f"[SUCCESS] Process completed in {generation_duration:.2f} seconds.")
    print("==================================================")


if __name__ == "__main__":
    main()
    