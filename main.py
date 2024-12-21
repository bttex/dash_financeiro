import pandas as pd
import streamlit as st

# Carregar os dados do CSV (substitua pelo caminho do seu arquivo)
dados = pd.read_csv('Extrato.csv', skiprows=4, sep=';')

# Garantir que a coluna 'Valor' está no formato numérico
dados['Valor'] = dados['Valor'].str.replace('.', '', regex=False)
dados['Valor'] = dados['Valor'].str.replace(',', '.', regex=False)
dados['Valor'] = pd.to_numeric(dados['Valor'], errors='coerce')

# Calcular o saldo acumulado
dados['Saldo'] = dados['Valor'].cumsum()

# Converter a coluna 'Data Lançamento' para o formato datetime
dados['Data Lançamento'] = pd.to_datetime(dados['Data Lançamento'], format='%d/%m/%Y', errors='coerce')

# Remover linhas com datas inválidas
dados = dados.dropna(subset=['Data Lançamento'])

# Filtrar os dados até hoje
data_atual = pd.to_datetime('today')
dados_hoje = dados[dados['Data Lançamento'] <= data_atual]

# Obter o saldo final mais recente
saldo_final_hoje = dados_hoje['Saldo'].iloc[-1] if not dados_hoje.empty else 0





# Exibir o saldo final


# Criar uma coluna de ano-mês para agrupamento
dados['ano_mes'] = dados['Data Lançamento'].dt.strftime('%Y-%m')

# Entradas mês a mês
entradas_mes = dados[dados['Valor'] > 0].groupby('ano_mes')['Valor'].sum()
entradas_mes.index = pd.to_datetime(entradas_mes.index + '-01')  # Adicionar dia 01 para converter para datetime

# Saídas mês a mês
saidas_mes = dados[dados['Valor'] < 0].groupby('ano_mes')['Valor'].sum()
saidas_mes.index = pd.to_datetime(saidas_mes.index + '-01')  # Adicionar dia 01 para converter para datetime

dados['saldo_mes'] = dados.groupby('ano_mes')['Saldo'].transform('max')

# Encontrar o mês anterior
dados['ano_mes_anterior'] = dados['Data Lançamento'] - pd.DateOffset(months=1)
dados['ano_mes_anterior'] = dados['ano_mes_anterior'].dt.strftime('%Y-%m')

# Combinar com os saldos do mês anterior
dados_ano_mes_anterior = dados[['Data Lançamento', 'saldo_mes', 'ano_mes_anterior']].dropna(subset=['ano_mes_anterior'])

# Obter o saldo do mês anterior para comparação
dados_ano_mes_anterior = dados_ano_mes_anterior.merge(
    dados[['ano_mes', 'saldo_mes']],
    left_on='ano_mes_anterior', right_on='ano_mes',
    suffixes=('_atual', '_anterior')
)

# Calcular a variação percentual corretamente
dados_ano_mes_anterior['variacao_percentual'] = (
    (dados_ano_mes_anterior['saldo_mes_atual'] - dados_ano_mes_anterior['saldo_mes_anterior']) 
    / abs(dados_ano_mes_anterior['saldo_mes_anterior'])  # Garantir que o denominador não seja zero
) * 100

# Exibir a variação percentual para o mês atual
variacao_percentual_hoje = dados_ano_mes_anterior['variacao_percentual'].iloc[-1] if not dados_ano_mes_anterior.empty else 0

st.metric(label="Saldo Final de Hoje", value=f"R${saldo_final_hoje:,.2f}",delta=f"{variacao_percentual_hoje:.2f}")

# Exibir a variação percentual com o sinal correto
if variacao_percentual_hoje > 0:
    st.metric(label="Aumento Percentual em Relação ao Mês Anterior", value=f"{variacao_percentual_hoje:.2f}%")
elif variacao_percentual_hoje < 0:
    st.metric(label="Queda Percentual em Relação ao Mês Anterior", value=f"{variacao_percentual_hoje:.2f}%")
else:
    st.metric(label="Variação Percentual em Relação ao Mês Anterior", value="0.00%")



# Criar gráficos
st.subheader("Entradas mês a mês")
chart_data_entradas = pd.DataFrame({
    'valor': entradas_mes.values
}, index=entradas_mes.index)
st.bar_chart(chart_data_entradas)

st.subheader("Saídas mês a mês")
chart_data_saidas = pd.DataFrame({
    'valor': saidas_mes.values
}, index=saidas_mes.index)
st.bar_chart(chart_data_saidas)

# Calcular o saldo do mesmo dia do mês anterior
# Obter o saldo acumulado por mês

