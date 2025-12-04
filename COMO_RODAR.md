# 🚀 Como Rodar o Projeto

## Opção 1: Execução Automática Completa (Recomendado)

Execute tudo de uma vez:

```bash
python run_full_analysis.py
```

Este script executa automaticamente todos os passos:
1. ✅ Gera respostas baseline
2. ✅ Processa com TDD (refina respostas)
3. ✅ Análise estatística
4. ✅ Comparação rápida
5. ✅ Gera visualizações

**Tempo estimado:** 5-10 minutos (depende da API do Gemini)

---

## Opção 2: Execução Passo a Passo

Se preferir executar manualmente ou entender cada etapa:

### Passo 1: Gerar Respostas Baseline
```bash
python generate_responses.py
```
**O que faz:** Gera respostas brutas do LLM sem refinamento
**Arquivo gerado:** `responses_raw.json`
**Tempo:** ~2-3 minutos (aguarda 5s entre cada pergunta)

### Passo 2: Processar com TDD
```bash
python pipeline_tdd_improved.py
```
**O que faz:** Refina respostas que falham nos testes
**Arquivo gerado:** `validated_tdd_improved.json`
**Tempo:** ~3-5 minutos (refina respostas que falham)

### Passo 3: Análise Estatística
```bash
python statistical_analysis.py
```
**O que faz:** Compara baseline vs TDD e calcula significância estatística
**Arquivo gerado:** `statistical_report.json`
**Tempo:** Instantâneo

### Passo 4: Comparação Rápida
```bash
python compare.py
```
**O que faz:** Mostra comparação resumida no console
**Arquivo gerado:** `comparison.json`
**Tempo:** Instantâneo

### Passo 5: Visualizações
```bash
python visualize_results.py
```
**O que faz:** Gera gráficos e relatório HTML
**Arquivos gerados:**
- `comparison_chart.png`
- `improvement_chart.png`
- `significance_chart.png`
- `report.html`
**Tempo:** Instantâneo

---

## 📊 Ver os Resultados

### Relatório HTML (Mais Visual)
Abra no navegador:
```
report.html
```

### Relatório Estatístico (JSON)
```bash
# No Windows PowerShell
Get-Content statistical_report.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Ou simplesmente abra o arquivo em um editor de texto
```

### Comparação Rápida
```bash
python compare.py
```

---

## ⚠️ Requisitos

Certifique-se de ter instalado as dependências:

```bash
pip install -r requirements.txt
```

Principais dependências:
- `google-generativeai` - API do Gemini
- `scipy` - Testes estatísticos
- `matplotlib` - Gráficos
- `pandas` - Análise de dados

---

## 🔍 Verificando se Funcionou

Após executar, você deve ter estes arquivos:

```
✓ responses_raw.json              # Respostas baseline
✓ validated_tdd_improved.json     # Respostas refinadas com TDD
✓ statistical_report.json         # Relatório estatístico completo
✓ comparison.json                 # Comparação JSON
✓ comparison_chart.png            # Gráfico de comparação
✓ improvement_chart.png           # Gráfico de melhoria
✓ significance_chart.png          # Gráfico de significância
✓ report.html                     # Relatório HTML completo
```

---

## 🐛 Problemas Comuns

### Erro: "API key not found"
- Verifique se a API key está configurada em:
  - `generate_responses.py` (linha 6)
  - `pipeline_tdd_improved.py` (linha 11)

### Erro: "File not found: prompts.json"
- Certifique-se de estar na pasta raiz do projeto
- Verifique se `prompts.json` e `ground_truth.json` existem

### Erro: "ModuleNotFoundError"
- Instale as dependências: `pip install -r requirements.txt`

### API muito lenta
- O código já tem delays (5s entre requisições)
- Se ainda der erro de rate limit, aumente o delay em `generate_responses.py`

---

## 💡 Dica

Para ver o progresso em tempo real, execute passo a passo (Opção 2) ao invés do script automático.

