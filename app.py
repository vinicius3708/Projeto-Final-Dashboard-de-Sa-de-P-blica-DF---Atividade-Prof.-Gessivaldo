import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard Saúde DF", layout="wide")
st.title("📊 Dashboard de Atendimentos - DF")

@st.cache_data
def carregar_e_limpar_dados():
    # Carrega o CSV original
    df = pd.read_csv("SIA042018.csv", sep=None, engine='python', encoding='latin1', on_bad_lines='skip')
    
    # Dicionário de renomeação para garantir que o código sempre encontre o que precisa
    # Se o CSV vier com 'estabelecimento_cnes', ele vira 'estabelec'
    df = df.rename(columns={
        'estabelecimento_cnes': 'estabelec',
        'estabelecimento': 'estabelec'
    })
    
    # Função para limpar os caracteres (aquela que corrigiu as letras)
    def limpar_caracteres(texto):
        try:
            return str(texto).encode('latin1').decode('utf-8', 'ignore').upper()
        except:
            return str(texto).upper()

    # Aplica a limpeza nas colunas de texto
    if 'estabelec' in df.columns:
        df['estabelec'] = df['estabelec'].apply(limpar_caracteres)
    if 'procedimento' in df.columns:
        df['procedimento'] = df['procedimento'].apply(limpar_caracteres)
        
    return df

# Executa o carregamento
df = carregar_e_limpar_dados()

# Exibe a tabela
st.subheader("Dados dos Atendimentos")
st.dataframe(df, use_container_width=True)

# GERAÇÃO DO GRÁFICO (Com verificação de segurança)
if 'estabelec' in df.columns:
    st.subheader("Atendimentos por Estabelecimento")
    
    # Agrupa e conta. Se não houver uma coluna específica, conta as linhas
    contagem = df.groupby('estabelec').size()
    
    # Exibe o gráfico de barras
    st.bar_chart(contagem)
else:
    st.error("A coluna 'estabelec' não foi encontrada no arquivo. Verifique os dados.")