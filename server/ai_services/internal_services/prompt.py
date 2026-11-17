import ollama
import json

LOW_MODEL = 'qwen3:0.6b'
HIGH_MODEL = 'deepseek-r1:1.5b'

MODELS = {
    'low': LOW_MODEL,
    'high': HIGH_MODEL,
}

def ask(prompt: str, model_strength: str, system_prompt: str, format: dict) -> dict:

    model = MODELS[model_strength.lower()]

    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],

    format=format,
    think=False,
    )

    return json.loads(response.message.content) # type: ignore