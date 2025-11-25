import json
import re

def factual_check(answer, truth):
    return truth.lower() in answer.lower()

def coherence_check(answer):
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences) > 0 and all(len(s.split()) >= 3 for s in sentences)

with open("responses_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

with open("ground_truth.json", "r", encoding="utf-8") as f:
    truths = json.load(f)

with open("validated_tdd.json", "r", encoding="utf-8") as f:
    validated = json.load(f)

total = 0
fact_ok = 0
coh_ok = 0

for group, questions in raw.items():
    for q, answer in questions.items():
        total += 1
        truth = truths.get(q, "")
        if truth and factual_check(answer, truth):
            fact_ok += 1
        if coherence_check(answer):
            coh_ok += 1

baseline_factual = fact_ok / total * 100
baseline_coherent = coh_ok / total * 100

total_t = 0
fact_ok_t = 0
coh_ok_t = 0

for group in validated.values():
    for q, result in group.items():
        total_t += 1
        if result["factual"]:
            fact_ok_t += 1
        if result["coherent"]:
            coh_ok_t += 1

tdd_factual = fact_ok_t / total_t * 100
tdd_coherent = coh_ok_t / total_t * 100

print("\n===== COMPARAÇÃO =====\n")
print(f"SEM TDD - Acurácia factual: {baseline_factual:.2f}%")
print(f"SEM TDD - Coerência:        {baseline_coherent:.2f}%")
print()
print(f"COM TDD - Acurácia factual: {tdd_factual:.2f}%")
print(f"COM TDD - Coerência:        {tdd_coherent:.2f}%")
print("\n=======================\n")

comparison = {
    "baseline": {
        "factual": baseline_factual,
        "coherence": baseline_coherent
    },
    "tdd": {
        "factual": tdd_factual,
        "coherence": tdd_coherent
    }
}

with open("comparison.json", "w", encoding="utf-8") as f:
    json.dump(comparison, f, indent=2, ensure_ascii=False)