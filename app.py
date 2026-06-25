import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard Saúde DF", layout="wide")
st.title("📊 Dashboard de Atendimentos - DF")

conn_str = "mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};SERVER=.;DATABASE=SaudePublicaDF;Trusted_Connection=yes;"

@st.cache_data
def carregar_dados():
    engine = create_engine(conn_str)
    # Lemos os dados como bytes para evitar que o Windows altere os acentos
    df = pd.read_csv("SIA042018.csv", sep=None, engine='python', encoding='latin1')
    
    # Esta função limpa o texto sem usar bibliotecas complicadas
    def limpar_caracteres(texto):
        if pd.isna(texto): return "OUTROS"
        # Converte para string
        t = str(texto)
        # O segredo: tratar como Latin-1 e corrigir para UTF-8
        try:
            return t.encode('latin1').decode('utf-8', 'ignore').upper()
        except:
            return t.upper()

    df['estabelec'] = df['estabelec'].apply(limpar_caracteres)
    df['procedimento'] = df['procedimento'].apply(limpar_caracteres)
    return df

try:
    df = carregar_dados()
    st.dataframe(df, use_container_width=True)
    
    resumo = df.groupby('estabelec')['quantidade_atendimentos'].sum().reset_index()
    st.bar_chart(resumo.set_index('estabelec'))

except Exception as e:
    st.write("Erro:", e)