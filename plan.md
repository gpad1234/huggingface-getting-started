# Local LLM Pilot Plan

## Objective

Turn the successful Ollama installation into a small, repeatable practice project. The first project will be a prompt lab: run a few carefully chosen prompts against one local model, save the outputs, and compare response quality and speed.

The plan deliberately avoids fine-tuning, web applications, large models, and the unfinished Python native build until the basic workflow is understood.

## Current baseline

The following baseline is already complete:

- macOS 14.8.7 on Intel x86_64
- 8 GB RAM, CPU-only inference
- Ollama 0.30.10 installed and linked
- Ollama service tested on `127.0.0.1:11434`
- `qwen2.5:3b` installed locally, approximately 1.9 GB
- `tinyllama:latest` installed as a smaller backup, approximately 637 MB
- A simple inference prompt executed successfully
- Installation details recorded in `spec.md`

## Immediate next step: first prompt-lab session

### Goal

Run three prompts with `qwen2.5:3b` and save the responses in a dated text file. This establishes a repeatable experiment and gives us a useful baseline before writing more code.

### Run the session

Terminal 1, only if Ollama is not already running:

```bash
cd /Users/gp/huggingface/getting-started
ollama serve
```

Terminal 2:

```bash
cd /Users/gp/huggingface/getting-started
mkdir -p runs
run_file="runs/$(date +%Y-%m-%d-%H%M%S).txt"
printf 'Model: qwen2.5:3b\nDate: ' | tee "$run_file"
date | tee -a "$run_file"
printf '\nPrompt 1\n' | tee -a "$run_file"
ollama run qwen2.5:3b "Explain recursion in plain English in three sentences." | tee -a "$run_file"
printf '\nPrompt 2\n' | tee -a "$run_file"
ollama run qwen2.5:3b "Write a short Python function that checks whether a number is prime. Include one example." | tee -a "$run_file"
printf '\nPrompt 3\n' | tee -a "$run_file"
ollama run qwen2.5:3b "Summarize this sentence in one sentence: Local language models can run privately on consumer hardware when the model is small and quantized." | tee -a "$run_file"
```

Run each model command separately if the terminal inserts cursor-control characters into the saved output. The important result is that all three responses are present in the file; formatting can be cleaned later.

### Immediate success check

The session is successful if:

1. All three prompts return text.
2. The Python example is syntactically plausible.
3. The summary preserves the original meaning.
4. The Mac remains responsive during the run.
5. A file appears under `runs/`.

Review the saved run with:

```bash
ls -lh runs
sed -n '1,160p' runs/*.txt
```

## Phase 1: prompt practice

### Tasks

- Run the immediate three-prompt session.
- Add two prompts related to the book or guide being studied.
- Record which prompts produce useful, confusing, or incomplete answers.
- Repeat one prompt three times and note whether the wording changes.

### Deliverable

One or more timestamped files under `runs/` and a short note describing the best prompt and the weakest response.

### Completion criteria

- At least five prompts have been tested.
- Outputs are saved locally.
- The user can explain the difference between a prompt and a model response.

## Phase 2: make the workflow repeatable

### Tasks

- Add a small shell script, for example `run_prompts.sh`.
- Store prompts in a plain text or JSON file.
- Keep the model name configurable through an environment variable.
- Add a clear error when the Ollama service is unavailable.

### Suggested interface

```bash
MODEL=qwen2.5:3b ./run_prompts.sh prompts.txt
```

### Completion criteria

- One command runs the same prompt set.
- The output includes the model name and timestamp.
- The script works without Python dependencies.

## Phase 3: add a minimal Python client

Only begin this phase after Phases 1 and 2 work.

### Tasks

- Call the Ollama HTTP API at `http://127.0.0.1:11434/api/generate`.
- Use Python’s standard library first, avoiding extra packages.
- Send one prompt and print the returned response.
- Handle a stopped service and invalid model name clearly.

### Completion criteria

- `python3 ollama_client.py "your prompt"` returns model output.
- The script does not require `llama-cpp-python`.
- The CLI workflow and Python workflow produce comparable answers.

Milestone completed on 2026-09-25. `ollama_client.py` uses Python's standard library, defaults to `qwen2.5:3b`, supports `--model`, and reports unavailable-service and invalid-model errors. The same prompt returned `OK` through both the Python client and `ollama run`; the comparison is saved in `runs/2026-09-25-python-client-check.txt`.

## Phase 4: optional comparison

Compare `qwen2.5:3b` with `tinyllama:latest` on the same three prompts.

Record:

- Response relevance
- Response completeness
- Wall-clock completion time for each prompt, approximately
- Overall machine responsiveness
- Disk usage

Do not install a 7B+ model as part of this phase. The available-memory reading was low, and larger models may cause swapping or make the computer unpleasant to use.

Phase completed on 2026-09-25. Each of the three prompts was sent individually to both models. Single-run wall-clock times and qualitative observations are recorded in `runs/2026-09-25-model-comparison-timed.txt`. Qwen was more reliable on these examples, but not consistently faster. Perceived machine responsiveness was not formally measured; these results are not a general benchmark.

## Explicitly deferred work

These items are outside the next step:

- Full Transformers and PyTorch setup
- Fine-tuning or LoRA training
- 7B+ model testing
- Web UI development
- Cloud API integration
- Continuing the `llama-cpp-python` native build

They may become reasonable later, but they would add complexity before the basic local inference workflow is understood.

## Recommended order of work

1. Run the three-prompt session and save the output. (Complete)
2. Review the saved output and record observations. (Complete)
3. Create the repeatable shell script. (Complete)
4. Add the standard-library Python HTTP client and compare it with `ollama run`. (Complete)
5. Compare the two installed models. (Complete; limited single-run comparison)
6. Decide whether a larger project is justified.

## Definition of done for the next milestone

The next milestone is complete when the repository contains:

- `spec.md` with the verified environment
- `guide.md` with the Ollama run instructions
- `plan.md` with this roadmap
- `runs/` containing at least one saved three-prompt session
- A short written observation about response quality and machine performance
