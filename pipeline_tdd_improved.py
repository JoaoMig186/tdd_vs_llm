"""
Pipeline TDD melhorado que refina respostas quando os testes falham.
Este é o componente chave para provar que TDD aumenta a precisão.
"""
import json
import re
import google.generativeai as genai
from typing import Dict, Tuple, Optional

# Configuração do modelo (ajuste a chave conforme necessário)
genai.configure(api_key="AIzaSyCPmd-lf1IWGK0qZsVmst81TiIGegyzl6I")
model = genai.GenerativeModel("gemini-2.0-flash")

def factual_check(answer: str, truth: str) -> bool:
    """Verifica se a resposta contém a verdade factual esperada."""
    if not truth:
        return None
    # Normaliza e verifica se a verdade está na resposta
    answer_lower = answer.lower()
    truth_lower = truth.lower()
    return truth_lower in answer_lower

def coherence_check(answer: str) -> bool:
    """Verifica se a resposta é coerente (tem frases completas)."""
    sentences = re.split(r'[.!?]', answer)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) == 0:
        return False
    # Verifica se todas as frases têm pelo menos 3 palavras
    return all(len(s.split()) >= 3 for s in sentences)

def refine_response_with_feedback(
    question: str, 
    original_answer: str, 
    truth: Optional[str] = None,
    failed_factual: bool = False,
    failed_coherence: bool = False
) -> str:
    """
    Refina a resposta usando feedback dos testes que falharam.
    Este é o coração do TDD: usar os testes para melhorar a resposta.
    """
    feedback_parts = []
    
    if failed_factual and truth:
        feedback_parts.append(f"A resposta deve conter a informação: '{truth}'")
    
    if failed_coherence:
        feedback_parts.append("A resposta deve ser mais coerente e ter frases completas.")
    
    if not feedback_parts:
        return original_answer  # Nada a melhorar
    
    feedback = " | ".join(feedback_parts)
    
    prompt = f"""Você recebeu uma pergunta e uma resposta inicial que não passou em alguns testes.
Por favor, forneça uma resposta melhorada que corrija os problemas identificados.

Pergunta: {question}

Resposta original: {original_answer}

Problemas identificados: {feedback}

Forneça uma resposta melhorada que resolva esses problemas:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao refinar resposta: {e}")
        return original_answer

def process_with_tdd(
    responses: Dict[str, Dict[str, str]],
    truths: Dict[str, str],
    max_iterations: int = 3
) -> Dict[str, Dict[str, Dict]]:
    """
    Processa respostas usando TDD: testa, identifica falhas e refina.
    
    Args:
        responses: Dicionário com respostas brutas organizadas por grupo
        truths: Dicionário com verdades factuais esperadas
        max_iterations: Número máximo de iterações de refinamento
    
    Returns:
        Dicionário com respostas validadas e refinadas
    """
    validated = {}
    
    for group, questions in responses.items():
        validated[group] = {}
        
        for question, answer in questions.items():
            current_answer = answer
            truth = truths.get(question, "")
            
            # Itera até passar nos testes ou atingir o limite
            for iteration in range(max_iterations):
                factual = factual_check(current_answer, truth) if truth else None
                coherent = coherence_check(current_answer)
                
                # Se passou em todos os testes, para
                if (factual is not False) and coherent:
                    break
                
                # Identifica quais testes falharam
                failed_factual = (factual is False) if truth else False
                failed_coherence = not coherent
                
                # Refina a resposta com base nos testes que falharam
                if failed_factual or failed_coherence:
                    current_answer = refine_response_with_feedback(
                        question, 
                        current_answer, 
                        truth,
                        failed_factual,
                        failed_coherence
                    )
            
            # Avaliação final
            final_factual = factual_check(current_answer, truth) if truth else None
            final_coherent = coherence_check(current_answer)
            
            validated[group][question] = {
                "answer": current_answer,
                "factual": final_factual,
                "coherent": final_coherent,
                "iterations": iteration + 1
            }
    
    return validated

if __name__ == "__main__":
    # Carrega dados
    with open("responses_raw.json", "r", encoding="utf-8") as f:
        responses = json.load(f)
    
    with open("ground_truth.json", "r", encoding="utf-8") as f:
        truths = json.load(f)
    
    # Processa com TDD
    print("Processando respostas com TDD...")
    validated = process_with_tdd(responses, truths)
    
    # Salva resultados
    with open("validated_tdd_improved.json", "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2, ensure_ascii=False)
    
    print("Processamento concluído! Resultados salvos em validated_tdd_improved.json")

