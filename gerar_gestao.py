import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
import re

# ============================================================
# 1. VENDAS EXTRAÍDAS DAS IMAGENS (DATAS CORRIGIDAS)
# ============================================================
# Dados originais da minha tabela anterior, com a correção:
# - "2026-08-05" → "2026-03-05" (usuário disse que confundimos agosto com março)
# - Mantidas todas as outras datas (janeiro a abril de 2026)
# - Incluídas vendas de 01/02/2026 (presentes na imagem 1000221398.jpg)

vendas_raw = [
    # Abril 2026
    ("2026-04-04", "", "Top", 1, 300, 300, "DEBT", ""),

    # Vendas de Abril 2026 (Adicionadas da planilha de gestão - 26/04)
    ("2026-04-26", "Glória", "Biquíni (sutiã)", 1, 65, 65, "CRED", ""),
    ("2026-04-26", "Glória", "Biquíni (sutiã)", 2, 65, 130, "CRED", ""),
    ("2026-04-26", "Glória", "Faixa Triangular", 2, 35, 70, "CRED", ""),
    ("2026-04-26", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-04-26", "Glória", "Boné", 1, 40, 40, "PIX", ""),
    ("2026-04-26", "Glória", "Top", 1, 85, 85, "PIX", ""),
    ("2026-04-26", "Glória", "Faixa Triangular", 1, 35, 35, "DEBT", ""),
    ("2026-04-26", "Glória", "Biquíni (sutiã)", 1, 65, 65, "DEBT", ""),
    ("2026-04-26", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-04-26", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-04-26", "Glória", "Faixa de Amarrar", 1, 35, 35, "CRED", ""),
    ("2026-04-26", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-04-26", "Glória", "Biquíni (sutiã)", 1, 65, 65, "CRED", ""),

    # Março 2026 (inclui a antiga data de agosto corrigida)
    ("2026-03-05", "", "Top", 1, 85, 85, "CRED", ""),  # antes era 2026-08-05
    ("2026-03-05", "", "Faixa Amarrar", 1, 35, 35, "PIX", ""),
    ("2026-03-05", "", "B4", 1, 100, 100, "CRED", ""),
    ("2026-03-05", "", "Macramê", 1, 195, 195, "CRED", ""),
    ("2026-03-05", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-05", "", "Faixa Amarrar", 1, 35, 35, "CRED", ""),
    ("2026-03-05", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-05", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "DIN", ""),
    ("2026-03-29", "Glória", "Top", 1, 65, 65, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 65, 65, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "DEBT", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Touca", 1, 40, 40, "PIX", ""),
    ("2026-03-29", "Glória", "Faixa A", 1, 35, 35, "CRED", ""),
    ("2026-03-29", "Glória", "Faixa Amarrar", 1, 100, 100, "PIX", ""),
    ("2026-03-29", "Glória", "Faixa Amarrar", 1, 35, 35, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-03-29", "Glória", "Faixa Delta", 1, 35, 35, "DEBT", ""),
    ("2026-03-29", "Glória", "Faixa Delta", 1, 35, 35, "DEBT", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-29", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-28", "Lavradio", "Faixa Amarrar", 1, 85, 85, "CRED", ""),
    ("2026-03-28", "Lavradio", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-03-28", "Lavradio", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-28", "Lavradio", "Biquini", 1, 65, 65, "DEBT", ""),
    ("2026-03-28", "Lavradio", "Faixa A", 1, 180, 180, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 140, 140, "CRED", ""),
    ("2026-03-22", "Glória", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 210, 210, "CRED", ""),
    ("2026-03-22", "Glória", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-03-22", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-22", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-22", "Glória", "Faixa Triângulo", 1, 40, 40, "PIX", ""),
    ("2026-03-21", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 170, 170, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 170, 170, "CRED", ""),
    ("2026-03-21", "", "Top", 1, 35, 35, "PIX", ""),
    ("2026-03-21", "", "Faixa Amarrar", 1, 35, 35, "PIX", ""),
    ("2026-03-14", "", "Biquini", 1, 45, 45, "CRED", ""),
    ("2026-03-14", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-14", "", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-14", "", "Touca", 1, 40, 40, "", ""),
    ("2026-03-14", "", "Touca", 1, 40, 40, "", ""),
    ("2026-03-14", "", "Top", 1, 85, 85, "", ""),
    ("2026-03-14", "", "Top", 1, 85, 85, "", ""),
    ("2026-03-08", "", "Top", 1, 85, 85, "PIX", ""),
    ("2026-03-08", "", "Biquini", 1, 65, 65, "DEBT", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "DEBT", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "PIX", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Touca", 1, 80, 80, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-08", "", "Biquini", 1, 65, 65, "", ""),
    ("2026-03-08", "", "Faixa Ombro", 1, 35, 35, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-08", "", "Faixa Cabelo", 1, 20, 20, "CRED", ""),
    ("2026-03-08", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "DEBT", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-03", "", "Touca", 1, 80, 80, "CRED", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-03", "", "Top", 1, 65, 65, "", ""),
    ("2026-03-03", "", "Faixa Ombro", 1, 35, 35, "CRED", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-03", "", "Faixa Cabelo", 1, 20, 20, "CRED", ""),
    ("2026-03-03", "", "Top", 1, 80, 80, "", ""),
    ("2026-03-01", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-03-01", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-01", "Glória", "Top", 1, 80, 80, "PIX", ""),
    ("2026-03-01", "Glória", "Touca", 1, 35, 35, "PIX", ""),
    ("2026-03-01", "Glória", "Top", 1, 105, 105, "CRED", ""),
    ("2026-03-01", "Glória", "Bolsa", 1, 10, 10, "CRED", ""),
    ("2026-03-01", "Glória", "Top", 1, 85, 85, "CRED", ""),
    ("2026-03-01", "Glória", "Top", 1, 80, 80, "PIX", ""),
    ("2026-03-01", "Glória", "Régua?", 1, 30, 30, "CRED", ""),
    ("2026-03-01", "Glória", "F1", 1, 90, 90, "CRED", ""),

    # Fevereiro 2026
    ("2026-02-28", "", "Touca", 1, 30, 30, "", ""),
    ("2026-02-28", "", "Top", 1, 85, 85, "", ""),
    ("2026-02-28", "", "Faixa", 1, 30, 30, "", ""),
    ("2026-02-28", "", "Top", 1, 85, 85, "", ""),
    ("2026-02-28", "", "Top", 1, 85, 85, "", ""),
    ("2026-02-28", "", "Faixa", 1, 30, 30, "", ""),
    ("2026-02-28", "", "Biquini", 1, 65, 65, "", ""),
    ("2026-02-25", "Glória", "Faixa", 1, 30, 30, "CRED", ""),
    ("2026-02-25", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-25", "Glória", "Biquini", 1, 65, 65, "DIN", ""),
    ("2026-02-25", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-25", "Glória", "Top", 1, 75, 75, "PIX", ""),
    ("2026-02-25", "Glória", "Top", 1, 75, 75, "CRED", ""),
    ("2026-02-25", "Glória", "Saia", 1, 100, 100, "CRED", ""),
    ("2026-02-25", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Top", 1, 15, 15, "", ""),
    ("2026-02-22", "", "Top", 1, 75, 75, "", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Faixa Delta", 1, 30, 30, "DEBT", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Biquini", 1, 130, 130, "PIX", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Faixa Delta", 1, 30, 30, "CRED", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "PIX", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-22", "", "Top", 1, 80, 80, "PIX", ""),
    ("2026-02-22", "", "Biquini", 1, 65, 65, "DEBT", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 130, 130, "", ""),
    ("2026-02-08", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-08", "Glória", "Faixa Amarrar", 1, 90, 90, "CRED", ""),
    ("2026-02-08", "Glória", "Faixa Delta", 1, 30, 30, "", ""),
    ("2026-02-08", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-08", "Glória", "Faixa Delta", 1, 30, 30, "", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 30, 30, "CRED", ""),
    ("2026-02-08", "Glória", "Faixa Delta", 1, 30, 30, "CRED", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-02-08", "Glória", "Biquini", 1, 80, 80, "", ""),
    ("2026-02-01", "", "Top", 1, 80, 80, "CRED", ""),  # 01/02
    ("2026-02-01", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-02-01", "", "Top", 1, 80, 80, "CRED", ""),

    # Janeiro 2026
    ("2026-01-31", "Lavradio", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-01-31", "Lavradio", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-01-31", "Lavradio", "Faixa Top", 1, 60, 60, "PIX", ""),
    ("2026-01-31", "Lavradio", "Top", 1, 80, 80, "", ""),
    ("2026-01-31", "Lavradio", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-31", "Lavradio", "Top", 1, 80, 80, "PIX", ""),
    ("2026-01-31", "Lavradio", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-31", "Lavradio", "Top", 1, 80, 80, "PIX", ""),
    ("2026-01-18", "Glória", "Top", 1, 60, 60, "PIX", ""),
    ("2026-01-18", "Glória", "Top", 1, 15, 15, "DEBT", ""),
    ("2026-01-18", "Glória", "Biquini", 1, 65, 65, "CRED", ""),
    ("2026-01-18", "Glória", "Top", 1, 15, 15, "CRED", ""),
    ("2026-01-18", "Glória", "Faixa Delta", 1, 30, 30, "PIX", ""),
    ("2026-01-18", "Glória", "Faixa Amarrar", 1, 30, 30, "", ""),
    ("2026-01-18", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-18", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-18", "Glória", "Top", 1, 80, 80, "PIX", ""),
    ("2026-01-18", "Glória", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-18", "Glória", "Faixa Amarrar", 1, 35, 35, "CRED", ""),
    ("2026-01-18", "Glória", "Faixa Amarrar", 1, 35, 35, "PIX", ""),
    ("2026-01-18", "Glória", "Saia", 1, 85, 85, "CRED", ""),
    ("2026-01-18", "Glória", "Top", 1, 80, 80, "PIX", ""),
    ("2026-01-17", "Lavradio", "Top", 1, 45, 45, "CRED", ""),
    ("2026-01-17", "Lavradio", "Top", 1, 45, 45, "CRED", ""),
    ("2026-01-17", "Lavradio", "Top", 1, 15, 15, "CRED", ""),
    ("2026-01-17", "Lavradio", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-01-17", "Lavradio", "Faixa Delta", 1, 60, 60, "PIX", ""),
    ("2026-01-17", "Lavradio", "Top", 1, 15, 15, "DEBT", ""),
    ("2026-01-17", "Lavradio", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-01-17", "Lavradio", "Faixa Amarrar", 1, 35, 35, "DEBT", ""),
    ("2026-01-17", "Lavradio", "Biquini", 1, 65, 65, "DEBT", ""),
    ("2026-01-17", "Lavradio", "Top", 1, 15, 15, "DEBT", ""),
    ("2026-01-17", "Lavradio", "Faixa", 1, 30, 30, "CRED", ""),
    ("2026-01-11", "", "Top", 1, 140, 140, "PIX", ""),
    ("2026-01-11", "", "Top", 1, 15, 15, "", ""),
    ("2026-01-11", "", "Faixa", 1, 30, 30, "PIX", ""),
    ("2026-01-11", "", "Top", 1, 45, 45, "PIX", ""),
    ("2026-01-11", "", "Biquini", 1, 65, 65, "PIX", ""),
    ("2026-01-11", "", "Top", 1, 75, 75, "PIX", ""),
    ("2026-01-11", "", "Turbante", 1, 30, 30, "", ""),
    ("2026-01-11", "", "Faixa", 1, 30, 30, "", ""),
    ("2026-01-11", "", "Saia", 1, 80, 80, "CRED", ""),
    ("2026-01-11", "", "Bolsa", 1, 70, 70, "DIN", ""),
    ("2026-01-11", "", "Top", 1, 15, 15, "PIX", ""),
    ("2026-01-11", "", "Saia", 1, 100, 100, "CRED", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "", ""),
    ("2026-01-04", "", "Faixa Amarrar", 1, 35, 35, "PIX", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "CRED", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "DEBT", ""),
    ("2026-01-04", "", "Faixa Delta", 1, 35, 35, "CRED", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "", ""),
    ("2026-01-04", "", "Faixa Delta", 1, 30, 30, "", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "", ""),
    ("2026-01-04", "", "Turbante", 1, 35, 35, "", ""),
    ("2026-01-04", "", "Top", 1, 80, 80, "PIX", ""),
]

# Converte para DataFrame
df_vendas = pd.DataFrame(vendas_raw, columns=["Data", "Local", "Item", "Qtd", "Preco", "Receita", "Metodo", "Obs"])
df_vendas["Data"] = pd.to_datetime(df_vendas["Data"])
df_vendas["Canal"] = df_vendas["Local"].apply(lambda x: f"Feira {x}" if x in ["Glória", "Lavradio"] else "Não identificado")
df_vendas["Produto"] = df_vendas["Item"].str.replace(" Faixa", "Faixa").str.replace(" Biquini", "Biquíni")
# Mapeamento de produto para nome exato da aba Produtos (ajustes manuais)
df_vendas["Produto"] = df_vendas["Produto"].replace({
    "Biquini": "Biquíni (sutiã)",
    "FaixaA": "Faixa de Cabelo",
    "FaixaAM": "Faixa de Cabelo",
    "Faixa": "Faixa de Cabelo",
    "FaixaDelta": "Faixa de Cabelo",
    "FaixaAmarrar": "Faixa Larga Dreads",
    "Touca": "Touca Unisex",
    "Turbante": "Touca Unisex",
    "Saia": "Saia",
    "Bolsa": "Bolsa",
    "Macramê": "Macramê",
    "B4": "Biquíni (sutiã)",
    "F1": "Top",
    "Régua?": "Outro",
})
df_vendas["Variação"] = "Natural"  # padrão, depois ajustar conforme cor nas imagens (simplificado)
# Para itens com variação conhecida, podemos mapear por preço ou nome. Vamos simplificar.

# ============================================================
# 2. CARREGAR ARQUIVO EXISTENTE (PRODUTOS, CUSTOS)
# ============================================================
# Simulando a leitura do arquivo fornecido. Na prática, você teria o arquivo.
# Vamos criar dataframes a partir da estrutura mostrada.
produtos_data = {
    "Produto": ["Top", "Top", "Top", "Biquíni (sutiã)", "Biquíni (sutiã)", "Faixa de Cabelo", "Faixa Larga Dreads", "Touca Unisex", "Touca Unisex", "Boné", "Faixa Triangular", "Faixa de Amarrar"],
    "Variação/Cor": ["Natural", "Terracota", "Off-white", "Natural", "Colorido", "Natural", "Natural", "Cinza", "Preta", "Natural", "Natural", "Natural"],
    "Categoria": ["Roupas", "Roupas", "Roupas", "Praia", "Praia", "Acessórios", "Acessórios", "Acessórios", "Acessórios", "Acessórios", "Acessórios", "Acessórios"],
    "Preço de Venda (R$)": [85, 85, 85, 65, 65, 35, 45, 40, 40, 40, 35, 35],
    "Custo do Fio (R$)": [18, 20, 18, 12, 14, 5, 8, 10, 10, 8, 5, 5],
    "Custo de Embalagem (R$)": [3, 3, 3, 2, 2, 1, 1, 2, 2, 1, 1, 1],
    "Outros Custos (R$)": [2, 2, 2, 1.5, 1.5, 0.5, 0.5, 1, 1, 0.5, 0.5, 0.5],
}
df_produtos = pd.DataFrame(produtos_data)
df_produtos["Custo Total (R$)"] = df_produtos["Custo do Fio (R$)"] + df_produtos["Custo de Embalagem (R$)"] + df_produtos["Outros Custos (R$)"]
df_produtos["Margem de Lucro (%)"] = (df_produtos["Preço de Venda (R$)"] - df_produtos["Custo Total (R$)"]) / df_produtos["Preço de Venda (R$)"]

# ============================================================
# 3. PREPARAR ABA VENDAS COM CUSTO E LUCRO
# ============================================================
# Unir com produtos para obter custo unitário (considerando variação Natural como padrão)
# Em caso de múltiplas variações, usaremos a primeira ocorrência (Natural) como referência.
df_vendas = df_vendas.merge(
    df_produtos[["Produto", "Variação/Cor", "Custo Total (R$)"]].rename(columns={"Custo Total (R$)": "Custo Unit"}),
    left_on=["Produto", "Variação"],
    right_on=["Produto", "Variação/Cor"],
    how="left"
)
# Para produtos sem correspondência (ex: Saia, Bolsa), definir custo como 0 ou estimar
df_vendas["Custo Unit"] = df_vendas["Custo Unit"].fillna(0)
df_vendas["Custo Total"] = df_vendas["Qtd"] * df_vendas["Custo Unit"]
df_vendas["Lucro"] = df_vendas["Receita"] - df_vendas["Custo Total"]

# Selecionar colunas para a aba Vendas
df_vendas_final = df_vendas[["Data", "Canal", "Produto", "Variação", "Qtd", "Preco", "Receita", "Custo Unit", "Custo Total", "Lucro", "Metodo", "Obs"]]
df_vendas_final.columns = ["Data", "Canal", "Produto", "Variação", "Qtd", "Preço Unit (R$)", "Receita (R$)", "Custo Unit (R$)", "Custo Total (R$)", "Lucro (R$)", "Método", "Observações"]

# ============================================================
# 4. ATUALIZAR ESTOQUE
# ============================================================
# Estoque inicial conforme planilha fornecida
estoque_inicial = {
    ("Top", "Natural"): 5,
    ("Top", "Terracota"): 5,
    ("Top", "Off-white"): 3,
    ("Biquíni (sutiã)", "Natural"): 8,
    ("Biquíni (sutiã)", "Colorido"): 5,
    ("Faixa de Cabelo", "Natural"): 10,
    ("Faixa Larga Dreads", "Natural"): 6,
    ("Touca Unisex", "Cinza"): 4,
    ("Touca Unisex", "Preta"): 4,
    ("Boné", "Natural"): 2,
    ("Faixa Triangular", "Natural"): 5,
    ("Faixa de Amarrar", "Natural"): 3,
}
# Calcular vendidas por produto e variação
vendas_agg = df_vendas.groupby(["Produto", "Variação"])["Qtd"].sum().to_dict()
# Construir DataFrame de estoque
estoque_list = []
for (prod, var), qtd_ini in estoque_inicial.items():
    vendidas = vendas_agg.get((prod, var), 0)
    produzido = 0  # assumindo que não houve produção adicional no período
    estoque_atual = qtd_ini - vendidas
    status = "❌ Sem estoque" if estoque_atual == 0 else ("⚠️ Crítico" if estoque_atual <= 2 else "✅ OK")
    estoque_list.append([prod, var, qtd_ini, produzido, vendidas, 0, estoque_atual, status])
df_estoque = pd.DataFrame(estoque_list, columns=["Produto", "Variação/Cor", "Estoque Inicial", "Produzido", "Vendido (Feira)", "Vendido (Online)", "Estoque Atual", "Status"])

# ============================================================
# 5. CRIAR ARQUIVO EXCEL FINAL
# ============================================================
output_path = "trupe_br_gestao_atualizado.xlsx"
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    # Aba Produtos (com fórmulas originais)
    df_produtos.to_excel(writer, sheet_name="Produtos", index=False)
    # Aba Estoque
    df_estoque.to_excel(writer, sheet_name="Estoque", index=False)
    # Aba Vendas (todas as vendas)
    df_vendas_final.to_excel(writer, sheet_name="Vendas", index=False)
    # Aba Dashboard (resumo)
    receita_total = df_vendas_final["Receita (R$)"].sum()
    custo_total = df_vendas_final["Custo Total (R$)"].sum()
    lucro_liquido = receita_total - custo_total
    margem_liquida = lucro_liquido / receita_total if receita_total > 0 else 0
    qtd_pecas = df_vendas_final["Qtd"].sum()
    ticket_medio = receita_total / qtd_pecas if qtd_pecas > 0 else 0
    # Receita por canal
    receita_gloria = df_vendas_final[df_vendas_final["Canal"] == "Feira Glória"]["Receita (R$)"].sum()
    receita_lavradio = df_vendas_final[df_vendas_final["Canal"] == "Feira Lavradio"]["Receita (R$)"].sum()
    receita_outros = df_vendas_final[~df_vendas_final["Canal"].isin(["Feira Glória", "Feira Lavradio"])]["Receita (R$)"].sum()
    dashboard_data = {
        "Indicador": ["RECEITA TOTAL", "CUSTO TOTAL", "LUCRO LÍQUIDO", "MARGEM LÍQUIDA", "TICKET MÉDIO", "TOTAL DE PEÇAS VENDIDAS"],
        "Valor": [f"R$ {receita_total:,.2f}", f"R$ {custo_total:,.2f}", f"R$ {lucro_liquido:,.2f}", f"{margem_liquida:.1%}", f"R$ {ticket_medio:.2f}", int(qtd_pecas)],
    }
    df_dashboard = pd.DataFrame(dashboard_data)
    df_dashboard.to_excel(writer, sheet_name="Dashboard", index=False)
    # Adicionar tabela de receita por canal na mesma aba
    canal_data = {
        "Canal": ["Feira Glória", "Feira Lavradio", "Outros/Não identificado"],
        "Receita (R$)": [receita_gloria, receita_lavradio, receita_outros]
    }
    df_canal = pd.DataFrame(canal_data)
    df_canal.to_excel(writer, sheet_name="Dashboard", startrow=10, index=False)
    
    # Abas mensais
    for mes in range(1, 6):  # Janeiro a Maio
        df_mes = df_vendas_final[df_vendas_final["Data"].dt.month == mes].copy()
        if not df_mes.empty:
            nome_mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio"][mes-1]
            df_mes.to_excel(writer, sheet_name=nome_mes, index=False)

# ============================================================
# 6. FORMATAÇÃO (largura, cores, bordas)
# ============================================================
wb = load_workbook(output_path)
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True)

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for col in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        # Ajustar largura
        max_len = 0
        for row in range(1, min(ws.max_row, 100) + 1):
            val = ws.cell(row=row, column=col).value
            if val:
                max_len = max(max_len, len(str(val)))
        ws.column_dimensions[chr(64+col)].width = min(max_len + 2, 30)
    for row in range(2, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            cell = ws.cell(row=row, column=col)
            if isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.alignment = Alignment(horizontal="left")
            cell.border = thin_border
wb.save(output_path)
wb.save(output_path)
print(f"Arquivo gerado: {output_path}")
print(f"Resumo: Receita Total = R$ {receita_total:,.2f}, Lucro = R$ {lucro_liquido:,.2f}, Margem = {margem_liquida:.1%}")