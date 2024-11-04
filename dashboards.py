import streamlit as st  # Importa Streamlit para criar aplicações web interativas
# pip install streamlit
# Para executar digite: steamlit run (Nome do projeto) - streamlit run dashboards.py
# Acesse o Link: http://localhost:8501 no navegador
import pandas as pd  # Importa Pandas para manipulação de dados
import plotly.express as px  # Importa Plotly Express para criação de gráficos interativos
# pip install plotly

# Configura o layout da página para ocupar toda a tela
st.set_page_config(layout="wide") 

# Lê o arquivo CSV com dados de vendas
df = pd.read_csv("vendas_supermercado.csv", sep=";", decimal=",") 
df["Data"] = pd.to_datetime(df["Data"])  # Converte a coluna "Data" para o formato de data
df = df.sort_values("Data")  # Ordena os dados por data

# Cria uma nova coluna "Month" com o formato "ano-mês"
df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month)) 
# Cria uma caixa de seleção para escolher o mês
month = st.sidebar.selectbox("Mês", df["Mês"].unique()) 

# Filtra os dados para incluir apenas o mês selecionado
df_filtered = df[df["Mês"] == month]

# Cria colunas para organizar os gráficos
col1, col2 = st.columns(2)  # Duas colunas
col3, col4, col5 = st.columns(3)  # Três colunas

# Gráfico de faturamento por dia
fig_date = px.bar(df_filtered, x="Data", y="Total", color="Cidade", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)  # Plota o gráfico na primeira coluna

# Gráfico de faturamento por tipo de produto
fig_prod = px.bar(df_filtered, x="Data", y="Linha de Produtos", 
                  color="Cidade", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)  # Plota o gráfico na segunda coluna

# Gráfico de faturamento total por filial
city_total = df_filtered.groupby("Cidade")[["Total"]].sum().reset_index()  # Agrupa por cidade e soma o total
fig_city = px.bar(city_total, x="Cidade", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)  # Plota o gráfico na terceira coluna

# Gráfico de faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Pagamento", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)  # Plota o gráfico na quarta coluna

# Gráfico de avaliação média das filiais
city_total = df_filtered.groupby("Cidade")[["Avaliacao"]].mean().reset_index()  # Agrupa por cidade e calcula a média da avaliação
fig_rating = px.bar(city_total, y="Avaliacao", x="Cidade", title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)  # Plota o gráfico na quinta coluna