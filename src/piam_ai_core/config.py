import os
from pydantic import BaseModel

class ModelConfig(BaseModel):
    """
    Configuration settings for the local LLM execution.
    Ensures that parameters are type-safe and validated.
    """
    # This automatically finds the model inside your local 'models' directory
    model_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/qwen2.5-coder-7b-instruct-q4_k_m.gguf"))
    context_window: int = 4096
    gpu_layers: int = 0  # 0 means: run entirely on the Intel CPU using your 32 GB RAM
    temperature: float = 0.1  # Low temperature makes the AI logical and precise (perfect for code)

    def validate_environment(self) -> bool:
        """
        Checks if the configured model file exists locally.
        """
        return os.path.exists(self.model_path)