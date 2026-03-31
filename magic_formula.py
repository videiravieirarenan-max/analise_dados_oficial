import requests
import pandas as pd
from yfinance import ticker

base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3NTQ4MDkxLCJpYXQiOjE3NzQ5NTYwOTEsImp0aSI6IjY4OGUxYWVkZGFiNjQ1YjliMmUzMDgxMjliNDI0YzkyIiwidXNlcl9pZCI6IjExNyJ9.cDKVcsGJ8krkyEc5-UTNNMA6uefmEQH2dckZCP9QbUU"
resp = requests.get(
    f"{base_url}/bolsa/planilhao",
    headers={"Authorization": f"Bearer {token}"},
    params={"data_base": "2021-04-01"},
)

dados= resp.json()
df= pd.DataFrame(dados)
print(df.head())

df2 = df[["ticker","roic","earning_yield"]]
df2['rank_roic'] = df2["roic"].rank(ascending=False)
df2['rank_p_ey'] = df2["earning_yield"].rank(ascending=False)
df2["rank_final"] = (df2['rank_roic'] + df2['rank_p_ey'])
df2.sort_values("rank_final", ascending=False)['ticker'][:20]

#api para pegar o preço das ações
base_url = "https://laboratoriodefinancas.com/api/v2"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3NTQ4MDkxLCJpYXQiOjE3NzQ5NTYwOTEsImp0aSI6IjY4OGUxYWVkZGFiNjQ1YjliMmUzMDgxMjliNDI0YzkyIiwidXNlcl9pZCI6IjExNyJ9.cDKVcsGJ8krkyEc5-UTNNMA6uefmEQH2dckZCP9QbUU"
params= {"tickers":"BBSE3","DATA_INI":"2021-04-01","DATA_FIM":"2026-03-26"}
resp = requests.get(
    f"{base_url}/PREÇO/CORRIGIDO",
    headers={"Authorization": f"Bearer {token}"},
    params=params,
)

df_preço = pd.DataFrame(resp.json())

# Preço Final

filtro1=df_preço["data"]=="2026-3-23"
preço_final = df_preço.loc[filtro1,]
preço_final= float(preço_final)

#filtro inicial
filtro2=df_preço["data"]=="2021-03-22"
preço_inicial= df_preço.loc[filtro2,'fechamento'].iloc[0]
preço_final/preço_inicial - 1

#api
import yfinance as yf
#get ticker data
ibov = yf.download("^BVSP", start="2001-01-01", end="2026-03-31")
#preço Inicial
filtro1 = ibov.index == "2001-01-01"
preço_inicial = ibov.loc[filtro1, 'Adj Close'].iloc[0]
#preço final
filtro2=ibov[ibov.index == "2026-03-30"]
ibov_fim = ibov.loc[filtro2, 'Adj Close'].iloc[0]
#preço final
filtro2 + ibov.index == "2026-03-30"
ibov_fim = ibov [filtro2] ["close"].iloc[0]
#retorno
ibov_fim/preço_inicial - 1