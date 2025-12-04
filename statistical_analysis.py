"""
Análise estatística para provar que TDD aumenta a precisão das respostas.
Inclui testes de significância estatística e métricas detalhadas.
"""
import json
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import pandas as pd

def load_data():
    """Carrega os dados de comparação."""
    with open("responses_raw.json", "r", encoding="utf-8") as f:
        raw_responses = json.load(f)
    
    with open("ground_truth.json", "r", encoding="utf-8") as f:
        truths = json.load(f)
    
    # Tenta carregar versão melhorada, senão usa a original
    try:
        with open("validated_tdd_improved.json", "r", encoding="utf-8") as f:
            tdd_validated = json.load(f)
    except FileNotFoundError:
        with open("validated_tdd.json", "r", encoding="utf-8") as f:
            tdd_validated = json.load(f)
    
    return raw_responses, truths, tdd_validated

def evaluate_baseline(raw_responses: Dict, truths: Dict) -> List[Tuple[bool, bool]]:
    """
    Avalia respostas brutas (baseline sem TDD).
    Retorna lista de tuplas (factual_correct, coherent).
    """
    results = []
    
    def factual_check(answer: str, truth: str) -> bool:
        if not truth:
            return None
        return truth.lower() in answer.lower()
    
    def coherence_check(answer: str) -> bool:
        import re
        sentences = re.split(r'[.!?]', answer)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) == 0:
            return False
        return all(len(s.split()) >= 3 for s in sentences)
    
    for group, questions in raw_responses.items():
        for question, answer in questions.items():
            truth = truths.get(question, "")
            factual = factual_check(answer, truth) if truth else None
            coherent = coherence_check(answer)
            results.append((factual, coherent))
    
    return results

def evaluate_tdd(tdd_validated: Dict) -> List[Tuple[bool, bool]]:
    """
    Avalia respostas processadas com TDD.
    Retorna lista de tuplas (factual_correct, coherent).
    """
    results = []
    
    for group in tdd_validated.values():
        for question, result in group.items():
            factual = result.get("factual")
            coherent = result.get("coherent", False)
            results.append((factual, coherent))
    
    return results

def calculate_metrics(results: List[Tuple[bool, bool]]) -> Dict:
    """Calcula métricas de precisão."""
    total = len(results)
    factual_correct = sum(1 for f, _ in results if f is True)
    factual_total = sum(1 for f, _ in results if f is not None)
    coherent_correct = sum(1 for _, c in results if c)
    
    return {
        "total": total,
        "factual_correct": factual_correct,
        "factual_total": factual_total,
        "factual_accuracy": factual_correct / factual_total if factual_total > 0 else 0,
        "coherent_correct": coherent_correct,
        "coherence_accuracy": coherent_correct / total if total > 0 else 0,
        "overall_correct": sum(1 for f, c in results if (f is True or f is None) and c),
        "overall_accuracy": sum(1 for f, c in results if (f is True or f is None) and c) / total if total > 0 else 0
    }

def statistical_significance_test(
    baseline_results: List[Tuple[bool, bool]],
    tdd_results: List[Tuple[bool, bool]],
    metric: str = "factual"
) -> Dict:
    """
    Testa significância estatística da diferença entre baseline e TDD.
    Usa teste binomial para proporções.
    """
    if metric == "factual":
        baseline_success = [1 if f is True else 0 for f, _ in baseline_results if f is not None]
        tdd_success = [1 if f is True else 0 for f, _ in tdd_results if f is not None]
    elif metric == "coherent":
        baseline_success = [1 if c else 0 for _, c in baseline_results]
        tdd_success = [1 if c else 0 for _, c in tdd_results]
    else:
        baseline_success = [1 if ((f is True or f is None) and c) else 0 for f, c in baseline_results]
        tdd_success = [1 if ((f is True or f is None) and c) else 0 for f, c in tdd_results]
    
    if len(baseline_success) == 0 or len(tdd_success) == 0:
        return {"error": "Dados insuficientes"}
    
    baseline_rate = np.mean(baseline_success)
    tdd_rate = np.mean(tdd_success)
    
    # Teste de proporções (z-test)
    n1, n2 = len(baseline_success), len(tdd_success)
    p1, p2 = baseline_rate, tdd_rate
    
    # Pooled proportion
    p_pool = (np.sum(baseline_success) + np.sum(tdd_success)) / (n1 + n2)
    
    # Standard error
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    
    # Z-score
    if se > 0:
        z_score = (p2 - p1) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # Two-tailed test
    else:
        z_score = 0
        p_value = 1.0
    
    # Efeito (diferença percentual)
    improvement = ((p2 - p1) / p1 * 100) if p1 > 0 else 0
    
    return {
        "baseline_rate": float(baseline_rate),
        "tdd_rate": float(tdd_rate),
        "improvement": float(improvement),
        "z_score": float(z_score),
        "p_value": float(p_value),
        "significant": bool(p_value < 0.05),
        "highly_significant": bool(p_value < 0.01)
    }

