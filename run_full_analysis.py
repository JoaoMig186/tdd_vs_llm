"""
Script principal que executa todo o pipeline de análise.
Execute este script para gerar todas as análises e provas de que TDD ajuda.
"""
import subprocess
import sys
import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica se um arquivo existe."""
    if not Path(filepath).exists():
        print(f"❌ {description} não encontrado: {filepath}")
        return False
    print(f"✓ {description} encontrado")
    return True

def run_step(step_name, script_name, required_files=None):
    """Executa um passo do pipeline."""
    print(f"\n{'='*60}")
    print(f"PASSO: {step_name}")
    print(f"{'='*60}\n")
    
    if required_files:
        all_exist = True
        for file_info in required_files:
            if isinstance(file_info, tuple):
                filepath, description = file_info
            else:
                filepath, description = file_info, filepath
            if not check_file_exists(filepath, description):
                all_exist = False
        
        if not all_exist:
            print(f"\n⚠️  Arquivos necessários não encontrados. Pulando {step_name}.")
            return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False
        )
        print(f"\n✓ {step_name} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar {step_name}: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Script não encontrado: {script_name}")
        return False

def main():
    """Executa o pipeline completo."""
    print("\n" + "="*60)
    print("PIPELINE COMPLETO: PROVA DE EFICÁCIA DO TDD")
    print("="*60)
    
    steps = [
        {
            "name": "1. Gerar Respostas Baseline",
            "script": "generate_responses.py",
            "required_files": [
                ("prompts.json", "Arquivo de prompts"),
                ("ground_truth.json", "Arquivo de ground truth")
            ]
        },
        {
            "name": "2. Processar com TDD",
            "script": "pipeline_tdd_improved.py",
            "required_files": [
                ("responses_raw.json", "Respostas baseline"),
                ("ground_truth.json", "Arquivo de ground truth")
            ]
        },
        {
            "name": "3. Análise Estatística",
            "script": "statistical_analysis.py",
            "required_files": [
                ("responses_raw.json", "Respostas baseline"),
                ("ground_truth.json", "Arquivo de ground truth")
            ]
        },
        {
            "name": "4. Comparação Rápida",
            "script": "compare.py",
            "required_files": None  # Já deve existir após passo 3
        },
        {
            "name": "5. Gerar Visualizações",
            "script": "visualize_results.py",
            "required_files": [
                ("statistical_report.json", "Relatório estatístico")
            ]
        }
    ]
    
    results = []
    
    for step in steps:
        success = run_step(
            step["name"],
            step["script"],
            step.get("required_files")
        )
        results.append((step["name"], success))
        
        if not success and step["name"] == "1. Gerar Respostas Baseline":
            print("\n⚠️  Não é possível continuar sem as respostas baseline.")
            print("   Por favor, configure a API key e execute generate_responses.py manualmente.")
            break
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DO PIPELINE")
    print("="*60 + "\n")
    
    for step_name, success in results:
        status = "✓ Concluído" if success else "✗ Falhou/Pulado"
        print(f"{status}: {step_name}")
    
    successful_steps = sum(1 for _, success in results if success)
    total_steps = len(results)
    
    print(f"\n{'='*60}")
    print(f"Passos concluídos: {successful_steps}/{total_steps}")
    print("="*60)
    
    # Lista arquivos gerados
    generated_files = [
        "responses_raw.json",
        "validated_tdd_improved.json",
        "statistical_report.json",
        "comparison.json",
        "comparison_chart.png",
        "improvement_chart.png",
        "significance_chart.png",
        "report.html"
    ]
    
    print("\n📁 Arquivos gerados:")
    for file in generated_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (não gerado)")
    
    print("\n💡 Para ver o relatório completo, abra: report.html")
    print("💡 Para análise estatística detalhada, veja: statistical_report.json")
    print("\n")

if __name__ == "__main__":
    main()

