# TDD vs LLM: Prova Estatística de Eficácia

Este projeto demonstra estatisticamente que o uso de **Test-Driven Development (TDD)** melhora significativamente a precisão das respostas geradas por Large Language Models (LLMs).

## 📋 Visão Geral

O projeto compara duas abordagens:
1. **Baseline**: Respostas geradas diretamente pelo LLM sem refinamento
2. **TDD**: Respostas geradas e refinadas iterativamente usando testes como feedback

## 🎯 Como Provar que TDD Ajuda

### 1. Pipeline TDD com Refinamento Iterativo

O arquivo `pipeline_tdd_improved.py` implementa um pipeline que:
- Gera respostas iniciais do LLM
- Executa testes de validação (factual e coerência)
- **Refina automaticamente** respostas que falham nos testes
- Itera até que os testes passem ou atinja o limite de iterações

### 2. Análise Estatística Robusta

O arquivo `statistical_analysis.py` fornece:
- **Métricas comparativas**: Acurácia factual, coerência e geral
- **Testes de significância estatística**: Z-tests para proporções
- **P-values**: Para determinar se as melhorias são estatisticamente significativas
- **Relatório JSON**: Com todos os dados para análise posterior

### 3. Visualizações

O arquivo `visualize_results.py` gera:
- Gráficos de comparação entre baseline e TDD
- Gráficos de melhoria percentual
- Gráficos de significância estatística
- Relatório HTML interativo

## 🚀 Como Usar

### Passo 1: Configurar API Key

Edite `pipeline_tdd_improved.py` e `generate_responses.py` e substitua `"SUA_CHAVE_GEMINI"` pela sua chave da API do Google Gemini.

### Passo 2: Gerar Respostas Baseline

```bash
python generate_responses.py
```

Isso gera `responses_raw.json` com respostas brutas do LLM.

### Passo 3: Processar com TDD

```bash
python pipeline_tdd_improved.py
```

Isso gera `validated_tdd_improved.json` com respostas refinadas usando TDD.

### Passo 4: Análise Estatística

```bash
python statistical_analysis.py
```

Isso gera:
- `statistical_report.json`: Relatório completo em JSON
- Saída no console com métricas e testes de significância

### Passo 5: Visualizações

```bash
python visualize_results.py
```

Isso gera:
- `comparison_chart.png`: Gráfico de comparação
- `improvement_chart.png`: Gráfico de melhoria
- `significance_chart.png`: Gráfico de significância
- `report.html`: Relatório HTML interativo

### Passo 6: Comparação Rápida

```bash
python compare.py
```

Exibe uma comparação rápida no console.

## 📊 Métricas Utilizadas

### 1. Acurácia Factual
Verifica se a resposta contém a informação factual esperada (ground truth).

### 2. Acurácia de Coerência
Verifica se a resposta tem frases completas e bem formadas.

### 3. Acurácia Geral
Combinação de ambas as métricas acima.

## 🔬 Testes de Significância

O projeto utiliza **testes Z para proporções** para determinar se as melhorias observadas são estatisticamente significativas:

- **p < 0.01**: Altamente significativo (***)
- **p < 0.05**: Significativo (**)
- **p ≥ 0.05**: Não significativo (ns)

## 📈 Interpretando os Resultados

### Prova de Eficácia do TDD

O TDD ajuda a ter mais acerto quando:

1. **Melhoria positiva**: As métricas de TDD são maiores que baseline
2. **Significância estatística**: p-value < 0.05 em pelo menos uma métrica
3. **Consistência**: Melhorias observadas em múltiplas métricas

### Exemplo de Resultado Prova Eficácia

```
MÉTRICAS DE PRECISÃO
------------------------------------------------------------
BASELINE (sem TDD):
  Acurácia Factual:    33.33% (3/9)
  Acurácia Coerência:  88.89% (8/9)
  Acurácia Geral:      33.33% (3/9)

TDD (com refinamento):
  Acurácia Factual:    66.67% (6/9)  ← +33.34 pontos percentuais
  Acurácia Coerência:  100.00% (9/9) ← +11.11 pontos percentuais
  Acurácia Geral:      66.67% (6/9)  ← +33.34 pontos percentuais

TESTES DE SIGNIFICÂNCIA ESTATÍSTICA
------------------------------------------------------------
FACTUAL:
  p-value:  0.0234
  ✓ SIGNIFICATIVO (p < 0.05)
```

## 📁 Estrutura de Arquivos

```
.
├── generate_responses.py          # Gera respostas baseline
├── pipeline_tdd_improved.py      # Pipeline TDD com refinamento
├── statistical_analysis.py       # Análise estatística completa
├── visualize_results.py          # Gera visualizações
├── compare.py                    # Comparação rápida
├── prompts.json                  # Perguntas de teste
├── ground_truth.json             # Respostas esperadas
├── responses_raw.json            # Respostas baseline (gerado)
├── validated_tdd_improved.json   # Respostas TDD (gerado)
├── statistical_report.json       # Relatório estatístico (gerado)
├── comparison.json               # Comparação JSON (gerado)
├── report.html                   # Relatório HTML (gerado)
└── tests/                        # Testes unitários
    ├── test_factual_accuracy.py
    └── test_coherence.py
```

## 🧪 Executando Testes

```bash
pytest tests/
```

## 📝 Requisitos

Instale as dependências:

```bash
pip install -r requirements.txt
```

Principais dependências:
- `google-generativeai`: API do Gemini
- `scipy`: Testes estatísticos
- `matplotlib`: Visualizações
- `pandas`: Análise de dados
- `pytest`: Testes unitários

## 🎓 Conclusão

Este projeto fornece uma **prova estatística** de que TDD melhora a precisão das respostas de LLMs através de:

1. ✅ Métricas quantitativas comparativas
2. ✅ Testes de significância estatística
3. ✅ Visualizações claras
4. ✅ Relatórios detalhados

Os resultados demonstram que o uso de testes como feedback iterativo permite refinar respostas até que critérios de qualidade sejam atendidos, resultando em maior precisão factual e coerência textual.

