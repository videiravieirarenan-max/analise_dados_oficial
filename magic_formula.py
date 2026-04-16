import requests
import pandas as pd
import yfinance as yf
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTUzNjQ1LCJpYXQiOjE3NzU1NjE2NDUsImp0aSI6IjdhNmQ1NzQyODY0NjQ4ODdiMDcxNzU3NzUzMDRhZDkzIiwidXNlcl9pZCI6IjExNyJ9.4O_WXBF-tfRDNN-58Uj_HrXCwcWdUvEUvBxFuwlmgXE"
base_url = "https://laboratoriodefinancas.com/planilhao"

headers = {"Authorization": f"Bearer {token}"}

data_inicio="2021-04-01"
data_fim = "2026-04-01"

# 1. Pegar dados do 'Planilhão'
resp = requests.get(f"{base_url}/bolsa/planilhao", headers=headers, params={"data_base": data_inicio})
df = pd.DataFrame(resp.json())


if not df.empty:
    # Limpeza e Ranking (Removendo valores nulos para o rank funcionar)
    df2 = df[["ticker", "roic", "earning_yield"]].dropna().copy()
    df2['rank_roic'] = df2["roic"].rank(ascending=False)
    df2['rank_ey'] = df2["earning_yield"].rank(ascending=False)
    df2["rank_final"] = df2['rank_roic'] + df2['rank_ey']

    # Pegamos as 5 melhores
    top_5_df = df2.sort_values("rank_final").head(5)
    lista_tickers = [f"{t}.SA" for t in top_5_df['ticker'].tolist()]


print(f"Top 5 Ações em {data_inicio}: {lista_tickers}")


    # 2. Cálculo de Performance
retornos = []
    
    # Download em lote é mais rápido e estável
    # group_by='column' ajuda a lidar com o MultiIndex do yfinance
# O jeito certo:

dados_hist = yf.download(lista_tickers, start="2021-04-01", end="2026-03-26")
for ticker in lista_tickers:
        try:
            # Acessando Adj Close tratando o MultiIndex: dados_hist['Adj Close'][ticker]
            # Usamos dropna() para garantir que pegamos o primeiro e último preço válido
            serie_precos = dados_hist['Adj Close'][ticker].dropna()
            
            if not serie_precos.empty:
                p_ini = serie_precos.iloc[0]
                p_fim = serie_precos.iloc[-1]
                performance = (p_fim / p_ini) - 1
                retornos.append(performance)
                print(f"{ticker}: {performance:.2%}")
        except Exception as e:
            print(f"Erro ao calcular {ticker}: {e}")

    # Resultado Final
    if retornos:
        media_retorno_magic = sum(retornos) / len(retornos)
        
        # 3. Comparação com Ibovespa
        ibov = yf.download("^BVSP", start=data_inicio, end=index=data_fim)['Adj Close']
        ibov = ibov.dropna()
        retorno_ibov = (ibov.iloc[-1] / ibov.iloc[0]) - 1

        print("-" * 30)
        print(f"Retorno Médio Magic Formula: {media_retorno_magic:.2%}")
        print(f"Retorno Ibovespa: {retorno_ibov:.2%}")
    else:
        print("Nenhum dado de retorno foi coletado.")