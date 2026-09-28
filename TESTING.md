# Local LLM Pilot Testing Guide

This guide covers the Python client, the Ollama service, and the private Flask dashboard. Start with the quick checks; model inference is CPU-intensive and is only needed for the end-to-end checks.

## Before testing

Open a terminal in the project directory and activate the virtual environment:

```bash
cd /Users/gp/huggingface/getting-started
source .venv/bin/activate
```

Check the installed models and whether the local Ollama API is responding:

```bash
ollama list
curl -fsS http://127.0.0.1:11434/api/tags
```

If Ollama is stopped, start it in a separate terminal and leave it running:

```bash
ollama serve
```

## Quick checks

Compile the Python files and inspect the client options:

```bash
python -m py_compile app.py ollama_client.py
python ollama_client.py --help
```

Check that the default model and an explicitly selected model both answer a short prompt:

```bash
python ollama_client.py "Reply with only the word OK."
python ollama_client.py --model tinyllama:latest "Reply with only the word OK."
```

The first command should use `qwen2.5:3b`; the second should use `tinyllama:latest`. Both should print a response. The exact wording can vary.

## Error handling

With Ollama running, request a model name that is not installed:

```bash
python ollama_client.py --model no-such-model "test prompt"
```

Expected: a nonzero exit and a clear HTTP/model-not-found message, without a Python traceback.

To test the stopped-service message, stop Ollama in the terminal where `ollama serve` is running with `Ctrl+C`, then run:

```bash
python ollama_client.py "test prompt"
```

Expected: a nonzero exit, a message that Ollama is unreachable, and the suggestion to run `ollama serve`. Restart Ollama before continuing.

## Flask route smoke test

This lightweight check uses Flask's built-in test client and does not call Ollama or generate text:

```bash
python -c 'from app import app; c = app.test_client(); r = c.get("/"); assert r.status_code == 200; assert b"TESTING.md" in r.data; assert c.get("/view/TESTING.md").status_code == 200; assert c.get("/view/not-a-project-file").status_code == 404; r = c.post("/generate", json={"prompt": " "}); assert r.status_code == 400; print("Flask route checks passed")'
```

Expected: `Flask route checks passed`.

## End-to-end dashboard check

Start the dashboard in a terminal:

```bash
python app.py
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Verify the following:

1. The page loads and lists the project documents, including `TESTING.md`.
2. Open `TESTING.md` from the dashboard and confirm its contents appear.
3. Select an installed model, enter `Reply with only the word OK.`, and run it. The response should appear in the page.
4. Repeat with “save result to runs/” checked. Confirm a new `*-webui.txt` file appears under Saved runs and opens when clicked.
5. Submit an empty prompt. The page should not send a request or display a generated response.

Stop the dashboard with `Ctrl+C` when finished. It binds to `127.0.0.1` only.

## Saved prompt-session check

To run the existing three-prompt script and save a result under `runs/`:

```bash
./run_prompts.sh
```

To use the smaller model instead:

```bash
MODEL=tinyllama:latest ./run_prompts.sh
```

Confirm that the script prints a `Saved:` path and that the file contains responses for all three prompts. A run that stops before all responses are present is partial; retain it, but do not count it as a complete comparison.

## Reporting results

For a model comparison, use the same prompt text for both models and run prompts individually to avoid long batches. Record the model, exact prompt, response, and approximate wall-clock duration. Judge whether the response is accurate, complete, and relevant; do not treat a single run as a general model benchmark.