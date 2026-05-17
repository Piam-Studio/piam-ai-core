# Piam AI-Core

A private, fully self-hosted, and sovereign AI orchestration engine designed to automate Contao CMS and Symfony architecture workflows for Piam Studio. 

This system runs 100% locally on dedicated hardware, ensuring absolute data privacy and GDPR compliance for all client requirements.

## System Architecture

The project is built using native Python and leverages the `llama.cpp` ecosystem to interact directly with quantized GGUF open-source models without any external cloud dependencies.

- **LLM Engine:** `llama-cpp-python` (optimized for CPU execution)
- **Base Model:** Qwen-2.5-Coder-7B-Instruct (Q4_K_M GGUF format)
- **Context Window:** 4096 tokens
- **Target Output:** Valid, structured PHP code for Contao Data Container Allocations (DCA)

## Local Installation & Setup

### Prerequisites
- macOS or Linux
- Python 3.10 or newer (Recommended: Python 3.11+)
- At least 16 GB RAM (32 GB highly recommended for 7B/14B models)

### Installation Steps
- Initialize the Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate
```
- Install Dependencies (CPU-optimized for Intel Macs):
```
pip install --upgrade pip
pip install -e .
```
- Download the AI Model:
  - Download the `qwen2.5-coder-7b-instruct-q4_k_m.gguf` file from Hugging Face. 
  - Place the file inside the local models/ directory.

### Verifying the Integration (Test Run)
```
python test_run.py
```

## Project Layout

```text
piam-ai-core/
├── models/             # Storage for local GGUF model files (git-ignored)
└── src/
    └── piam_ai_core/
        ├── config.py   # Hardware and LLM generation configurations
        ├── generator.py# Core inference engine interacting with the LLM
        └── prompts/    # Immutable architecture-specific system prompts
```

> (c) 2026 Piam Studio. All documentation is strictly maintained in English.

