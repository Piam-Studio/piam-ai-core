import sys
from llama_cpp import Llama
from piam_ai_core.config import ModelConfig
from piam_ai_core.prompts.contao_dca import CONTAO_DCA_SYSTEM_PROMPT


class PiamAiGenerator:
    """
    The orchestrator engine that interacts directly with the local GGUF model
    without utilizing any bloated external frameworks.
    """

    def __init__(self):
        self.config = ModelConfig()

        # Check if user forgot to download the model
        if not self.config.validate_environment():
            print(f"[ERROR] Model file not found at: {self.config.model_path}", file=sys.stderr)
            print("[INFO] Please place the .gguf model file inside the 'models/' directory.", file=sys.stderr)
            sys.exit(1)

        # Natively initialize the Llama engine with GPU offloading enabled
        self.llm = Llama(
            model_path=self.config.model_path,
            n_ctx=self.config.context_window,
            n_gpu_layers=self.config.gpu_layers,
            verbose=False
        )

    def generate_dca(self, raw_requirements: str) -> str:
        """
        Transforms user input into strict Contao DCA configuration code.
        """
        # Format the prompt using standard ChatML template (ideal for Qwen)
        formatted_prompt = (
            f"<|im_start|>system\n{CONTAO_DCA_SYSTEM_PROMPT}<|im_end|>\n"
            f"<|im_start|>user\nGenerate a Contao DCA for: {raw_requirements}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        response = self.llm(
            prompt=formatted_prompt,
            max_tokens=2048,
            temperature=self.config.temperature,
            stop=["<|im_end|>", "<|endoftext|>"]
        )

        return response["choices"][0]["text"].strip()
    