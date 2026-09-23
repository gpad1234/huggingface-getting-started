# Local LLM Pilot Guide for an 8GB MacBook Pro

This guide follows the low-hardware path described in the project README. The verified primary runtime is Ollama, using the locally downloaded `qwen2.5:3b` model. See `spec.md` for the complete installation record and troubleshooting details.

## Recommended approach

For an older 8GB MacBook Pro, the best choice is the GGUF/quantized model route rather than the full Transformers + PyTorch workflow. Ollama manages the model runtime and avoids compiling Python native bindings.

The README says the GGUF approach is better for consumer hardware and lower-memory setups. That matches this machine.

## Recommended model size

Use a small quantized model only:

- Best starting point: Qwen 2.5 3B Instruct Q4
- Also reasonable: Phi-3 Mini Q4 or Gemma 2B Q4
- Avoid 7B+ models for a first pilot on 8GB RAM

## Run with Ollama

```bash
ollama --version
ollama serve
```

Leave `ollama serve` running, open a second terminal, and run:

```bash
cd /Users/gp/huggingface/getting-started
ollama run qwen2.5:3b "Explain machine learning in one simple sentence."
```

The first run downloads approximately 1.9 GB. Later runs reuse the local model.

## Optional Python fallback

The following path is retained for experimentation only. On this machine, `llama-cpp-python` required a native build that did not complete.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install huggingface-hub llama-cpp-python
```

## Download a standalone GGUF file for the fallback

```bash
hf download Qwen/Qwen2.5-3B-Instruct-GGUF qwen2.5-3b-instruct-q4_k_m.gguf --local-dir .
```

This matches the README pattern of downloading a single GGUF file instead of a large repository.

## Minimal local inference script

Create a file called `pilot_llm.py`:

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./qwen2.5-3b-instruct-q4_k_m.gguf",
    n_ctx=2048,
)

response = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "Explain machine learning in one simple sentence."}
    ]
)

print(response["choices"][0]["message"]["content"])
```

Run it:

```bash
python pilot_llm.py
```

## Suggested pilot project scope

Keep the practice project small:

- 1 local model
- 1 Python script
- 3 to 5 prompt tests
- No fine-tuning
- No large model downloads
- Simple output check only

## Why this fits your machine

This setup is intentionally conservative:

- It follows the README’s GGUF recommendation
- It avoids the heavier full Transformers route
- It is realistic on an 8GB MacBook Pro
- It gives a practical local LLM experience without memory overload

## Good next step

Once the model runs successfully, try a few prompts such as:

```text
Explain recursion in plain English.
Summarize this paragraph.
Write a short Python function to check if a number is prime.
```

If needed, you can later upgrade to a larger model or switch to a more advanced app structure.
