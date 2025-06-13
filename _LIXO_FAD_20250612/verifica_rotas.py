import os
import pandas as pd
import requests
from requests.exceptions import RequestException

# Defina os caminhos completos para o arquivo de entrada e saída
input_file = r"C:\Users\vinic\fad_espacial\auditoria_rotas_fad_ATUALIZADA.xlsx"
output_file = r"C:\Users\vinic\fad_espacial\auditoria_rotas_fad_ATUALIZADA_result.xlsx"
sheet_name = "Rotas OK (HTML + API)"

# Verifica se o arquivo de entrada existe
if not os.path.exists(input_file):
    print("Arquivo de entrada não encontrado:", input_file)
    exit(1)

# Leitura da planilha do Excel
try:
    df = pd.read_excel(input_file, sheet_name=sheet_name)
except Exception as e:
    print(f"Erro ao ler a planilha: {e}")
    exit(1)

# Garante que as colunas 'Funcionando?' e 'MENSAGEM' existam
if 'Funcionando?' not in df.columns:
    df['Funcionando?'] = ""
if 'MENSAGEM' not in df.columns:
    df['MENSAGEM'] = ""
else:
    # Converte a coluna "MENSAGEM" para string para evitar warnings de dtype
    df['MENSAGEM'] = df['MENSAGEM'].astype(str)

# Itera por cada linha da planilha
for index, row in df.iterrows():
    url = row['URL acesso']
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            df.at[index, 'Funcionando?'] = "SIM"
            df.at[index, 'MENSAGEM'] = ""
        else:
            df.at[index, 'Funcionando?'] = "NÃO"
            df.at[index, 'MENSAGEM'] = f"Código {response.status_code}: {response.reason}"
    except RequestException as e:
        df.at[index, 'Funcionando?'] = "NÃO"
        df.at[index, 'MENSAGEM'] = str(e)

# Exibe o caminho onde o arquivo de saída será salvo (útil para debug)
print("Salvando arquivo em:", output_file)

# Tenta salvar a planilha atualizada
try:
    df.to_excel(output_file, sheet_name=sheet_name, index=False)
    print(f"Verificação completa. Arquivo salvo em: {output_file}")
except Exception as e:
    print("Erro ao salvar o arquivo:", e)
