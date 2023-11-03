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

def style_metric_cards(
    background_color: str = "#AFA6A6",
    border_size_px: str = '#000000',
    border_color: str = "#CCC",
    border_radius_px: int = 10,
    border_left_color: str = "#227308",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title='Dash ESA 2023', 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

# Definindo a configuração local para o Brasil (pt_BR)
locale.setlocale(locale.LC_ALL, 'pt_BR')

# Definindo o ANO ATUAL para filtro
ano_atual = str(datetime.now().year)


# -----------------------
# TRATAMENTO DOS DADOS
# -----------------------

# Realizando a junção dos 3 arquivos .CSV num único DataFrame

# Caminhos para os arquivos .CSV
caminho_1 = r"C:\Users\User\OneDrive\Trabalho\ESA 2023\Dashboard_ESA\base_dados\Cel Manfrini.csv"

caminho_2 = r"C:\Users\User\OneDrive\Trabalho\ESA 2023\Dashboard_ESA\base_dados\Cel Manfrini(1).csv"

caminho_3 = r"C:\Users\User\OneDrive\Trabalho\ESA 2023\Dashboard_ESA\base_dados\Cel Manfrini(2).csv"

caminho_4 = r"C:\Users\User\OneDrive\Trabalho\ESA 2023\Dashboard_ESA\base_dados\Cel Manfrini(3).csv"

@st.cache_data
def load_data(caminho_1, caminho_2, caminho_3, caminho_4):
    # Leitura dos arquivos .CSV em DataFrames individuais
    df1 = pd.read_csv(caminho_1)
    df2 = pd.read_csv(caminho_2)
    df3 = pd.read_csv(caminho_3)
    df4 = pd.read_csv(caminho_4)

    # Concatenação dos DataFrames em um único DataFrame
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)

    # Excluindo linhas que contenham a string "Tela" em qualquer coluna
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Tela')).any(axis=1)]

    # Transformando o tipo de dado das colunas de valores monetários
    df['A_LIQUIDAR'] = df['A_LIQUIDAR'].apply(lambda x: float(x.replace('.', '').replace(',', '.')))
    df['LIQUIDADO_A_PAGAR'] = df['LIQUIDADO_A_PAGAR'].apply(lambda x: float(x.replace('.', '').replace(',', '.')))
    df['TOTAL_A_PAGAR'] = df['TOTAL_A_PAGAR'].apply(lambda x: float(x.replace('.', '').replace(',', '.')))
    df['PAGO'] = df['PAGO'].apply(lambda x: float(x.replace('.', '').replace(',', '.')))

    # Convertendo a coluna DATA para datetime
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%y')

    # Convertendo a coluna DIAS em número inteiro
    df['DIAS'] = df['DIAS'].astype(int)
    return df

df = load_data(caminho_1=caminho_1, caminho_2=caminho_2, caminho_3=caminho_3, caminho_4=caminho_4)

# ------------------------------------------
#       STREAMLIT
# ------------------------------------------

# Sidebar
with st.sidebar:
   import streamlit as st
   
   

