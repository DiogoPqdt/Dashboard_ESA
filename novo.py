import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale
from datetime import datetime
import streamlit as st 
from streamlit_extras.metric_cards import style_metric_cards 
import requests

# -----------------------
# FUNÇÕES
# -----------------------

# Como a função style_metric_cards já foi importada, não há necessidade de redefini-la.

st.set_page_config(page_title='Dash ESA 2023', 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

# Definindo a configuração local para o Brasil (pt_BR)
# Verificar se o sistema suporta 'pt_BR.UTF-8', caso contrário, use um código local compatível
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

# Definindo o ANO ATUAL para filtro
ano_atual = str(datetime.now().year)


# -----------------------
# TRATAMENTO DOS DADOS
# -----------------------

# Caminhos para os arquivos .CSV
caminho_1 = r"C:\Users\User\OneDrive\Trabalho\ESA 2024\Dashboard_ESA\base_dados\Cel Manfrini.csv"
caminho_2 = r"C:\Users\User\OneDrive\Trabalho\ESA 2024\Dashboard_ESA\base_dados\Cel Manfrini(1).csv"
caminho_3 = r"C:\Users\User\OneDrive\Trabalho\ESA 2024\Dashboard_ESA\base_dados\Cel Manfrini(2).csv"
caminho_4 = r"C:\Users\User\OneDrive\Trabalho\ESA 2024\Dashboard_ESA\base_dados\Cel Manfrini(3).csv"

@st.cache_data
def load_data(caminho_1, caminho_2, caminho_3, caminho_4):
    try:
        # Leitura dos arquivos .CSV em DataFrames individuais
        df1 = pd.read_csv(caminho_1)
        df2 = pd.read_csv(caminho_2)
        df3 = pd.read_csv(caminho_3)
        df4 = pd.read_csv(caminho_4)
    except FileNotFoundError as e:
        st.error(f"Erro: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio se houver erro

    # Concatenação dos DataFrames em um único DataFrame
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)

    # Excluindo linhas que contenham a string "Tela" em qualquer coluna
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Tela')).any(axis=1)]
    
     # Inserindo _ nos titulos das colunas
    df.columns = df.columns.str.replace(' ', '_')

    # Transformando o tipo de dado das colunas de valores monetários com tratamento de erros
    df['A_LIQUIDAR'] = pd.to_numeric(df['A_LIQUIDAR'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
    df['LIQUIDADO_A_PAGAR'] = pd.to_numeric(df['LIQUIDADO_A_PAGAR'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
    df['TOTAL_A_PAGAR'] = pd.to_numeric(df['TOTAL_A_PAGAR'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
    df['PAGO'] = pd.to_numeric(df['PAGO'].str.replace('.', '').str.replace(',', '.'), errors='coerce')

    # Convertendo a coluna DATA para datetime com quatro dígitos no ano
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce')

    # Convertendo a coluna DIAS em número inteiro com tratamento de erro
    df['DIAS'] = pd.to_numeric(df['DIAS'], errors='coerce').fillna(0).astype(int)
    
    return df

# Carregando os dados
df = load_data(caminho_1=caminho_1, caminho_2=caminho_2, caminho_3=caminho_3, caminho_4=caminho_4)

# Verificando se o DataFrame não está vazio antes de prosseguir
if df.empty:
    st.error("Não foi possível carregar os dados.")
else:
    st.write("Dados carregados com sucesso!")
