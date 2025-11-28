
import google.generativeai as genai
import json
import time

genai.configure(api_key="SUA_CHAVE_GEMINI")
model = genai.GenerativeModel("gemini-2.0-flash")

with open("prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

responses = {}

for group, qs in prompts.items():
    responses[group] = {}
    for q in qs:
        output = model.generate_content(q)
        responses[group][q] = output.text
        time.sleep(5) 

with open("responses_raw.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, indent=2, ensure_ascii=False)