# Função para a página Recursos Gerais
def pagina_geral():
    tab1, tab2, tab3 = st.tabs([ 'Recursos Empenhados', 'Recursos para Empenho', 'Empenhos atraso'])
    with tab1:
        st.markdown("# Recursos Gerais - ESA")
        st.markdown("### Essa página visa apresentar uma visão macro dos recursos da ESA!")

        # Saldos Totais
        st.markdown('# Dados Gerais')
        total_pago = df['PAGO'].sum().round(2)
        total_a_liquidar = df['A_LIQUIDAR'].sum().round(2)
        total_liquidado_a_pagar = df['LIQUIDADO_A_PAGAR'].sum().round(2)


        col1, col2, col3 = st.columns(3, gap='large')

        with col1:
            st.metric(label="Total Pago", value=locale.currency(total_pago, grouping=True))

        with col2:
            st.metric(label="Total a liquidar", value=locale.currency(total_a_liquidar, grouping=True))

        with col3:
            st.metric(label="Total Liquidado a Pagar", value=locale.currency(total_liquidado_a_pagar, grouping=True))
            style_metric_cards()

        # Saldos Exercícios Correntes
        st.markdown('# Dados Ano Corrente')
        df_corrente = df[df['ANO'] == ano_atual]

        total_pago = df_corrente['PAGO'].sum().round(2)
        total_a_liquidar = df_corrente['A_LIQUIDAR'].sum().round(2)
        total_liquidado_a_pagar = df_corrente['LIQUIDADO_A_PAGAR'].sum().round(2)

        col1, col2, col3 = st.columns(3, gap='large')

        with col1:
            st.metric(label="Total Pago", value=locale.currency(total_pago, grouping=True))

        with col2:
            st.metric(label="Total a liquidar", value=locale.currency(total_a_liquidar, grouping=True))

        with col3:
            st.metric(label="Total Liquidado a Pagar", value=locale.currency(total_liquidado_a_pagar, grouping=True))
            style_metric_cards()

        # Saldos Exercícios RPNP
        st.markdown('# Dados de Restos a Pagar')
        df_restos = df[df['ANO'] != ano_atual]

        total_pago = df_restos['PAGO'].sum().round(2)
        total_a_liquidar = df_restos['A_LIQUIDAR'].sum().round(2)
        total_liquidado_a_pagar = df_restos['LIQUIDADO_A_PAGAR'].sum().round(2)

        col1, col2, col3 = st.columns(3, gap='large')

        with col1:
            st.metric(label="Total Pago", value=locale.currency(total_pago, grouping=True))

        with col2:
            st.metric(label="Total a liquidar", value=locale.currency(total_a_liquidar, grouping=True))

        with col3:
            st.metric(label="Total Liquidado a Pagar", value=locale.currency(total_liquidado_a_pagar, grouping=True))
            style_metric_cards()

        st.markdown('## 10 Notas de Empenhos com mais tempo')

        col1, col2 = st.columns(2, gap='large')

        with col1:
            cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
            df_aux = df.loc[:, cols].sort_values(by='DIAS', ascending=False)
            df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
            fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), 
                        x='NE', 
                        y='A_LIQUIDAR',
                        labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                        text_auto= '.5s', # type: ignore
                        color='DIAS',
                        color_continuous_scale = 'reds',
                        log_y=True,
                        template='plotly_dark',
                        hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
            fig.update_traces(textposition = 'outside')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
            df_aux = df.loc[:, cols].sort_values(by='DIAS', ascending=False)
            df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
            st.dataframe(df_aux)

        st.markdown('## 10 Notas de Empenhos com maior valor A LIQUIDAR')

        col1, col2 = st.columns(2, gap='large')

        with col1:
            cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
            df_aux = df.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
            df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
            fig = px.bar(df_aux, 
                        x='NE', 
                        y='A_LIQUIDAR',
                        labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                        text_auto= '.5s',
                        color='A_LIQUIDAR',
                        color_continuous_scale = 'reds',
                        log_y=True,
                        template='plotly_dark',
                        hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
            fig.update_traces(textposition = 'outside')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
            df_aux = df.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
            df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
            st.dataframe(df_aux)
            
    with tab2:
        st.markdown("# Notas de Crédito - ESA")
        st.markdown("### Essa página visa apresentar os saldos disponíveis para a ESA")
        df_recursos = pd.read_excel(r'C:\Users\User\OneDrive\Trabalho\ESA 2023\Dashboard_ESA\base_dados\Recursos_Disponiveis.xlsx', sheet_name='Recursos_ESA')
        df_recursos = df_recursos[['ND', 'UG Emissora', 'PI', 'Descrição PI', 'Detalhe Descrição PI', 'Soma de Valor']]

        # Convertendo tipos de colunas
        df_recursos['ND'] =  df_recursos['ND'].astype(str)
        df_recursos['UG Emissora'] = df_recursos['UG Emissora'].astype(str)
        df_recursos['UG Emissora'] = df_recursos['UG Emissora'].apply(lambda x: x.replace('.0', ''))
        
        
        #Total de Recursos disponíveis
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            total_recurso = df_recursos['Soma de Valor'].sum()
            st.metric(label="Total de Recursos", value=locale.currency(total_recurso, grouping=True))
            style_metric_cards()
            
        st.divider()
        st.markdown('## Recursos por ND')
        # Recursos disponíveis por ND
        col1, col2 = st.columns(2, gap='large')

        with col1:
           
            # Recursos disponíveis por ND
            df_aux = df_recursos.loc[:,['ND', 'PI','Soma de Valor']].groupby(by= ['ND']).sum().sort_values(by='Soma de Valor', ascending=False).reset_index()

            fig = px.bar(df_aux,
                         x = 'ND',
                         y = 'Soma de Valor',
                         labels={'ND':'Natureza da Despesa', 'Soma de Valor':'Recurso para empenhar'},
                         text_auto='.3s',
                         height=500,
                         log_y=True,
                         color='Soma de Valor',
                         color_continuous_scale = 'reds',
                         template='plotly_dark')
            fig.update_traces(textposition = 'outside', cliponaxis = False, hovertemplate=None)
            fig.update_layout(hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Porcentagem de Recursos por ND
            df_aux = df_recursos.loc[:,['ND', 'PI','Soma de Valor']].groupby(by= ['ND']).sum().sort_values(by='Soma de Valor', ascending=False).reset_index()

            fig = px.pie(df_aux, values='Soma de Valor', 
                                 names='ND',
                                 color_discrete_sequence=px.colors.sequential.RdBu,
                                 template='plotly_dark')
            fig.update_traces(textposition='inside',
                              textinfo='percent+label',
                              marker=dict(line=dict(color='#000000', width=2)))
            fig.update(layout_showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
        st.divider()
        st.markdown('## Recurso por PI')
        # Recursos disponíveis por ND
        col1, col2 = st.columns(2, gap='large')

        with col1:
           
            # Recursos disponíveis por PI
            df_aux = df_recursos.loc[:,['PI','Soma de Valor']].groupby(by= ['PI']).sum().sort_values(by='Soma de Valor', ascending=False).reset_index()

            fig = px.bar(df_aux,
                         x = 'PI',
                         y = 'Soma de Valor',
                         labels={'PI':'Programa Interno', 'Soma de Valor':'Recurso para empenhar'},
                         text_auto='.3s',
                         height=500,
                         log_y=True,
                         color='Soma de Valor',
                         color_continuous_scale = 'reds',
                         template='plotly_dark')
            fig.update_traces(textposition = 'outside', cliponaxis = False, hovertemplate=None)
            fig.update_layout(hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Porcentagem de Recursos por ND
            df_aux = df_recursos.loc[:,['PI','Soma de Valor']].groupby(by= ['PI']).sum().sort_values(by='Soma de Valor', ascending=False).reset_index()

            fig = px.pie(df_aux, values='Soma de Valor', 
                                 names='PI',
                                 color_discrete_sequence=px.colors.sequential.RdBu,
                                 template='plotly_dark')
            fig.update_traces(textposition='inside',
                              textinfo='percent+label',
                              marker=dict(line=dict(color='#000000', width=2)))
            fig.update(layout_showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
        st.divider()
        df_consolidado = df_recursos.sort_values(by='Soma de Valor', ascending=False).reset_index(drop=True)
        st.markdown('### Planilha de Recursos Disponíveis')
        st.dataframe(df_consolidado, use_container_width=True)
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
                
        csv = convert_df(df_consolidado)
                
        st.download_button(
            label="Download Recursos Disponíveis",
            data=csv,
            file_name='Recursos_disponíveis.csv',
            mime='text/csv')
        
    with tab3:
        st.markdown("# Empenhos que devem ser cobrados pelo Almox - ESA")
        st.markdown("### Essa página visa filtrar os empenhos que devem ser cobrados quanto a entrega")
        st.divider()

        
        nd = ['449052', '339030' ]
        cols = ['UG', 'ANO', 'CREDOR', 'NOME_CREDOR',
                'DATA', 'DIAS', 'ND', 'NDSI', 'NOME_NDSI', 
                'NE', 'PI', 'NOME_PI', 'UGR', 'NOME_UGR', 
                'A_LIQUIDAR', 'LIQUIDADO_A_PAGAR','PAGO']
        df_foco = df.loc[df['ND'].isin(nd) & (df['DIAS'] > 60) & (df['A_LIQUIDAR'] != 0), cols].sort_values(by=['ND', 'DIAS'], ascending=False).reset_index(drop=True)
        df_foco.reset_index(drop=True)
        st.markdown('### Planilha de Empenhos Atrasados')
        st.dataframe(df_foco, use_container_width=True)
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
                
        csv = convert_df(df_foco)
                
        st.download_button(
            label="Download Empenhos em atraso",
            data=csv,
            file_name='Retorno_Empenhos_Atraso.csv',
            mime='text/csv')
        

# Função para a página sobre UG 160
def pagina_160():
    st.markdown("# Recursos UG 160")
    st.markdown("## Aqui você encontra informações sobre os recursos da UG 160")
    df_160 = df[df['UG'] == '160129']

    # Saldos Totais
    total_pago = df_160['PAGO'].sum().round(2)
    total_a_liquidar = df_160['A_LIQUIDAR'].sum().round(2)
    total_liquidado_a_pagar = df_160['LIQUIDADO_A_PAGAR'].sum().round(2)

    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.metric(label="Total Pago", value=locale.currency(total_pago, grouping=True))
        
    with col2:
        st.metric(label="Total a liquidar", value=locale.currency(total_a_liquidar, grouping=True))

    with col3:
        st.metric(label="Total Liquidado a Pagar", value=locale.currency(total_liquidado_a_pagar, grouping=True))
        style_metric_cards()
        
    st.markdown('## 10 Notas de Empenhos com mais tempo')
        
    col1, col2 = st.columns(2, gap='large')

    with col1:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_160.loc[:, cols].sort_values(by='DIAS', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
        fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False),
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.3s',
                    color='DIAS',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_160.loc[:, cols].sort_values(by='DIAS', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
        st.dataframe(df_aux.sort_values(by='A_LIQUIDAR', ascending=False))

    st.markdown('## 10 Notas de Empenhos com maior valor A LIQUIDAR')
        
    col1, col2 = st.columns(2, gap='large')

    with col1:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_160.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
        fig = px.bar(df_aux, 
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.3s',
                    color='A_LIQUIDAR',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_160.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
        st.dataframe(df_aux)
        
    

# Função para a página UG 167
def pagina_167():
    st.markdown("# Recursos UG 167")
    st.markdown("## Aqui você encontra informações sobre os recursos da UG 167")
    df_167 = df[df['UG'] == '167129']
    
    # Saldos Totais
    total_pago = df_167['PAGO'].sum().round(2)
    total_a_liquidar = df_167['A_LIQUIDAR'].sum().round(2)
    total_liquidado_a_pagar = df_167['LIQUIDADO_A_PAGAR'].sum().round(2)

    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        st.metric(label="Total Pago", value=locale.currency(total_pago, grouping=True))
        
    with col2:
        st.metric(label="Total a liquidar", value=locale.currency(total_a_liquidar, grouping=True))

    with col3:
        st.metric(label="Total Liquidado a Pagar", value=locale.currency(total_liquidado_a_pagar, grouping=True))
        style_metric_cards()
        
    st.markdown('## 10 Notas de Empenhos com mais tempo')
        
    col1, col2 = st.columns(2, gap='large')

    with col1:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_167.loc[:, cols].sort_values(by='DIAS', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
        fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), 
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.3s',
                    color='DIAS',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_167.loc[:, cols].sort_values(by='DIAS', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
        st.dataframe(df_aux)

    st.markdown('# 10 Notas de Empenhos com maior valor A LIQUIDAR')
        
    col1, col2 = st.columns(2, gap='large')

    with col1:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_167.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10)
        fig = px.bar(df_aux, 
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.3s',
                    color='A_LIQUIDAR',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        cols = ['NE', 'A_LIQUIDAR', 'DIAS', 'NOME_NDSI', 'NDSI']
        df_aux = df_167.loc[:, cols].sort_values(by='A_LIQUIDAR', ascending=False)
        df_aux = df_aux[df_aux['A_LIQUIDAR'] != 0].head(10).reset_index(drop=True)
        st.dataframe(df_aux, use_container_width=True)
    
# Função para a página por ND
def pagina_ND():
    st.markdown('# Página por Natureza da Despesa')
    st.markdown("## Aqui você terá a capacidade de filtrar os recursos por ND ou UG")
    
    
    lista_nd = list(df['ND'].unique())
        
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        opcao_nd = st.selectbox(
        'Selecione a ND',
        lista_nd)
    
    with col2:     
        nr_ne = st.slider('Escolha a Quantidade de NE que serão visualizadas.', 0, 20, 10)
    # Dados Gerais por ND
    st.markdown('# Notas de Empenho com maior número de dias')
    # Inserindo colunas 
    col1, col2 = st.columns(2, gap='large')
    
    cols = ['UG', 'NE', 'DIAS', 'NOME_UGR' ,'NOME_NDSI', 'NDSI', 'A_LIQUIDAR', 'LIQUIDADO_A_PAGAR', 'PAGO']

    df_aux = df.loc[(df['ND'] == opcao_nd) & (df['A_LIQUIDAR'] != 0) , cols].sort_values(by='DIAS', ascending=False).reset_index(drop=True).head(nr_ne)
    
    with col1:
        fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), 
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.5s',
                    color='DIAS',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.dataframe(df_aux.sort_values(by='DIAS', ascending=False), use_container_width=True)
        
    # Dados Gerais por ND
    st.markdown('# Notas de Empenho com maior valor')
    # Inserindo colunas 
    col1, col2 = st.columns(2, gap='large')
    cols = ['UG', 'NE', 'DIAS', 'NOME_UGR' ,'NOME_NDSI', 'NDSI', 'A_LIQUIDAR', 'LIQUIDADO_A_PAGAR', 'PAGO']

    df_aux = df.loc[(df['ND'] == opcao_nd) & (df['A_LIQUIDAR'] != 0) , cols].sort_values(by='A_LIQUIDAR', ascending=False).reset_index(drop=True).head(nr_ne)
    
    with col1:
        fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), 
                    x='NE', 
                    y='A_LIQUIDAR',
                    labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                    text_auto='.5s',
                    color='DIAS',
                    color_continuous_scale = 'reds',
                    log_y=True,
                    template='plotly_dark',
                    hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
        fig.update_traces(textposition = 'outside')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.dataframe(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), use_container_width=True)
    
# Função para a página por ACAO
def pagina_acao():
    st.markdown('# Página por Ação Orçamentária ')
    st.markdown("## Aqui você terá a capacidade de filtrar os recursos por Ação Orçamentária")
    
    
    lista_acao = list(df['ACAO'].unique())
   
    opcao_acao = st.selectbox(
    'Selecione a Ação',
    lista_acao,
    index=None,
    placeholder="Selecione a Ação")
    
    # Dados Gerais por Ação Orçamentária

    
    cols = ['UG', 'NE', 'DIAS', 'NOME_UGR' ,'NOME_NDSI', 'NDSI', 'A_LIQUIDAR', 'LIQUIDADO_A_PAGAR', 'PAGO']

    df_aux = df.loc[(df['ACAO'] == opcao_acao) & (df['A_LIQUIDAR'] != 0), cols].sort_values(by='A_LIQUIDAR', ascending=False).reset_index(drop=True).head(10)
    
    
    fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False), 
                x='NE', 
                y='A_LIQUIDAR',
                labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                text_auto='.3s',
                color='DIAS',
                color_continuous_scale = 'reds',
                log_y=True,
                template='plotly_dark',
                hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
    fig.update_traces(textposition = 'outside')
    st.plotly_chart(fig, use_container_width=True)
        
 
    st.dataframe(df_aux, use_container_width=True)
    
# Função para a página por UGR
def pagina_ugr():
    st.markdown('# Página por UGR de origem do Recurso ')
    st.markdown("## Aqui você terá a capacidade de filtrar os recursos por UGR")
    
    
    lista_acao = list(df['NOME_UGR'].unique())
   
    opcao_acao = st.selectbox(
    'Selecione a UGR',
    lista_acao)
    
    # Dados Gerais por Ação Orçamentária

    
    cols = ['UG', 'NE', 'DIAS', 'NOME_UGR' ,'NOME_NDSI', 'NDSI', 'A_LIQUIDAR', 'LIQUIDADO_A_PAGAR', 'PAGO']

    df_aux = df.loc[(df['NOME_UGR'] == opcao_acao) & (df['A_LIQUIDAR'] != 0), cols].sort_values(by='A_LIQUIDAR', ascending=False).reset_index(drop=True)
    
    
    fig = px.bar(df_aux.sort_values(by='A_LIQUIDAR', ascending=False).head(10), 
                x='NE', 
                y='A_LIQUIDAR',
                labels={'NE':'Nota de Empenho', 'A_LIQUIDAR':'Saldo a liquidar'},
                text_auto='.3s',
                color='DIAS',
                color_continuous_scale = 'reds',
                log_y=True,
                template='plotly_dark',
                hover_name="NE", hover_data={'DIAS': True, 'A_LIQUIDAR': True, 'NOME_NDSI': True, 'NDSI': True})
    fig.update_traces(textposition = 'outside')
    st.plotly_chart(fig, use_container_width=True)
        
 
    st.dataframe(df_aux, use_container_width=True)
    
# Função para a página de Consutla ao CNPJ da Empresa
def pagina_cnpj():
    st.markdown('# Consulta CNPJ ')
    st.markdown("## Aqui você terá a acesso aos principais dados do Fornecedor")
    
    def consulta_cnpj(numero_cnpj):
        url = f"https://receitaws.com.br/v1/cnpj/{numero_cnpj}"

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)

        dic_fornecedor = response.json()

        return dic_fornecedor

    # Criando uma lista de CNPJ válidas para pesquisas
    # filtrando dos dados da coluna FAV
    df_cnpj = df[df['NOME_PI'] != 'PROFISSIONAL DE SAUDE AUTONOMO']
    df_cnpj = df[df['NOME_PI'] != 'ATENDIMENTO MEDICO-HOPITALR/FC']
    df_cnpj = df[df['NOME_PI'] != 'IND-INDENIZACOES']
    df_cnpj = df[df['NOME_PI'] != 'IND - INDENIZACOES']
    df_cnpj = df[df['NOME_PI'] != 'INDENIZACAO DESPESAS.']
    df_cnpj = df[df['NOME_PI'] != 'AUXILIO FINANCEIRO NÃO INDENIZÁVEL']
    df_cnpj = df[df['NOME_PI'] != 'INRE - RESTITUICAO E RESSARCIMENTO']
    df_cnpj = df[df['NOME_NDSI'] != 'OUTROS SERV.DE TERCEIROS PJ- PAGTO ANTECIPADO']
    df_cnpj = df[df['CREDOR'] != '160129']
    df_cnpj['CREDOR'].unique()
    
    option = st.selectbox(
    'Qual CNPJ deseja realizar consulta?',
    df_cnpj['CREDOR'].unique())
    
    
    # Chamar a função e atribuir o resultado ao dicionário
    dicionario = consulta_cnpj(option)
    
    st.header( dicionario['nome'])
    
    logradouro = dicionario['logradouro']
    numero = dicionario['numero']
    bairro = dicionario['bairro']
    cidade = dicionario['municipio']
    estado = dicionario['uf']
    telefone = dicionario['telefone']
    email = dicionario['email']
    
    # Dados da Empresa filtrada
   
    st.text(f'Logradouro: {logradouro}')
    st.text(f'Número: {numero}')
    st.text(f'Bairro: {bairro}')
    st.text(f'Cidade: {cidade}')
    st.text(f'Estado: {estado}')
    st.text(f'Telefone: {telefone}')
    st.text(f'E-mail: {email}')

#--------------------------------------------
# Criando um menu de seleção na barra lateral
#--------------------------------------------


st.sidebar.markdown('## Análise dos Recursos da ESA')

st.sidebar.metric(label="Empenhos Realizados até o momento", value=df.shape[0])

pagina_selecionada = st.sidebar.selectbox(
    "Escolha uma página",
    ("Recursos Gerais", "Recursos 160", "Recursos 167", "Recursos por ND", "Recursos por Ação", "Recursos por UGR", "Consulta CNPJ")
)

# Mostrando a página selecionada
if pagina_selecionada == "Recursos Gerais":
    pagina_geral()
elif pagina_selecionada == "Recursos 160":
    pagina_160()
elif pagina_selecionada == "Recursos 167":
    pagina_167()
elif pagina_selecionada == "Recursos por ND":
    pagina_ND()
elif pagina_selecionada == "Recursos por Ação":
    pagina_acao()
elif pagina_selecionada == "Recursos por UGR":
    pagina_ugr()
elif pagina_selecionada == "Consulta CNPJ":
    pagina_cnpj()