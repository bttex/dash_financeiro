import pandas as pd
import streamlit as st
import altair as alt

# Configurar a página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide", page_icon="💰")

# Carregar os dados do CSV (substitua pelo caminho correto ou upload do arquivo)
dados = pd.read_csv('Extrato.csv', skiprows=4, sep=';')

# Processar os dados
dados['Valor'] = dados['Valor'].str.replace('.', '', regex=False)
dados['Valor'] = dados['Valor'].str.replace(',', '.', regex=False)
dados['Valor'] = pd.to_numeric(dados['Valor'], errors='coerce')
dados['Data Lançamento'] = pd.to_datetime(dados['Data Lançamento'], format='%d/%m/%Y', errors='coerce')
dados = dados.dropna(subset=['Data Lançamento'])
dados['Saldo'] = dados['Valor'].cumsum()
dados['ano_mes'] = dados['Data Lançamento'].dt.to_period('M').dt.to_timestamp()

# Calcular métricas
data_atual = pd.Timestamp.now()
saldo_final = dados['Saldo'].iloc[-1] if not dados.empty else 0
entradas_mes = dados[dados['Valor'] > 0].groupby('ano_mes')['Valor'].sum()
saidas_mes = dados[dados['Valor'] < 0].groupby('ano_mes')['Valor'].sum()

# Layout do dashboard
st.title("💰 Dashboard Financeiro")
st.markdown("Uma visão completa das suas finanças com dados atualizados.")
st.markdown("---")

# Cards de resumo
st.markdown("### Resumo Geral")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Saldo Final", f"R${saldo_final:,.2f}", help="Saldo acumulado até o momento.")

with col2:
    st.metric("Total de Entradas", f"R${entradas_mes.sum():,.2f}", help="Soma total das entradas registradas.")

with col3:
    st.metric("Total de Saídas", f"R${saidas_mes.sum():,.2f}", help="Soma total das saídas registradas.")

st.markdown("---")

# Filtro de datas
st.markdown("### Filtros")
data_min = dados['Data Lançamento'].min()
data_max = dados['Data Lançamento'].max()

intervalo_datas = st.date_input("Selecione o intervalo de datas:", [data_min, data_max], min_value=data_min, max_value=data_max)

if intervalo_datas and len(intervalo_datas) == 2:
    data_inicio = pd.Timestamp(intervalo_datas[0])
    data_fim = pd.Timestamp(intervalo_datas[1])
    dados_filtrados = dados[(dados['Data Lançamento'] >= data_inicio) & (dados['Data Lançamento'] <= data_fim)]
else:
    dados_filtrados = dados

# Gráficos de entradas e saídas
st.markdown("### Análise Mês a Mês")
col1, col2 = st.columns(2)

entradas_filtradas = dados_filtrados[dados_filtrados['Valor'] > 0].groupby('ano_mes')['Valor'].sum()
saidas_filtradas = dados_filtrados[dados_filtrados['Valor'] < 0].groupby('ano_mes')['Valor'].sum()

with col1:
    st.markdown("#### Entradas por Mês")
    entradas_chart = alt.Chart(entradas_filtradas.reset_index()).mark_bar(color='#2ecc71').encode(
        x=alt.X('ano_mes:T', title='Mês'),
        y=alt.Y('Valor:Q', title='Entradas')
    ).properties(height=300)
    st.altair_chart(entradas_chart, use_container_width=True)

with col2:
    st.markdown("#### Saídas por Mês")
    saidas_chart = alt.Chart(saidas_filtradas.reset_index()).mark_bar(color='#e74c3c').encode(
        x=alt.X('ano_mes:T', title='Mês'),
        y=alt.Y('Valor:Q', title='Saídas')
    ).properties(height=300)
    st.altair_chart(saidas_chart, use_container_width=True)

st.markdown("---")

# Gráfico de saldo acumulado
st.markdown("### Evolução do Saldo Acumulado")
saldo_mes = dados_filtrados.groupby('ano_mes')['Saldo'].max().reset_index()

saldo_chart = alt.Chart(saldo_mes).mark_area(opacity=0.3, color="#3498db").encode(
    x=alt.X('ano_mes:T', title='Mês'),
    y=alt.Y('Saldo:Q', title='Saldo Acumulado')
).properties(height=400)

st.altair_chart(saldo_chart, use_container_width=True)

# Análise por Histórico (se aplicável)
if 'Histórico' in dados_filtrados.columns:
    st.markdown("### Análise por Histórico")
    historico = dados_filtrados.groupby('Histórico')['Valor'].sum().reset_index()
    historico_chart = alt.Chart(historico).mark_bar().encode(
        x=alt.X('Valor:Q', title='Total por Histórico'),
        y=alt.Y('Histórico:N', title='Histórico', sort='-x'),
        color=alt.Color('Histórico:N', legend=None)
    ).properties(height=400)
    st.altair_chart(historico_chart, use_container_width=True)

# Mostrar detalhes dos dados
st.markdown("---")
st.markdown("### Detalhes dos Dados")
st.dataframe(dados_filtrados)

# Observação sobre melhorias
st.markdown(
    """
    <style>
        div[data-testid="metric-container"] {
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid #CCC;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)
