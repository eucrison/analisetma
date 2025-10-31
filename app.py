# ===============================================
# app.py
# ===============================================
import streamlit as st
import pandas as pd
import requests as rq

st.set_page_config(page_title="Análise de Tickets e TMA", layout="wide")

st.sidebar.title("📂 Navegação")
menu = st.sidebar.radio(
    "Escolha uma seção:",
    ["Upload & Resumo", "Rankings", "Gráficos", "🔍 Insights Automáticos"]
)

uploaded_file = st.sidebar.file_uploader("Envie o arquivo CSV", type=["csv"])

if uploaded_file:
    df = rq.load_data(uploaded_file)
    st.sidebar.success(f"Arquivo carregado: {len(df)} registros")

    if menu == "Upload & Resumo":
        st.title("📈 Resumo Geral dos Dados")
        resumo = rq.resumo_geral(df)
        st.table(pd.DataFrame(resumo.items(), columns=["Indicador", "Valor"]))

    elif menu == "Rankings":
        st.title("🏅 Rankings de Agentes")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 - Maior Volume de Tickets")
            st.dataframe(rq.top_agentes_qtd(df))
        with col2:
            st.subheader("Top 10 - Menor e Maior TMA Médio")
            menor, maior = rq.top_agentes_tma(df)
            st.write("**Menor TMA**")
            st.dataframe(menor)
            st.write("**Maior TMA**")
            st.dataframe(maior)

    elif menu == "Gráficos":
        st.title("📊 Visualizações de Desempenho")

        st.subheader("Distribuição Geral do TMA")
        st.pyplot(rq.grafico_boxplot_tma(df))

        st.subheader("Relação entre Produtividade e Tempo Médio")
        st.pyplot(rq.grafico_dispersa_produtividade(df))

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("TMA por Produto")
            st.pyplot(rq.grafico_barra_media(df, "produto", "Produto"))
        with col4:
            st.subheader("TMA por Jornada")
            st.pyplot(rq.grafico_barra_media(df, "jornada", "Jornada"))

    elif menu == "🔍 Insights Automáticos":
        st.title("🔍 Insights Automáticos")
        insights = rq.gerar_insights(df)
        for item in insights:
            st.markdown(f"- {item}")

else:
    st.info("👈 Faça o upload de um arquivo CSV para iniciar a análise.")
