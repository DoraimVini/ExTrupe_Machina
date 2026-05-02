import pandas as pd
import os

def check_result():
    file_path = 'trupe_br_gestao.xlsx'
    df_estoque = pd.read_excel(file_path, sheet_name='Estoque', header=1)
    
    # Procurar por 'Boné'
    bone_row = df_estoque[df_estoque['Produto'].astype(str).str.contains('Bon[ée]', case=False, regex=True)]
    
    if not bone_row.empty:
        print("Dados do Boné no Estoque:")
        for col in bone_row.columns:
            val = bone_row.iloc[0][col]
            # Evitar erro de encoding no print
            print(f"{col}: {val}")
    else:
        print("Boné não encontrado no Estoque.")

if __name__ == "__main__":
    check_result()
