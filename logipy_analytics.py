import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURAÇÃO DE DIRETÓRIOS (Conforme nova estratégia de CSVs)
# ==============================================================================
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# STEP 1: SIMULAÇÃO DE DADOS BRUTOS (WMS / ERP em CSV)
# ==============================================================================
def criar_dados_ficticios():
    np.random.seed(42)
    
    # 1. Cadastro de Produtos (Estoque ERP)
    produtos = [f'SKU-{i:03d}' for i in range(1, 21)]
    estoque_atual = np.random.randint(50, 2500, size=20)
    custo_unitario = np.random.uniform(3.0, 150.0, size=20).round(2)
    demanda_media_diaria = np.random.randint(10, 80, size=20)
    
    df_estoque = pd.DataFrame({
        'SKU': produtos,
        'Estoque_Atual': estoque_atual,
        'Custo_Unitario_R$': custo_unitario,
        'Demanda_Media_Diaria': demanda_media_diaria
    })
    
    # 2. Histórico de Produtividade (Operação de Picking WMS)
    operadores = ['Operador A', 'Operador B', 'Operador C', 'Operador D']
    datas = [datetime(2026, 11, 1) + timedelta(days=i) for i in range(5)]
    
    linhas_picking = []
    for data in datas:
        for op in operadores:
            linhas_picking.append({
                'Data': data.strftime('%Y-%m-%d'),
                'Operador': op,
                'Horas_Trabalhadas': float(np.random.choice([6.0, 8.0, 8.5])),
                'Caixas_Separadas': np.random.randint(400, 1000)
            })
            
    df_picking = pd.DataFrame(linhas_picking)
    
    # Salvando os arquivos brutos em CSV
    df_estoque.to_csv(os.path.join(DATA_DIR, 'erp_estoque_bruto.csv'), index=False)
    df_picking.to_csv(os.path.join(DATA_DIR, 'wms_picking_bruto.csv'), index=False)
    print(f"✨ Dados brutos em CSV gerados com sucesso em: '{DATA_DIR}/'")

# ==============================================================================
# STEP 2: PIPELINE ETL E CÁLCULO DE KPIS DE SUPPLY CHAIN
# ==============================================================================
def processar_dados_logistica():
    # Caminhos dos arquivos de entrada e saída
    caminho_estoque = os.path.join(DATA_DIR, 'erp_estoque_bruto.csv')
    caminho_picking = os.path.join(DATA_DIR, 'wms_picking_bruto.csv')
    
    saida_estoque = os.path.join(OUTPUT_DIR, 'controle_estoque.csv')
    saida_produtividade = os.path.join(OUTPUT_DIR, 'produtividade_picking.csv')
    
    # Carregando dados brutos de arquivos CSV
    df_estoque = pd.read_csv(caminho_estoque)
    df_picking = pd.read_csv(caminho_picking)
    
    # --- PIPELINE 1: Controle de Estoque ---
    df_estoque['Valor_Total_Estoque_R$'] = (df_estoque['Estoque_Atual'] * df_estoque['Custo_Unitario_R$']).round(2)
    df_estoque['Dias_de_Suprimento'] = (df_estoque['Estoque_Atual'] / df_estoque['Demanda_Media_Diaria']).round(1)
    
    condicoes = [
        (df_estoque['Dias_de_Suprimento'] <= 5),
        (df_estoque['Dias_de_Suprimento'] > 5) & (df_estoque['Dias_de_Suprimento'] <= 15),
        (df_estoque['Dias_de_Suprimento'] > 15)
    ]
    escolhas = ['Crítico', 'Atenção', 'OK']
    df_estoque['Status_Abastecimento'] = np.select(condicoes, escolhas, default='Sem Dados')
    
    # --- PIPELINE 2: Monitoramento de Produtividade ---
    df_performance = df_picking.groupby('Operador').agg({
        'Horas_Trabalhadas': 'sum',
        'Caixas_Separadas': 'sum'
    }).reset_index()
    
    df_performance['Caixas_Por_Hora'] = (df_performance['Caixas_Separadas'] / df_performance['Horas_Trabalhadas']).round(1)
    df_performance = df_performance.sort_values(by='Caixas_Por_Hora', ascending=False)
    
    # --- PIPELINE 3: Exportação dos Outputs Individuais em CSV ---
    df_estoque.to_csv(saida_estoque, index=False)
    df_performance.to_csv(saida_produtividade, index=False)
        
    print(f"🚀 Relatórios CSV gerados em: '{OUTPUT_DIR}/'")

if __name__ == '__main__':
    criar_dados_ficticios()
    processar_dados_logistica()
