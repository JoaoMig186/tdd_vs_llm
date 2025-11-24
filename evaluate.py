import json

with open("validated_tdd.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total, fact_ok, coh_ok = 0, 0, 0

for group in data.values():
    for q, result in group.items():
        total += 1
        if result["factual"] is True:
            fact_ok += 1
        if result["coherent"] is True:
            coh_ok += 1

print(f"Taxa de acertos factuais: {fact_ok / total:.2%}")
print(f"Taxa de coerência textual: {coh_ok / total:.2%}")
