# Local LLM Pilot Specification

## 1. Purpose

This project is a small local language-model pilot based on the GGUF/quantized-model guidance in `README.md`. Its purpose is to practise downloading, starting, and prompting a local model on an older 8GB MacBook Pro.

The verified runtime path is Ollama. The Python `llama-cpp-python` path remains in the repository as an experimental fallback, but it is not the active or required path.

## 2. Verified machine

| Item | Verified value |
| --- | --- |
| Operating system | macOS 14.8.7 |
| CPU architecture | Intel x86_64 |
| Memory | 8 GB total; Ollama reported approximately 1.7 GB available during startup |
| Python | 3.12.7 |
| Homebrew | 7.0.6 |
| Ollama | 0.30.10 |
| Inference hardware | CPU; no usable GPU/VRAM was detected |
| Project directory | `/Users/gp/huggingface/getting-started` |

## 3. Installed and verified components

### Ollama

Ollama is installed through Homebrew and linked at `/usr/local/bin/ollama`. Its local service listens on `127.0.0.1:11434`.

Verify it with:

```bash
ollama --version
```

Expected result:

```text
ollama version is 0.30.10
```

The attempted Homebrew upgrade to 0.34.2 was not completed because this macOS/Homebrew configuration is unsupported for some binary bottles and the `lz4` dependency was terminated while compiling. The existing 0.30.10 installation is usable and passed inference tests.

### Local Ollama models

The following models are currently present:

| Model | Approximate size | Intended use |
| --- | ---: | --- |
| `qwen2.5:3b` | 1.9 GB | Primary pilot model |
| `tinyllama:latest` | 637 MB | Smaller backup/test model |

List installed models with:

```bash
ollama list
```

### Hugging Face download tooling

The `huggingface-hub` Python package is installed for downloading model files. The current CLI command is `hf`; `huggingface-cli` is deprecated.

The standalone GGUF file below was successfully downloaded:

```text
qwen2.5-3b-instruct-q4_k_m.gguf
```

It is approximately 2.0 GB and is used only by the Python fallback script. Ollama uses its own model storage under `~/.ollama/models` and does not need this file for the verified Ollama workflow.

### Python fallback files

- `pilot_llm.py` contains a `llama_cpp` inference example.
- `requirements.txt` lists `huggingface-hub` and `llama-cpp-python`.
- `huggingface-hub` installed successfully.
- `llama-cpp-python` was not successfully installed because pip attempted a local native build and the build was cancelled/terminated repeatedly.

Do not run `pip install -r requirements.txt` as part of the primary pilot setup unless you specifically want to continue troubleshooting the Python native build.

## 4. Primary run procedure

Open a terminal and move to the project directory:

```bash
cd /Users/gp/huggingface/getting-started
```

Start the Ollama service if it is not already running:

```bash
ollama serve
```

Leave that terminal open. In a second terminal, run the pilot prompt:

```bash
cd /Users/gp/huggingface/getting-started
ollama run qwen2.5:3b "Explain machine learning in one simple sentence."
```

The first run downloads the model if it is missing. Later runs reuse the local copy.

A successful response looks like:

```text
Machine learning is a method where computers learn from data to improve
performance without being explicitly programmed.
```

The command was run successfully more than once with exit code 0.

## 5. Additional practice prompts

```bash
ollama run qwen2.5:3b "Explain recursion in plain English."
ollama run qwen2.5:3b "Summarize this paragraph in three bullet points: ..."
ollama run qwen2.5:3b "Write a short Python function that checks whether a number is prime."
```

Use short prompts and modest outputs on this machine. Avoid large context windows, parallel model requests, fine-tuning, and 7B+ models during this pilot.

## 6. Operational commands

Check that the service responds:

```bash
curl http://127.0.0.1:11434/api/tags
```

Stop an interactive model session with `Ctrl+C`. Stop a manually started server with `Ctrl+C` in the terminal running `ollama serve`.

Optionally configure Ollama to start as a background service:

```bash
brew services start ollama
```

Check the service status:

```bash
brew services list | grep ollama
```

## 7. Storage and cleanup

Ollama models are stored under:

```text
~/.ollama/models
```

Remove a model only when its disk space is no longer needed:

```bash
ollama rm tinyllama:latest
```

The separately downloaded GGUF file can be removed only if the Python fallback is no longer wanted:

```bash
rm ./qwen2.5-3b-instruct-q4_k_m.gguf
```

That file is not required to run `ollama run qwen2.5:3b`.

## 8. Pilot acceptance criteria

The pilot is considered complete when all of the following are true:

1. `ollama --version` returns a version.
2. `ollama list` shows `qwen2.5:3b`.
3. `ollama run qwen2.5:3b "Explain machine learning in one simple sentence."` exits successfully.
4. The response is coherent and relevant.
5. The machine remains responsive enough for short prompt tests.

All five criteria have been met for the current setup.

## 9. Python HTTP client and recent validation

On 2026-09-25, `ollama_client.py` was added as a Python standard-library CLI for Ollama's local HTTP API. It posts a non-streaming request to `http://127.0.0.1:11434/api/generate`, defaults to `qwen2.5:3b`, accepts `--model` to select another installed model, and reports connection, HTTP, and invalid-response errors without a traceback.

Run it with the project virtual environment or another Python 3 installation:

```bash
.venv/bin/python ollama_client.py "Explain recursion in plain English."
.venv/bin/python ollama_client.py --model tinyllama:latest "Explain recursion in plain English."
```

The project virtual environment uses Python 3.12.7. The client itself requires no third-party Python packages. Ollama must be running first; start it with `ollama serve` if needed.

### Client checks performed

- Ran `python -m py_compile ollama_client.py` successfully and confirmed the CLI options with `--help`.
- With Ollama stopped, the client reported that the service was unreachable and suggested `ollama serve`.
- Started Ollama on `127.0.0.1:11434`; a short prompt returned `OK` through the client.
- Ran the same prompt through `ollama run qwen2.5:3b`; it also returned `OK`.
- Selected a nonexistent model; Ollama returned HTTP 404 and the client displayed the model-not-found response without a traceback.
- Workspace diagnostics reported no errors in the client or the updated project documentation.

The matching client/direct-CLI check is recorded in `runs/2026-09-25-python-client-check.txt`.

### Model comparison status

The three-prompt comparison was completed by sending each prompt individually to both models through the Python client. The matched prompts cover recursion, a prime-checking function, and summarization. One `/usr/bin/time -p` wall-clock measurement was recorded for each model/prompt pair; these are single-run CPU timings, not a formal benchmark or time-to-first-token measurements. Full observations are in `runs/2026-09-25-model-comparison-timed.txt`.

Qwen was clearer and more faithful on the recursion and summary prompts. For code generation, Qwen produced a working integer prime checker but included an unnecessary check and explanation error; TinyLlama's code had a variable-name mismatch and could reference an undefined variable. Qwen was slower for the prime-checker prompt (132.60 s versus 37.12 s), but faster on summarization (11.05 s versus 14.46 s); recursion took 13.47 s versus 15.48 s. Perceived machine responsiveness was not formally measured. The earlier incomplete batch remains preserved and labeled partial in `runs/2026-09-25-155309.txt`.
