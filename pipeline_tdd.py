
import json
import re

def factual_check(answer, truth):
    return truth.lower() in answer.lower()

def coherence_check(answer):
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences) > 0 and all(len(s.split()) >= 3 for s in sentences)

with open("responses_raw.json") as f:
    responses = json.load(f)
with open("ground_truth.json") as f:
    truths = json.load(f)

validated = {}

for group, qs in responses.items():
    validated[group] = {}
    for q, ans in qs.items():
        truth = truths.get(q, "")
        factual = factual_check(ans, truth) if truth else None
        coherent = coherence_check(ans)
        validated[group][q] = {
            "answer": ans,
            "factual": factual,
            "coherent": coherent
        }

with open("validated_tdd.json", "w") as f:
    json.dump(validated, f, indent=2, ensure_ascii=False)
