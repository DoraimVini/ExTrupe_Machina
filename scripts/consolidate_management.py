import pandas as pd
import os
import shutil
from datetime import datetime

def consolidate():
    file_path = 'trupe_br_gestao.xlsx'
    backup_path = f'trupe_br_gestao_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return

    print(f"Criando backup: {backup_path}")
    shutil.copy2(file_path, backup_path)
    
    # Ler abas
    print("Lendo dados...")
    xl = pd.ExcelFile(file_path)
    
    # Vendas (Header na linha 1)
    df_vendas = pd.read_excel(xl, sheet_name='Vendas', header=1)
    # Estoque (Header na linha 1)
    df_estoque = pd.read_excel(xl, sheet_name='Estoque', header=1)
    # Produtos (Header na linha 1)
    df_produtos = pd.read_excel(xl, sheet_name='Produtos', header=1)
    # Dashboard (Apenas para preservar)
    try:
        df_dash = pd.read_excel(xl, sheet_name='Dashboard')
    except:
        df_dash = None

    # 1. Processar Vendas
    print("Processando vendas...")
    sales_summary = []
    for index, row in df_vendas.iterrows():
        if index >= len(df_vendas): break
        try:
            produto = str(row['Produto']).strip()
            canal = str(row['Canal']).lower()
            qtd = row['Qtd']
        except:
            continue
            
        if pd.isna(produto) or produto == 'nan' or produto == 'TOTAL' or pd.isna(qtd):
            continue
            
        tipo_venda = 'Feira' if 'feira' in canal else 'Online'
        sales_summary.append({'Produto': produto, 'Qtd': qtd, 'Tipo': tipo_venda})
    
    df_sales_sum = pd.DataFrame(sales_summary)
    if not df_sales_sum.empty:
        agg_sales = df_sales_sum.groupby(['Produto', 'Tipo'])['Qtd'].sum().unstack(fill_value=0)
    else:
        agg_sales = pd.DataFrame(columns=['Feira', 'Online'])
        
    if 'Feira' not in agg_sales.columns: agg_sales['Feira'] = 0
    if 'Online' not in agg_sales.columns: agg_sales['Online'] = 0

    # 1.1 Processar Financeiro
    print("Processando resumo financeiro...")
    total_receita = df_vendas['Receita (R$)'].sum()
    total_custo = df_vendas['Custo Total (R$)'].sum()
    total_lucro = df_vendas['Lucro (R$)'].sum()
    
    # Receita por canal
    receita_canal = df_vendas.groupby('Canal')['Receita (R$)'].sum().to_dict()
    
    # Criar DataFrame para Dashboard
    dash_data = [
        ['TRUPE BR - RESUMO FINANCEIRO', '', '', 'RECEITA POR CANAL', 'VALOR'],
        ['', '', '', '', ''],
        ['RECEITA TOTAL', total_receita, '', 'Feira Glória', receita_canal.get('Feira Glória', 0)],
        ['CUSTO TOTAL', total_custo, '', 'Feira Lavradio', receita_canal.get('Feira Lavradio', 0)],
        ['LUCRO TOTAL', total_lucro, '', 'Online', receita_canal.get('Online', 0)],
        ['', '', '', '', ''],
        ['PRODUTOS MAIS VENDIDOS', 'QTD', '', 'LUCRO POR PRODUTO', 'VALOR']
    ]
    
    # Top 5 produtos por quantidade
    top_vendas = df_vendas.groupby('Produto')['Qtd'].sum().sort_values(ascending=False).head(5)
    # Top 5 produtos por lucro
    top_lucro = df_vendas.groupby('Produto')['Lucro (R$)'].sum().sort_values(ascending=False).head(5)
    
    for i in range(5):
        row = ['', '', '', '', '']
        if i < len(top_vendas):
            row[0] = top_vendas.index[i]
            row[1] = top_vendas.values[i]
        if i < len(top_lucro):
            row[3] = top_lucro.index[i]
            row[4] = top_lucro.values[i]
        dash_data.append(row)
        
    df_dash_new = pd.DataFrame(dash_data)

    # 2. Processar Dados de Produtos (Catálogo)
    print("Mapeando catálogo de produtos...")
    catalog = {}
    for index, row in df_produtos.iterrows():
        try:
            nome = str(row['Produto']).strip()
            cat = str(row['Categoria']).strip()
            preco = row['Preço Venda (R$)']
        except:
            continue
            
        if pd.isna(nome) or nome == 'nan' or 'CADASTRO' in nome or nome == 'Produto':
            continue
        
        catalog[nome.lower()] = {
            'Nome Original': nome,
            'Categoria': cat if not pd.isna(cat) else 'Outros',
            'Preço': preco if not pd.isna(preco) else 0
        }

    # 3. Garantir que todos os produtos do catálogo e das vendas estejam no Estoque
    print("Verificando produtos faltantes no estoque...")
    existing_products = set(df_estoque['Produto'].dropna().str.strip().str.lower().unique())
    
    new_rows = []
    # Da lista de produtos cadastrados
    for p_lower, info in catalog.items():
        if p_lower not in existing_products:
            print(f"Adicionando ao estoque: {info['Nome Original']} (do catálogo)")
            new_rows.append({
                'Produto': info['Nome Original'],
                'Estoque 26/04': 0,
                'Produzido (semana)': 0,
                'Vendido Feira': 0,
                'Vendido Online': 0,
                'Estoque Atual': 0,
                'Status': 'Novo',
                'Observação': 'Adicionado automaticamente do catálogo'
            })
            existing_products.add(p_lower)

    # Das vendas (caso algum produto tenha sido vendido mas não esteja no catálogo nem estoque)
    for v_prod in agg_sales.index:
        if v_prod.lower() not in existing_products:
            print(f"Adicionando ao estoque: {v_prod} (das vendas)")
            new_rows.append({
                'Produto': v_prod,
                'Estoque 26/04': 0,
                'Produzido (semana)': 0,
                'Vendido Feira': 0,
                'Vendido Online': 0,
                'Estoque Atual': 0,
                'Status': 'Novo',
                'Observação': 'Vendido mas não estava no estoque'
            })
            existing_products.add(v_prod.lower())

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df_estoque = pd.concat([df_estoque, df_new], ignore_index=True)

    # 4. Atualizar Valores do Estoque
    print("Atualizando quantidades e cálculos...")
    for index, row in df_estoque.iterrows():
        produto_estoque = str(row['Produto']).strip()
        if pd.isna(produto_estoque) or produto_estoque == 'nan' or produto_estoque == 'Produto':
            continue
            
        p_lower = produto_estoque.lower()
        
        # Vendas
        vendas_feira = 0
        vendas_online = 0
        
        # Match exato ou parcial nas vendas
        for v_name in agg_sales.index:
            if v_name.lower() == p_lower:
                vendas_feira = agg_sales.loc[v_name, 'Feira']
                vendas_online = agg_sales.loc[v_name, 'Online']
                break
        
        # Atualizar colunas de venda
        df_estoque.loc[index, 'Vendido Feira'] = vendas_feira
        df_estoque.loc[index, 'Vendido Online'] = vendas_online
        
        # Cálculo: Estoque Atual = Inicial + Produzido - Vendido
        inicial = row['Estoque 26/04'] if not pd.isna(row['Estoque 26/04']) else 0
        produzido = row['Produzido (semana)'] if not pd.isna(row['Produzido (semana)']) else 0
        
        estoque_final = inicial + produzido - vendas_feira - vendas_online
        df_estoque.loc[index, 'Estoque Atual'] = estoque_final
        
        # Status
        if estoque_final < 0:
            df_estoque.loc[index, 'Status'] = '🚨 ERRO: NEGATIVO'
        elif estoque_final <= 2:
            df_estoque.loc[index, 'Status'] = '⚠️ BAIXO'
        else:
            df_estoque.loc[index, 'Status'] = '✅ OK'

    # 5. Salvar Tudo
    print(f"Salvando alterações em {file_path}...")
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df_produtos.to_excel(writer, sheet_name='Produtos', index=False, startrow=1)
        # O header original de Produtos tem 2 linhas (0 e 1), salvamos a partir da 1.
        # Mas para garantir que não perdemos a linha 0:
        # Melhor estratégia: carregar o original e escrever por cima apenas onde precisa
        # Mas o pandas engine='openpyxl' mode='a' é chato com formatacao.
        # Vamos reescrever as abas principais e tentar manter o resto.
        
        # Escrever Estoque atualizado
        df_estoque.to_excel(writer, sheet_name='Estoque', index=False, startrow=1)
        
        # Escrever Vendas e Dashboard
        df_vendas.to_excel(writer, sheet_name='Vendas', index=False, startrow=1)
        df_dash_new.to_excel(writer, sheet_name='Dashboard', index=False, header=False)

    print("Consolidação finalizada com sucesso!")

if __name__ == "__main__":
    consolidate()
