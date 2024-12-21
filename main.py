import pandas as pd
import streamlit as st
import altair as alt

# Configurar a página
st.set_page_config(page_title="Dashboard Financeiro", layout="centered")

# Carregar os dados do CSV (substitua pelo caminho correto ou upload do arquivo)
dados = pd.read_csv('Extrato.csv', skiprows=4, sep=';')

# Processar os dados
dados['Valor'] = dados['Valor'].str.replace('.', '', regex=False)
dados['Valor'] = dados['Valor'].str.replace(',', '.', regex=False)
dados['Valor'] = pd.to_numeric(dados['Valor'], errors='coerce')
dados['Data Lançamento'] = pd.to_datetime(dados['Data Lançamento'], format='%d/%m/%Y', errors='coerce')
dados = dados.dropna(subset=['Data Lançamento'])
dados['Saldo'] = dados['Valor'].cumsum()
dados['ano_mes'] = dados['Data Lançamento'].dt.strftime('%Y-%m')

# Calcular métricas
data_atual = pd.to_datetime('today')
dados_hoje = dados[dados['Data Lançamento'] <= data_atual]
saldo_final = dados['Saldo'].iloc[-1] if not dados.empty else 0
entradas_mes = dados[dados['Valor'] > 0].groupby('ano_mes')['Valor'].sum()
saidas_mes = dados[dados['Valor'] < 0].groupby('ano_mes')['Valor'].sum()

# Layout do dashboard
st.title("Dashboard Financeiro")

col1, col2, col3 = st.columns(3)

# Card de saldo final
with col1:
    st.markdown(f"""
    <div style="background-color: #2ecc71; color: white; padding: 15px; border-radius: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); text-align: center; width: 230px; height: 150px;">
        <h3>Saldo Final</h3>
        <p style="font-size: 18px;">R${saldo_final:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Card de total de entradas
with col2:
    st.markdown(f"""
    <div style="background-color: #3498db; color: white; padding: 10px; border-radius: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); text-align: center; width: 230px; height: 150px;">
        <h3>Total de Entradas</h3>
        <p style="font-size: 18px;">R${entradas_mes.sum():,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Card de total de saídas
with col3:
    st.markdown(f"""
    <div style="background-color: #e74c3c; color: white; padding: 15px; border-radius: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); text-align: center; width: 230px; height: 150px;">
        <h3>Total de Saídas</h3>
        <p style="font-size: 18px;">R${saidas_mes.sum():,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Gráficos
st.subheader("Análise Mês a Mês")

col1, col2 = st.columns(2)

# Gráfico de entradas
with col1:
    st.markdown("### Entradas por Mês")
    entradas_chart = alt.Chart(entradas_mes.reset_index()).mark_bar(color='green').encode(
        x=alt.X('ano_mes:T', title='Mês'),
        y=alt.Y('Valor:Q', title='Entradas')
    ).properties(width=400, height=300)
    st.altair_chart(entradas_chart, use_container_width=True)

# Gráfico de saídas
with col2:
    st.markdown("### Saídas por Mês")
    saidas_chart = alt.Chart(saidas_mes.reset_index()).mark_bar(color='red').encode(
        x=alt.X('ano_mes:T', title='Mês'),
        y=alt.Y('Valor:Q', title='Saídas')
    ).properties(width=400, height=300)
    st.altair_chart(saidas_chart, use_container_width=True)

# Saldo acumulado por mês
st.subheader("Evolução do Saldo Acumulado por Mês")
saldo_mes = dados.groupby('ano_mes')['Saldo'].max().reset_index()  # Agora é por mês

saldo_chart = alt.Chart(saldo_mes).mark_area(opacity=0.3, color="#9b59b6").encode(
    x=alt.X('ano_mes:T', title='Mês'),
    y=alt.Y('Saldo:Q', title='Saldo Acumulado')
).properties(width=800, height=400)

st.altair_chart(saldo_chart, use_container_width=True)

# Análise por Histórico (Exemplo)
st.subheader("Análise por Histórico")
if 'Histórico' in dados.columns:
    historico = dados.groupby('Histórico')['Valor'].sum().reset_index()
    historico_chart = alt.Chart(historico).mark_bar().encode(
        x=alt.X('Valor:Q', title='Total por Histórico'),
        y=alt.Y('Histórico:N', title='Histórico', sort='-x'),
        color=alt.Color('Histórico:N', legend=None)
    ).properties(width=800, height=400)
    st.altair_chart(historico_chart, use_container_width=True)
else:
    st.warning("Os dados não possuem a coluna 'Histórico' para análise por histórico.")

# Detalhes dos dados
st.write("### Detalhes dos Dados")
st.dataframe(dados)
