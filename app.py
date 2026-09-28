"""Private local web UI: shows the project docs and lets you test the Ollama models.

Run with:
    python3 app.py

Binds to 127.0.0.1 only, so it is not reachable from other machines.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from flask import Flask, Response, jsonify, render_template_string, request

BASE_DIR = Path(__file__).resolve().parent
RUNS_DIR = BASE_DIR / "runs"
OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:3b"

# Only these project files may be viewed through the UI.
DOC_FILES = ["status.md", "spec.md", "guide.md", "plan.md", "TESTING.md", "README.md"]

app = Flask(__name__)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"(could not read file: {exc})"


def list_runs() -> list[str]:
    if not RUNS_DIR.is_dir():
        return []
    return sorted((p.name for p in RUNS_DIR.glob("*.txt")), reverse=True)


def list_models() -> list[str]:
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3) as resp:
            data = json.load(resp)
        models = [m["name"] for m in data.get("models", [])]
        if models:
            return models
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        pass
    return [DEFAULT_MODEL]


INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Local LLM Pilot &mdash; private dashboard</title>
  <style>
    body { font-family: -apple-system, system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #222; }
    h1 { font-size: 1.4rem; }
    section { margin-bottom: 2rem; }
    textarea { width: 100%; box-sizing: border-box; font-family: inherit; font-size: 1rem; padding: 0.5rem; }
    select, button { font-size: 1rem; padding: 0.4rem 0.7rem; }
    pre { background: #f5f5f5; padding: 1rem; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }
    ul { padding-left: 1.2rem; }
    a { color: #0b5cab; }
    .row { display: flex; gap: 0.5rem; align-items: center; margin: 0.5rem 0; }
    #status { color: #666; font-style: italic; }
    .badge { background: #eee; border-radius: 4px; padding: 0.1rem 0.5rem; font-size: 0.8rem; }
  </style>
</head>
<body>
  <h1>Local LLM Pilot <span class="badge">private &mdash; localhost only</span></h1>

  <section>
    <h2>Project docs</h2>
    <ul>
      {% for name in docs %}
        <li><a href="/view/{{ name }}">{{ name }}</a></li>
      {% endfor %}
    </ul>
  </section>

  <section>
    <h2>Try a prompt</h2>
    <div class="row">
      <label for="model">Model:</label>
      <select id="model">
        {% for m in models %}
          <option value="{{ m }}">{{ m }}</option>
        {% endfor %}
      </select>
    </div>
    <textarea id="prompt" rows="4" placeholder="Type a prompt to send to the local model..."></textarea>
    <div class="row">
      <button id="send">Run</button>
      <label><input type="checkbox" id="save"> save result to runs/</label>
      <span id="status"></span>
    </div>
    <pre id="output">(response will appear here)</pre>
  </section>

  <section>
    <h2>Saved runs</h2>
    <ul>
      {% for name in runs %}
        <li><a href="/runs/{{ name }}">{{ name }}</a></li>
      {% else %}
        <li>(no saved runs yet)</li>
      {% endfor %}
    </ul>
  </section>

  <script>
    const btn = document.getElementById("send");
    const out = document.getElementById("output");
    const status = document.getElementById("status");
    btn.addEventListener("click", async () => {
      const prompt = document.getElementById("prompt").value.trim();
      const model = document.getElementById("model").value;
      const save = document.getElementById("save").checked;
      if (!prompt) { return; }
      btn.disabled = true;
      status.textContent = "Running... (may take a while on CPU)";
      out.textContent = "";
      try {
        const res = await fetch("/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt, model, save })
        });
        const data = await res.json();
        if (!res.ok) {
          out.textContent = "Error: " + (data.error || res.statusText);
        } else {
          out.textContent = data.response;
          status.textContent = data.saved_as ? ("Saved as " + data.saved_as) : "";
        }
      } catch (err) {
        out.textContent = "Error: " + err;
      } finally {
        btn.disabled = false;
      }
    });
  </script>
</body>
</html>
"""

VIEW_HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>{{ name }}</title>
<style>body{font-family:-apple-system,system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;}
pre{background:#f5f5f5;padding:1rem;white-space:pre-wrap;word-wrap:break-word;}</style>
</head>
<body>
  <p><a href="/">&larr; back</a></p>
  <h1>{{ name }}</h1>
  <pre>{{ content }}</pre>
</body>
</html>
"""


@app.route("/")
def index() -> str:
    return render_template_string(
        INDEX_HTML, docs=DOC_FILES, models=list_models(), runs=list_runs()
    )


@app.route("/view/<name>")
def view_doc(name: str) -> str | tuple[str, int]:
    if name not in DOC_FILES:
        return "Not found", 404
    content = read_text(BASE_DIR / name)
    return render_template_string(VIEW_HTML, name=name, content=content)


@app.route("/runs/<name>")
def view_run(name: str) -> Response | tuple[str, int]:
    # Only allow simple filenames already known to exist in runs/, no path traversal.
    if not re.fullmatch(r"[\w.-]+\.txt", name) or name not in list_runs():
        return "Not found", 404
    content = read_text(RUNS_DIR / name)
    return render_template_string(VIEW_HTML, name=name, content=content)


@app.route("/generate", methods=["POST"])
def generate() -> tuple[Response, int] | Response:
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    model = (data.get("model") or DEFAULT_MODEL).strip()
    save = bool(data.get("save"))

    if not prompt:
        return jsonify(error="prompt is required"), 400

    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.load(resp)
    except urllib.error.URLError as exc:
        return jsonify(error=f"Ollama is not reachable ({exc}). Start it with: ollama serve"), 502
    except (TimeoutError, json.JSONDecodeError) as exc:
        return jsonify(error=f"Ollama request failed: {exc}"), 502

    response_text = result.get("response", "")

    saved_as = None
    if save:
        RUNS_DIR.mkdir(exist_ok=True)
        from datetime import datetime

        saved_as = f"{datetime.now():%Y-%m-%d-%H%M%S}-webui.txt"
        (RUNS_DIR / saved_as).write_text(
            f"Model: {model}\nPrompt: {prompt}\n\n{response_text}\n", encoding="utf-8"
        )

    return jsonify(response=response_text, saved_as=saved_as)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=False)