def generate_report():
    """Gera relatório completo de análise estatística."""
    print("\n" + "="*60)
    print("ANÁLISE ESTATÍSTICA: TDD vs BASELINE")
    print("="*60 + "\n")
    
    # Carrega dados
    raw_responses, truths, tdd_validated = load_data()
    
    # Avalia ambos os métodos
    baseline_results = evaluate_baseline(raw_responses, truths)
    tdd_results = evaluate_tdd(tdd_validated)
    
    # Calcula métricas
    baseline_metrics = calculate_metrics(baseline_results)
    tdd_metrics = calculate_metrics(tdd_results)
    
    # Exibe métricas
    print("MÉTRICAS DE PRECISÃO")
    print("-" * 60)
    print(f"\nBASELINE (sem TDD):")
    print(f"  Acurácia Factual:    {baseline_metrics['factual_accuracy']:.2%} ({baseline_metrics['factual_correct']}/{baseline_metrics['factual_total']})")
    print(f"  Acurácia Coerência:  {baseline_metrics['coherence_accuracy']:.2%} ({baseline_metrics['coherent_correct']}/{baseline_metrics['total']})")
    print(f"  Acurácia Geral:      {baseline_metrics['overall_accuracy']:.2%} ({baseline_metrics['overall_correct']}/{baseline_metrics['total']})")
    
    print(f"\nTDD (com refinamento):")
    print(f"  Acurácia Factual:    {tdd_metrics['factual_accuracy']:.2%} ({tdd_metrics['factual_correct']}/{tdd_metrics['factual_total']})")
    print(f"  Acurácia Coerência:  {tdd_metrics['coherence_accuracy']:.2%} ({tdd_metrics['coherent_correct']}/{tdd_metrics['total']})")
    print(f"  Acurácia Geral:      {tdd_metrics['overall_accuracy']:.2%} ({tdd_metrics['overall_correct']}/{tdd_metrics['total']})")
    
    # Melhoria
    factual_improvement = ((tdd_metrics['factual_accuracy'] - baseline_metrics['factual_accuracy']) / 
                          baseline_metrics['factual_accuracy'] * 100) if baseline_metrics['factual_accuracy'] > 0 else 0
    coherence_improvement = ((tdd_metrics['coherence_accuracy'] - baseline_metrics['coherence_accuracy']) / 
                            baseline_metrics['coherence_accuracy'] * 100) if baseline_metrics['coherence_accuracy'] > 0 else 0
    overall_improvement = ((tdd_metrics['overall_accuracy'] - baseline_metrics['overall_accuracy']) / 
                          baseline_metrics['overall_accuracy'] * 100) if baseline_metrics['overall_accuracy'] > 0 else 0
    
    print(f"\nMELHORIA COM TDD:")
    print(f"  Factual:    {factual_improvement:+.2f} pontos percentuais")
    print(f"  Coerência:  {coherence_improvement:+.2f} pontos percentuais")
    print(f"  Geral:      {overall_improvement:+.2f} pontos percentuais")
    
    # Testes de significância estatística
    print("\n" + "="*60)
    print("TESTES DE SIGNIFICÂNCIA ESTATÍSTICA")
    print("="*60 + "\n")
    
    for metric_name in ["factual", "coherent", "overall"]:
        test_result = statistical_significance_test(baseline_results, tdd_results, metric_name)
        
        if "error" in test_result:
            print(f"{metric_name.upper()}: {test_result['error']}")
            continue
        
        print(f"{metric_name.upper()}:")
        print(f"  Baseline: {test_result['baseline_rate']:.2%}")
        print(f"  TDD:      {test_result['tdd_rate']:.2%}")
        print(f"  Melhoria: {test_result['improvement']:+.2f}%")
        print(f"  Z-score:  {test_result['z_score']:.3f}")
        print(f"  p-value:  {test_result['p_value']:.4f}")
        
        if test_result['highly_significant']:
            print(f"  ✓ ALTAMENTE SIGNIFICATIVO (p < 0.01)")
        elif test_result['significant']:
            print(f"  ✓ SIGNIFICATIVO (p < 0.05)")
        else:
            print(f"  ✗ Não significativo (p >= 0.05)")
        print()
    
    # Salva relatório em JSON
    report = {
        "baseline_metrics": baseline_metrics,
        "tdd_metrics": tdd_metrics,
        "improvements": {
            "factual": factual_improvement,
            "coherence": coherence_improvement,
            "overall": overall_improvement
        },
        "statistical_tests": {
            "factual": statistical_significance_test(baseline_results, tdd_results, "factual"),
            "coherent": statistical_significance_test(baseline_results, tdd_results, "coherent"),
            "overall": statistical_significance_test(baseline_results, tdd_results, "overall")
        }
    }
    
    with open("statistical_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("="*60)
    print("Relatório completo salvo em statistical_report.json")
    print("="*60 + "\n")
    
    return report

if __name__ == "__main__":
    generate_report()

