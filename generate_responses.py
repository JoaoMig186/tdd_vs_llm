
from transformers import pipeline
import json

generator = pipeline("text-generation", model="distilgpt2")

with open("prompts.json") as f:
    prompts = json.load(f)

responses = {}

for group, qs in prompts.items():
    responses[group] = {}
    for q in qs:
        output = generator(q, max_length=50, num_return_sequences=1)
        responses[group][q] = output[0]['generated_text']

with open("responses_raw.json", "w") as f:
    json.dump(responses, f, indent=2, ensure_ascii=False)
