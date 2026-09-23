#!/bin/zsh

set -e

model="${MODEL:-qwen2.5:3b}"
run_file="runs/$(date +%Y-%m-%d-%H%M%S).txt"

if ! command -v ollama >/dev/null 2>&1; then
  print -u2 "Error: ollama is not installed or is not on PATH."
  exit 1
fi

if ! curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  print -u2 "Error: Ollama is not running. Start it with: ollama serve"
  exit 1
fi

mkdir -p runs
{
  print "Model: $model"
  print -n "Date: "
  date
  print ""
  print "Prompt 1"
  ollama run "$model" "Explain recursion in plain English in three sentences."
  print ""
  print "Prompt 2"
  ollama run "$model" "Write a short Python function that checks whether a number is prime. Include one example."
  print ""
  print "Prompt 3"
  ollama run "$model" "Summarize this sentence in one sentence: Local language models can run privately on consumer hardware when the model is small and quantized."
} > "$run_file"

print "Saved: $run_file"
cat "$run_file"
