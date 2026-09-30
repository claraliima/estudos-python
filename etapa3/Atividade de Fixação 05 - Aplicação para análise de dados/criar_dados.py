import pandas as pd
import numpy as np

np.random.seed(42)

# --- 1. GERAÇÃO DO ARQUIVO: transacoes.csv ---
datas_transacoes = pd.date_range(start='2026-09-01', periods=1000, freq='h')

df_transacoes = pd.DataFrame({
    'id_cliente': np.random.choice(['C100', 'C101', 'C102', 'C103', 'C104'], size=1000),
    'data_transacao': datas_transacoes,
    'valor': np.random.choice(
        [np.nan, 150.0, 3000.0, 7500.0, 12000.0, 50.0], 
        size=1000, 
        p=[0.05, 0.40, 0.30, 0.15, 0.05, 0.05]
    ),
    'estado_cliente': np.random.choice(['SP', 'RJ', 'MG', 'RS'], size=1000),
    'origem': np.random.choice(['web', 'mobile_app', 'atm'], size=1000)
})

df_transacoes = pd.concat([df_transacoes, df_transacoes.iloc[:15]], ignore_index=True)

df_transacoes.to_csv('transacoes.csv', index=False, encoding='latin1')


# 2. GERAÇÃO DO ARQUIVO: cotacoes.csv ---
datas_cotacoes = pd.date_range(start='2026-09-01', end='2026-10-01', freq='D')

variacoes = np.random.normal(loc=0.001, scale=0.015, size=len(datas_cotacoes))
preco_inicial = 5.20
precos = preco_inicial * np.exp(np.cumsum(variacoes))

df_cotacoes = pd.DataFrame({
    'data': datas_cotacoes,
    'cotacao_usd': np.round(precos, 4),
    'volume_negociado': np.random.randint(10000, 500000, size=len(datas_cotacoes))
})

df_cotacoes.loc[5, 'cotacao_usd'] = np.nan
df_cotacoes.loc[18, 'cotacao_usd'] = np.nan

df_cotacoes.to_csv('cotacoes.csv', index=False, encoding='utf-8')

print("Arquivos 'transacoes.csv' e 'cotacoes.csv' gerados com sucesso!")

# 3. Ingestão, Performance e Limpeza:

# O arquivo veio com encoding legado (latin1). Garanta a correta leitura sem corromper caracteres.
df_transacoes = pd.read_csv("transacoes.csv", encoding="latin1") 
df_cotacoes = pd.read_csv("cotacoes.csv", encoding="latin1") 

# Trate os valores ausentes (NaN) no campo valor imputando a mediana por estado.
df_transacoes["valor"] = df_transacoes["valor"].fillna(df_transacoes.groupby("estado_cliente")["valor"].transform("median"))

# Crie uma nova coluna chamada plataforma com valor estático 'Mobile' para rastreabilidade do pipeline.
df_transacoes["plataforma"] = "Mobile"

# 4. Engenharia de Dados & Alinhamento Temporável

# Converta a coluna data_transacao para o tipo datetime64[ns] e aplique a fuso horário 'America/Sao_Paulo' (tz_localize).
df_transacoes["data_transacao"] = pd.to_datetime(df_transacoes["data_transacao"])
df_transacoes["data_transacao"] = df_transacoes["data_transacao"].dt.tz_localize("America/Sao_Paulo")

#Adicione uma coluna identificando o dia da semana e o mês das transações utilizando o acessor .dt.
df_transacoes["dia_transacao"] = df_transacoes["data_transacao"].dt.day
df_transacoes["mes_transacao"] = df_transacoes["data_transacao"].dt.month

# Descarte transações duplicadas mantendo apenas a primeira ocorrência.
df_transacoes = df_transacoes.drop_duplicates(keep="first")

# 5. Operações Vetorizadas e Filtros Bitwise

filtro = (
    (df_transacoes["mes_transacao"] == 9) &
    ((df_transacoes["estado_cliente"] == "SP") | (df_transacoes["estado_cliente"] == "RJ")) &
    (df_transacoes["valor"] > 5000)
)

df_transacoes_filtrado = df_transacoes[filtro]

# 6. Cruzamento de Dados & Agregação:

risco_dict = {
    "C100": "Baixo",
    "C101": "Alto",
    "C102": "Médio",
    "C103": "Baixo",
    "C104": "Alto"
}

df_transacoes["nivel_risco"] = df_transacoes["id_cliente"].map(risco_dict)

df_transacoes_pivotado = df_transacoes.pivot_table(
    values="valor",
    index="mes_transacao",
    columns="nivel_risco",
    aggfunc="sum", 
    margins = True
)

# 7. Detecção Estatística de Outliers (Z-Score)
df_transacoes["z_score"] = (
    (df_transacoes["valor"] - df_transacoes.groupby("estado_cliente")["valor"].transform("mean"))
    / df_transacoes.groupby("estado_cliente")["valor"].transform("std")
)

df_transacoes_anomalias = df_transacoes[(df_transacoes["z_score"] > 2.5)]

# 8. Visualização Gráfica Orientada a Objetos (Matplotlib):
import matplotlib.pyplot as plt

# Agrupar o valor total de transações por dia
transacoes_diarias = (
    df_transacoes
    .groupby(df_transacoes["data_transacao"].dt.date)["valor"]
    .sum()
)

# Calcular a média móvel de 7 dias
media_movel_7 = transacoes_diarias.rolling(7).mean()

# Criar o gráfico usando a API Orientada a Objetos
fig, ax = plt.subplots(figsize=(12, 6))

# Linha do valor total diário
ax.plot(
    transacoes_diarias.index,
    transacoes_diarias.values,
    label="Valor total diário"
)

# Linha da média móvel de 7 dias
ax.plot(
    media_movel_7.index,
    media_movel_7.values,
    label="Média móvel de 7 dias"
)

# Fazer o eixo Y começar em zero
ax.set_ylim(bottom=0)

# Título e legendas
ax.set_title("Valor Total de Transações por Dia")
ax.set_xlabel("Data")
ax.set_ylabel("Valor das Transações (R$)")
ax.legend()

# Melhorar a visualização
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

print(df_transacoes.head())
print(df_transacoes_filtrado.head())
print(df_transacoes_pivotado.head())
print(df_transacoes_anomalias.head())