"""Send a prompt to the local Ollama API."""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"


def generate(prompt: str, model: str) -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.load(response)
    return result["response"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt a locally running Ollama model.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"model name (default: {DEFAULT_MODEL})")
    parser.add_argument("prompt", nargs="+", help="prompt text")
    args = parser.parse_args()

    try:
        print(generate(" ".join(args.prompt), args.model))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        print(f"Ollama returned HTTP {exc.code}: {detail or exc.reason}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(
            f"Could not reach Ollama at http://127.0.0.1:11434 ({exc}). Start it with: ollama serve",
            file=sys.stderr,
        )
        return 1
    except (KeyError, json.JSONDecodeError) as exc:
        print(f"Ollama returned an invalid response: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())