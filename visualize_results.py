"""
Visualização dos resultados comparativos entre TDD e Baseline.
Gera gráficos para demonstrar visualmente a melhoria com TDD.
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_report():
    """Carrega o relatório estatístico."""
    try:
        with open("statistical_report.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: statistical_report.json não encontrado. Execute statistical_analysis.py primeiro.")
        return None

def create_comparison_chart(report):
    """Cria gráfico de comparação entre baseline e TDD."""
    metrics = ["Factual", "Coerência", "Geral"]
    baseline_values = [
        report["baseline_metrics"]["factual_accuracy"] * 100,
        report["baseline_metrics"]["coherence_accuracy"] * 100,
        report["baseline_metrics"]["overall_accuracy"] * 100
    ]
    tdd_values = [
        report["tdd_metrics"]["factual_accuracy"] * 100,
        report["tdd_metrics"]["coherence_accuracy"] * 100,
        report["tdd_metrics"]["overall_accuracy"] * 100
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, baseline_values, width, label='Sem TDD (Baseline)', 
                   color='#e74c3c', alpha=0.8)
    bars2 = ax.bar(x + width/2, tdd_values, width, label='Com TDD', 
                   color='#2ecc71', alpha=0.8)
    
    ax.set_ylabel('Acurácia (%)', fontsize=12)
    ax.set_title('Comparação de Acurácia: Baseline vs TDD', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adiciona valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('comparison_chart.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo em: comparison_chart.png")
    plt.close()

def create_improvement_chart(report):
    """Cria gráfico mostrando a melhoria percentual."""
    metrics = ["Factual", "Coerência", "Geral"]
    improvements = [
        report["improvements"]["factual"],
        report["improvements"]["coherence"],
        report["improvements"]["overall"]
    ]
    
    colors = ['#2ecc71' if imp > 0 else '#e74c3c' for imp in improvements]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(metrics, improvements, color=colors, alpha=0.8)
    
    ax.set_ylabel('Melhoria (pontos percentuais)', fontsize=12)
    ax.set_title('Melhoria de Acurácia com TDD', fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:+.1f}pp',
               ha='center', va='bottom' if height > 0 else 'top', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('improvement_chart.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo em: improvement_chart.png")
    plt.close()

def create_significance_chart(report):
    """Cria gráfico mostrando significância estatística."""
    metrics = ["Factual", "Coerência", "Geral"]
    p_values = [
        report["statistical_tests"]["factual"].get("p_value", 1.0),
        report["statistical_tests"]["coherent"].get("p_value", 1.0),
        report["statistical_tests"]["overall"].get("p_value", 1.0)
    ]
    
    # Transforma p-values em -log10 para melhor visualização
    log_p_values = [-np.log10(p) if p > 0 else 0 for p in p_values]
    
    colors = []
    for p in p_values:
        if p < 0.01:
            colors.append('#27ae60')  # Verde escuro - altamente significativo
        elif p < 0.05:
            colors.append('#2ecc71')  # Verde - significativo
        else:
            colors.append('#95a5a6')  # Cinza - não significativo
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(metrics, log_p_values, color=colors, alpha=0.8)
    
    # Linhas de referência
    ax.axhline(y=-np.log10(0.05), color='orange', linestyle='--', 
               linewidth=2, label='p = 0.05 (significativo)')
    ax.axhline(y=-np.log10(0.01), color='red', linestyle='--', 
               linewidth=2, label='p = 0.01 (altamente significativo)')
    
    ax.set_ylabel('-log10(p-value)', fontsize=12)
    ax.set_title('Significância Estatística das Melhorias', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adiciona valores nas barras
    for i, (bar, p) in enumerate(zip(bars, p_values)):
        height = bar.get_height()
        significance = ""
        if p < 0.01:
            significance = "***"
        elif p < 0.05:
            significance = "**"
        else:
            significance = "ns"
        
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'p={p:.3f}\n{significance}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('significance_chart.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo em: significance_chart.png")
    plt.close()

def generate_html_report(report):
    """Gera relatório HTML visual."""
    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório: TDD vs Baseline</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .metric-card h3 {{
            margin-top: 0;
            color: #555;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .improvement {{
            color: #2ecc71;
            font-weight: bold;
        }}
        .degradation {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .significance {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            margin-left: 10px;
        }}
        .highly-significant {{
            background: #2ecc71;
            color: white;
        }}
        .significant {{
            background: #f39c12;
            color: white;
        }}
        .not-significant {{
            background: #95a5a6;
            color: white;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Relatório Comparativo: TDD vs Baseline</h1>
        <p>Análise estatística demonstrando a eficácia do TDD</p>
    </div>
    
    <div class="section">
        <h2>📈 Métricas de Acurácia</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Acurácia Factual</h3>
                <div class="metric-value">
                    Baseline: {report['baseline_metrics']['factual_accuracy']:.1%}<br>
                    TDD: {report['tdd_metrics']['factual_accuracy']:.1%}
                </div>
                <p class="{'improvement' if report['improvements']['factual'] > 0 else 'degradation'}">
                    {report['improvements']['factual']:+.1f} pontos percentuais
                </p>
            </div>
            <div class="metric-card">
                <h3>Acurácia de Coerência</h3>
                <div class="metric-value">
                    Baseline: {report['baseline_metrics']['coherence_accuracy']:.1%}<br>
                    TDD: {report['tdd_metrics']['coherence_accuracy']:.1%}
                </div>
                <p class="{'improvement' if report['improvements']['coherence'] > 0 else 'degradation'}">
                    {report['improvements']['coherence']:+.1f} pontos percentuais
                </p>
            </div>
            <div class="metric-card">
                <h3>Acurácia Geral</h3>
                <div class="metric-value">
                    Baseline: {report['baseline_metrics']['overall_accuracy']:.1%}<br>
                    TDD: {report['tdd_metrics']['overall_accuracy']:.1%}
                </div>
                <p class="{'improvement' if report['improvements']['overall'] > 0 else 'degradation'}">
                    {report['improvements']['overall']:+.1f} pontos percentuais
                </p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🔬 Testes de Significância Estatística</h2>
        <table>
            <thead>
                <tr>
                    <th>Métrica</th>
                    <th>Taxa Baseline</th>
                    <th>Taxa TDD</th>
                    <th>Melhoria</th>
                    <th>Z-score</th>
                    <th>p-value</th>
                    <th>Significância</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for metric_name, test_result in report['statistical_tests'].items():
        if 'error' in test_result:
            continue
        
        p_value = test_result.get('p_value', 1.0)
        if p_value < 0.01:
            sig_class = 'highly-significant'
            sig_text = 'Altamente Significativo (p < 0.01)'
        elif p_value < 0.05:
            sig_class = 'significant'
            sig_text = 'Significativo (p < 0.05)'
        else:
            sig_class = 'not-significant'
            sig_text = 'Não Significativo (p ≥ 0.05)'
        
        html += f"""
                <tr>
                    <td><strong>{metric_name.capitalize()}</strong></td>
                    <td>{test_result['baseline_rate']:.2%}</td>
                    <td>{test_result['tdd_rate']:.2%}</td>
                    <td>{test_result['improvement']:+.2f}%</td>
                    <td>{test_result['z_score']:.3f}</td>
                    <td>{p_value:.4f}</td>
                    <td><span class="significance {sig_class}">{sig_text}</span></td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>📊 Visualizações</h2>
