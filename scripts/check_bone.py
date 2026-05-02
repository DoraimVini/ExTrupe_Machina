import pandas as pd
import os

def check_bone():
    file_path = 'trupe_br_gestao.xlsx'
    if not os.path.exists(file_path):
        print("Arquivo não encontrado")
        return

    xl = pd.ExcelFile(file_path)
    for sheet in xl.sheet_names:
        print(f"\n--- Analisando aba: {sheet} ---")
        # Tentando ler com header=1 caso seja o padrao do projeto
        try:
            df = pd.read_excel(xl, sheet_name=sheet, header=1)
        except:
            df = pd.read_excel(xl, sheet_name=sheet)
            
        # Procurar por 'Boné' ou 'Bone'
        mask = df.astype(str).apply(lambda x: x.str.contains('Bon[ée]', case=False, regex=True))
        matches = df[mask.any(axis=1)]
        
        if not matches.empty:
            print(f"Encontrado na aba {sheet}:")
            # Convertendo para dict para evitar erro de encoding no print do dataframe
            print(matches.to_dict('records'))
        else:
            print("Nenhum 'Boné' encontrado.")

if __name__ == "__main__":
    check_bone()
