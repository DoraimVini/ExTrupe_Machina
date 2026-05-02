import os
import json
import pandas as pd
import requests
import shutil
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
STOCK_DB_ID = "35205465-f1ab-80a8-8de4-e23cea9e7136"
CALENDAR_DB_ID = "35205465-f1ab-8059-be92-e6a01fc0fc7a"
EXCEL_FILE = "trupe_br_gestao.xlsx"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def clear_database(database_id):
    print(f"Limpando base Notion: {database_id}...")
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get("results", [])
        for page in results:
            requests.patch(f"https://api.notion.com/v1/pages/{page['id']}", headers=HEADERS, json={"archived": True})
    else:
        print(f"Erro ao limpar base: {response.text}")

def sync_stock():
    print("Sincronizando Estoque com Notion...")
    df_e = pd.read_excel(EXCEL_FILE, sheet_name='Estoque', header=1)
    df_p = pd.read_excel(EXCEL_FILE, sheet_name='Produtos', header=1)
    
    produtos_info = {}
    for _, row in df_p.iterrows():
        nome = str(row.iloc[0])
        if pd.isna(nome) or nome == 'nan' or nome == 'Produto' or 'CADASTRO' in nome: continue
        
        try:
            preco_raw = row.iloc[2]
            if isinstance(preco_raw, (int, float)):
                preco = float(preco_raw)
            else:
                try: preco = float(str(preco_raw).replace('R$', '').replace(',', '.').strip())
                except: preco = 0
        except: preco = 0

        produtos_info[nome] = {
            'categoria': str(row.iloc[1]) if not pd.isna(row.iloc[1]) else "Outros",
            'preco': preco,
            'obs': str(row.iloc[9]) if not pd.isna(row.iloc[9]) else ""
        }

    count = 0
    for _, row in df_e.iterrows():
        nome = str(row['Produto']).strip()
        if pd.isna(nome) or nome == 'nan' or nome == 'Produto' or 'ESTOQUE' in nome: continue
        
        try: qtd_atual = float(row['Estoque Atual']) if not pd.isna(row['Estoque Atual']) else 0
        except: qtd_atual = 0
        
        info = produtos_info.get(nome, {'categoria': 'Outros', 'preco': 0, 'obs': ''})
        status = "Disponível" if qtd_atual > 0 else "Esgotado"
        if 0 < qtd_atual <= 2: status = "Baixo Estoque"

        properties = {
            "Nome": {"title": [{"text": {"content": nome}}]},
            "Categoria": {"select": {"name": info['categoria']}},
            "Preço": {"number": info['preco']},
            "Status": {"select": {"name": status}},
            "Foto": {"rich_text": [{"text": {"content": info['obs']}}]}
        }
        
        requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json={
            "parent": {"database_id": STOCK_DB_ID}, 
            "properties": properties
        })
        count += 1
            
    print(f"Sucesso! {count} itens sincronizados.")

def sync_calendar():
    print("Sincronizando Calendário...")
    start_date = datetime.now()
    count = 0
    for i in range(15):
        current_date = start_date + timedelta(days=i)
        if current_date.weekday() == 5: name = "Feira da Lavradio"
        elif current_date.weekday() == 6: name = "Feira da Glória"
        else: continue
            
        properties = {
            "": {"title": [{"text": {"content": name}}]}, # Campo título sem nome
            "Data de Postagem": {"date": {"start": current_date.strftime("%Y-%m-%d")}},
            "Tipo": {"rich_text": [{"text": {"content": "Feira"}}]},
            "Plataforma": {"rich_text": [{"text": {"content": "Presencial"}}]}
        }

        requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json={
            "parent": {"database_id": CALENDAR_DB_ID}, 
            "properties": properties
        })
        count += 1
    print(f"Sucesso! {count} eventos criados.")

if __name__ == "__main__":
    clear_database(STOCK_DB_ID)
    clear_database(CALENDAR_DB_ID)
    sync_stock()
    sync_calendar()
    print("Sincronização completa!")
