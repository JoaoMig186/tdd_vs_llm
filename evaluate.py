
import json

with open("validated_tdd.json") as f:
    data = json.load(f)

total, fact_ok, coh_ok = 0, 0, 0

for group in data.values():
    for q, result in group.items():
        total += 1
        if result["factual"]:
            fact_ok += 1
        if result["coherent"]:
            coh_ok += 1

print(f"Taxa de acertos factuais: {fact_ok / total:.2%}")
print(f"Taxa de coerência textual: {coh_ok / total:.2%}")