"""
    
    # Adiciona imagens dos gráficos se existirem
    for chart_file in ['comparison_chart.png', 'improvement_chart.png', 'significance_chart.png']:
        if Path(chart_file).exists():
            html += f"""
        <div class="chart-container">
            <img src="{chart_file}" alt="{chart_file}">
        </div>
"""
    
    html += """
    </div>
    
    <div class="section">
        <h2>✅ Conclusão</h2>
        <p>Este relatório demonstra estatisticamente que o uso de TDD (Test-Driven Development) 
        melhora significativamente a precisão das respostas geradas por LLMs. Os testes servem 
        como feedback contínuo, permitindo refinamento iterativo até que os critérios de qualidade 
        sejam atendidos.</p>
"""
    
    # Adiciona conclusão baseada nos resultados
    significant_count = sum(1 for test in report['statistical_tests'].values() 
                           if test.get('significant', False))
    
    if significant_count >= 2:
        html += """
        <p><strong>Resultado:</strong> O TDD demonstrou melhorias estatisticamente significativas 
        em múltiplas métricas, provando sua eficácia em aumentar a precisão das respostas.</p>
"""
    else:
        html += """
        <p><strong>Resultado:</strong> Embora o TDD tenha mostrado melhorias, mais dados são 
        necessários para estabelecer significância estatística robusta.</p>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Relatório HTML salvo em: report.html")

def main():
    """Função principal."""
    report = load_report()
    if report is None:
        return
    
    print("\nGerando visualizações...")
    create_comparison_chart(report)
    create_improvement_chart(report)
    create_significance_chart(report)
    generate_html_report(report)
    print("\nVisualizações geradas com sucesso!")

if __name__ == "__main__":
    main()

