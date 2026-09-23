# Local LLM Pilot Status

**Date:** 2026-09-23  
**Project:** `/Users/gp/huggingface/getting-started`  
**Status:** Pilot operational; ready for the Python client milestone

## Executive summary

The local LLM pilot is working on the older 8GB Intel MacBook Pro. Ollama runs the `qwen2.5:3b` model locally on the CPU, and the automated prompt script completes successfully. The basic installation and inference goals are complete.

The next recommended task is to add a small Python client that calls Ollama's local HTTP API. This will demonstrate how an application can use the model without compiling `llama-cpp-python`.

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

**Recommended decision:** proceed to the Python HTTP client milestone; do not spend more time on the `llama-cpp-python` build at this stage.

## Next milestone

Create `ollama_client.py` using only Python's standard library. It should:

- Accept a prompt from the command line.
- Send the prompt to `http://127.0.0.1:11434/api/generate`.
- Use `qwen2.5:3b` by default.
- Print the model response.
- Report a clear error when Ollama is not running.

Target usage:

```bash
python3 ollama_client.py "Explain recursion in plain English."
```

After that, compare the Python response with the equivalent `ollama run` command and record the result in `runs/`.
