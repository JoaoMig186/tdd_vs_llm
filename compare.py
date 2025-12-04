"""
Script de comparação melhorado que usa análise estatística.
Para uma análise completa, execute: python statistical_analysis.py
"""
import json
import re

def factual_check(answer, truth):
    if not truth:
        return None
    return truth.lower() in answer.lower()

def coherence_check(answer):
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences) > 0 and all(len(s.split()) >= 3 for s in sentences)

# Tenta carregar versão melhorada, senão usa a original
try:
    tdd_file = "validated_tdd_improved.json"
    with open(tdd_file, "r", encoding="utf-8") as f:
        validated = json.load(f)
    print(f"Usando: {tdd_file}")
except FileNotFoundError:
    tdd_file = "validated_tdd.json"
    with open(tdd_file, "r", encoding="utf-8") as f:
        validated = json.load(f)
    print(f"Usando: {tdd_file} (versão melhorada não encontrada)")

with open("responses_raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

with open("ground_truth.json", "r", encoding="utf-8") as f:
    truths = json.load(f)

total = 0
fact_ok = 0
fact_total = 0
coh_ok = 0

for group, questions in raw.items():
    for q, answer in questions.items():
        total += 1
        truth = truths.get(q, "")
        if truth:
            fact_total += 1
            if factual_check(answer, truth):
                fact_ok += 1
        if coherence_check(answer):
            coh_ok += 1

baseline_factual = (fact_ok / fact_total * 100) if fact_total > 0 else 0
baseline_coherent = (coh_ok / total * 100) if total > 0 else 0

total_t = 0
fact_ok_t = 0
fact_total_t = 0
coh_ok_t = 0

for group in validated.values():
    for q, result in group.items():
        total_t += 1
        factual = result.get("factual")
        if factual is not None:
            fact_total_t += 1
            if factual:
                fact_ok_t += 1
        if result.get("coherent", False):
            coh_ok_t += 1

tdd_factual = (fact_ok_t / fact_total_t * 100) if fact_total_t > 0 else 0
tdd_coherent = (coh_ok_t / total_t * 100) if total_t > 0 else 0

factual_improvement = tdd_factual - baseline_factual
coherence_improvement = tdd_coherent - baseline_coherent

print("\n" + "="*60)
print("COMPARAÇÃO: BASELINE vs TDD")
print("="*60 + "\n")
print(f"SEM TDD (Baseline):")
print(f"  Acurácia factual:    {baseline_factual:.2f}% ({fact_ok}/{fact_total})")
print(f"  Coerência:           {baseline_coherent:.2f}% ({coh_ok}/{total})")
print()
print(f"COM TDD:")
print(f"  Acurácia factual:    {tdd_factual:.2f}% ({fact_ok_t}/{fact_total_t})")
print(f"  Coerência:           {tdd_coherent:.2f}% ({coh_ok_t}/{total_t})")
print()
print(f"MELHORIA:")
print(f"  Factual:             {factual_improvement:+.2f} pontos percentuais")
print(f"  Coerência:           {coherence_improvement:+.2f} pontos percentuais")
print("\n" + "="*60)
print("\n💡 Para análise estatística completa, execute:")
print("   python statistical_analysis.py")
print("\n💡 Para visualizações, execute:")
print("   python visualize_results.py")
print("="*60 + "\n")

comparison = {
    "baseline": {
        "factual": baseline_factual,
        "coherence": baseline_coherent,
        "factual_count": f"{fact_ok}/{fact_total}",
        "coherence_count": f"{coh_ok}/{total}"
    },
    "tdd": {
        "factual": tdd_factual,
        "coherence": tdd_coherent,
        "factual_count": f"{fact_ok_t}/{fact_total_t}",
        "coherence_count": f"{coh_ok_t}/{total_t}"
    },
    "improvements": {
        "factual": factual_improvement,
        "coherence": coherence_improvement
    }
}

with open("comparison.json", "w", encoding="utf-8") as f:
    json.dump(comparison, f, indent=2, ensure_ascii=False)