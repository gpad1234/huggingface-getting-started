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
