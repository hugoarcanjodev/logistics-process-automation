# LogiPy-Analytics - Logistics Process Automation

**Automação de ETL e KPIs de Supply Chain para controle de estoque e produtividade operacional**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Vetorização-013243?logo=numpy&logoColor=white)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-217346?logo=microsoftexcel&logoColor=white)
![Área](https://img.shields.io/badge/Área-Logística%20%26%20Supply%20Chain-orange)
![Status](https://img.shields.io/badge/Status-MVP-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Visão Geral

Em Centros de Distribuição (CDs) e indústrias, analistas gastam horas tratando dados brutos exportados de sistemas **ERP** (SAP, Totvs) e **WMS** antes de conseguirem analisá-los. Esse trabalho manual atrasa decisões e aumenta o risco de **ruptura de estoque** e de **subutilização da mão de obra**.

O **LogiPy-Analytics** é um projeto autoral que automatiza esse pipeline de ponta a ponta:

1. **Extração:** leitura de bases brutas simuladas de ERP (estoque) e WMS (picking).
2. **Transformação:** limpeza, padronização e agregação dos dados com Pandas.
3. **Cálculo de KPIs:** Dias de Suprimento, Status de Abastecimento e Caixas por Hora.
4. **Entrega:** relatório gerencial `.xlsx` com abas estruturadas, pronto para a liderança.

> **Nota:** os dados deste repositório são **sintéticos**, gerados pelo próprio script para fins de demonstração. Nenhuma informação de empresa real é utilizada.

---

## 🎯 Problemas de Negócio Endereçados

| Problema | Como o projeto atua |
| :--- | :--- |
| Risco de ruptura de estoque | Classificação automática de SKUs por cobertura (Crítico / Atenção / OK) |
| Retrabalho manual em Excel | Pipeline reprodutível: um comando substitui o "copiar e colar" |
| Falta de visibilidade da produtividade | Ranking de operadores por CPH para apoio ao dimensionamento de equipe e escala |
| Capital de giro retido | Valorização do estoque por SKU (`Estoque × Custo Unitário`) |

---

## 🛠️ Stack Tecnológica

- **Python 3.9+**: linguagem base.
- **Pandas**: limpeza, junção e agregação dos dados.
- **NumPy**: lógica condicional vetorizada (`np.select`) para classificação de risco.
- **OpenPyXL**: geração do `.xlsx` com múltiplas abas.

### Conceitos de Engenharia de Produção aplicados

- **Days of Supply (DoS):** cobertura de estoque em dias, com base na demanda média diária.
- **Ruptura de Estoque (Stockout):** prevenção de falta de produto.
- **Produtividade do fator trabalho (CPH):** caixas separadas por hora trabalhada.

---

## 📂 Estrutura do Repositório

```text
logistics-process-automation/
├── logipy_analytics.py            # Script principal: ETL, KPIs e exportação
├── requirements.txt               # Dependências do projeto
├── data/
│   ├── erp_estoque_bruto.csv     # Base simulada: estoque (ERP)
│   └── wms_picking_bruto.csv     # Base simulada: picking (WMS)
├── output/
│   └── controle_estoque.csv  # Relatório
│   └── produtividade_picking.csv  # Relatório
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📈 Indicadores (KPIs)

### 1. Controle de Estoque

| Métrica | Fórmula | Impacto operacional |
| :--- | :--- | :--- |
| **Valor Total em Estoque** | `Estoque_Atual × Custo_Unitario` | Capital de giro imobilizado por SKU |
| **Dias de Suprimento (DoS)** | `Estoque_Atual ÷ Demanda_Media_Diaria` | Quantos dias a operação se sustenta com o saldo atual |
| **Status de Abastecimento** | Regra condicional (abaixo) | Alerta para Compras/PCP agirem antes da ruptura |

**Regra de classificação:**

| Status | Condição |
| :--- | :--- |
| 🔴 Crítico | DoS ≤ 5 dias |
| 🟡 Atenção | 5 < DoS ≤ 15 dias |
| 🟢 OK | DoS > 15 dias |

> Os limites (5 e 15 dias) são parâmetros de exemplo e devem ser ajustados ao lead time e à criticidade de cada operação.

### 2. Produtividade de Picking

| Métrica | Fórmula | Impacto operacional |
| :--- | :--- | :--- |
| **Caixas por Hora (CPH)** | `Caixas_Separadas ÷ Horas_Trabalhadas` | Identifica gargalos e alta performance individual e coletiva |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Git

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/hugoarcanjodev/logipy-analytics.git
cd logipy-analytics

# 2. (Recomendado) Criar e ativar um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependências
pip install -r requirements.txt
```

### Execução

```bash
python logipy_analytics.py
```

O script gera os dados simulados, processa o pipeline e salva o relatório em `output/relatorio_produtividade.xlsx`.

---

## 📊 Output Gerado

O Excel final traz duas visões gerenciais:

### Aba `Controle_Estoque`
Foco em criticidade e necessidade de ressuprimento.

| SKU | Estoque_Atual | Custo_Unitario_R$ | Demanda_Media_Diaria | Valor_Total_Estoque_R$ | Dias_de_Suprimento | Status_Abastecimento |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| SKU-001 | 120 | 15,00 | 40 | 1.800,00 | 3,0 | Crítico |
| SKU-002 | 600 | 8,50 | 50 | 5.100,00 | 12,0 | Atenção |
| SKU-003 | 2.000 | 3,20 | 60 | 6.400,00 | 33,3 | OK |

*Valores ilustrativos.*

### Aba `Produtividade_Picking`
Foco na gestão de equipes por hora trabalhada.

| Operador | Horas_Trabalhadas | Caixas_Separadas | Caixas_Por_Hora |
| :--- | ---: | ---: | ---: |
| Operador A | 8,0 | 960 | 120,0 |
| Operador B | 8,0 | 840 | 105,0 |

*Valores ilustrativos.*

> 💡 **Dica:** adicione aqui um print do relatório real em `docs/` e referencie com `![Relatório](docs/relatorio.png)`.

---

## ⚠️ Limitações Conhecidas

- Utiliza dados simulados; a integração direta com ERP/WMS (via API ou banco de dados) não está implementada.
- DoS assume demanda média diária constante, sem sazonalidade ou variabilidade.
- Os limites de classificação são fixos no código.

---

## 🧭 Roadmap

- [ ] **Curva ABC:** classificar SKUs por relevância de faturamento (A, B, C) para priorizar auditorias de inventário.
- [ ] **Estoque de Segurança:** cálculo estatístico com desvio padrão da demanda e lead time do fornecedor.
- [ ] **Dashboard interativo:** migrar o output estático para um painel web com Streamlit.
- [ ] **Testes automatizados:** cobertura das regras de negócio com `pytest`.
- [ ] **Parametrização:** limites de criticidade configuráveis via arquivo de configuração.

---

## 👤 Autor

**Hugo Arcanjo**
Estudante de Engenharia de Produção | Logística & Supply Chain | Automação e Análise de Dados

- 💼 [LinkedIn](https://www.linkedin.com/in/hugo-arcanjo/)
- 🐙 [GitHub](https://github.com/hugoarcanjodev)

Projeto desenvolvido como portfólio técnico, unindo Engenharia de Produção, automação de processos e análise de dados aplicada à logística.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.