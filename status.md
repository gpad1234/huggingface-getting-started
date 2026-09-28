# Local LLM Pilot Status

**Date:** 2026-09-25
**Project:** `/Users/gp/huggingface/getting-started`  
**Status:** Pilot operational; Python HTTP client and initial model comparison complete

## Executive summary

The local LLM pilot is working on the older 8GB Intel MacBook Pro. Ollama runs the `qwen2.5:3b` model locally on the CPU, and the automated prompt script completes successfully. The standard-library Python HTTP client also returns responses from Ollama and handles unavailable-service and invalid-model errors.

The Python client and direct `ollama run` workflow returned the same response for the same prompt. Both installed models have now been compared on the same three prompts with individual CPU runs and approximate wall-clock timings. Qwen was more reliable on these examples, although much slower on the prime-checker prompt. Treat the results as anecdotal rather than a general benchmark.

## Completed

- Reviewed `README.md` and selected the GGUF/quantized model approach.
- Selected Ollama as the primary runtime for this machine.
- Installed and linked Ollama through Homebrew.
- Verified Ollama version `0.30.10`.
- Started and tested the Ollama service at `127.0.0.1:11434`.
- Downloaded and tested `qwen2.5:3b`, approximately 1.9 GB.
- Confirmed `tinyllama:latest`, approximately 637 MB, is also available.
- Ran the original one-sentence machine-learning test successfully.
- Ran the three-prompt practice session successfully.
- Added `run_prompts.sh` to automate the three-prompt session.
- Added `ollama_client.py`, a standard-library CLI for Ollama's local HTTP API.
- Compared the Python client with `ollama run`; both returned `OK` for the same prompt.
- Verified `--model` with both installed models and saved a one-prompt comparison; Qwen's response was more accurate for the recursion prompt.
- Completed the matched three-prompt comparison with both models and recorded approximate wall-clock timings and response-quality observations.
- Saved prompt results under `runs/`.
- Documented the environment in `spec.md`.
- Documented the main and fallback workflows in `guide.md`.
- Documented the staged roadmap in `plan.md`.

## Verified commands

### Check Ollama

```bash
ollama --version
ollama list
```

Verified results:

```text
ollama version is 0.30.10
qwen2.5:3b       1.9 GB
 tinyllama:latest 637 MB
```

### Run the automated prompt test

```bash
cd /Users/gp/huggingface/getting-started
./run_prompts.sh
```

Latest verification: exit code `0`.

The script creates a timestamped output file in `runs/` and runs three prompts:

1. Explain recursion.
2. Write a Python prime-number checker.
3. Summarize a sentence about local quantized models.

### Use the smaller model

```bash
MODEL=tinyllama:latest ./run_prompts.sh
```

## Environment

| Component | Current state |
| --- | --- |
| Operating system | macOS 14.8.7 |
| Architecture | Intel x86_64 |
| Memory | 8 GB RAM |
| Inference | CPU-only |
| Python | 3.12.7 |
| Homebrew | 7.0.6 |
| Ollama | 0.30.10 |
| Primary model | `qwen2.5:3b` |
| Backup model | `tinyllama:latest` |

## Current project files

| File or directory | Purpose |
| --- | --- |
| `README.md` | Original Hugging Face and local LLM reference material |
| `spec.md` | Detailed installed-environment specification |
| `guide.md` | Practical setup and run guide |
| `plan.md` | Multi-phase next-step plan |
| `run_prompts.sh` | Automated three-prompt test script |
| `ollama_client.py` | Standard-library CLI for the local Ollama API |
| `pilot_llm.py` | Experimental Python GGUF client using `llama-cpp` |
| `requirements.txt` | Python fallback dependencies |
| `qwen2.5-3b-instruct-q4_k_m.gguf` | Standalone 2.0 GB GGUF fallback file |
| `runs/` | Saved prompt-session outputs |

## Known limitations

- The verified Ollama installation is version `0.30.10`; the attempted upgrade to `0.34.2` was interrupted during an unsupported Homebrew dependency build.
- Inference is CPU-only and should remain limited to small models and short prompts.
- `llama-cpp-python` was not installed successfully because it requires a native build on this machine.
- The Python GGUF route is therefore an optional experiment, not part of the working pilot.
- The standalone GGUF file duplicates model storage and can be removed if the Python fallback is abandoned.

## Review decision

The pilot meets its current acceptance criteria:

- Ollama is installed.
- The service starts locally.
- A small model is available.
- Inference returns coherent responses.
- The automated test runs successfully.
- Results are saved for review.

**Recommended decision:** keep `qwen2.5:3b` as the primary model for this pilot based on these examples; do not spend more time on the `llama-cpp-python` build at this stage.

## Next milestone

The initial comparison is complete. The individual paired outputs, wall-clock times, and limitations are recorded in `runs/2026-09-25-model-comparison-timed.txt`. Perceived machine responsiveness was not formally measured. A useful next activity is to run selected generated code through automated checks, or choose another small project task; continue avoiding larger model downloads on this 8 GB CPU-only machine.

## Private web UI

Added `app.py`, a small Flask app for local, private use only (binds to `127.0.0.1`):

- Dashboard listing project docs (`README.md`, `spec.md`, `guide.md`, `plan.md`, `status.md`) and saved runs.
- A prompt box to test any installed Ollama model directly from the browser, with an option to save the result under `runs/`.

Run it with:

```bash
cd /Users/gp/huggingface/getting-started
.venv/bin/python app.py
```

Then open `http://127.0.0.1:3000` in a browser. It is not exposed beyond localhost.
