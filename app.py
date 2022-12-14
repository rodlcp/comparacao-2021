import pandas as pd
import streamlit as st
import plotly.express as px

data = {i: pd.read_parquet(f'data/{i}.parquet') for i in ['qx', 'ex', 'lx']}

def gen_plot_df(var, cob, sex, anos):
    df = data[var][[f"{i} - {cob}-{sex}" for i in anos]]
    return df.reset_index().melt(id_vars = 'Idade', value_name = deal_var(var))

st.set_page_config(layout="wide")

show_name = {
    'ex': 'Eₓ',
    'qx': 'qₓ',
    'lx': 'lₓ'
}

deal_var = lambda x: show_name[x]

sidebar = st.sidebar

cob = sidebar.selectbox('Cobertura', ['sb', 'mt'], format_func = lambda x: 'Morte' if x == 'mt' else 'Sobrevivência')
sex = sidebar.selectbox('Sexo', ['m', 'f'], format_func = lambda x: 'Masculino' if x == 'm' else 'Feminino')
anos = sidebar.multiselect('Ano', ['2021', '2015', '2010'])
var = sidebar.selectbox('Variável', ['qx', 'ex', 'lx'], format_func = deal_var)

c = px.line(
    gen_plot_df(var, cob, sex, anos), 
    x = "Idade", 
    y = deal_var(var),
    color = 'Versão'
)

if var == 'qx':
    c.update_yaxes(
        range=[-5, 0.3], 
        tickformat = '.1e',
        tickmode = 'linear',
        tick0 = -5,
        dtick = 1,
        type = 'log'
    )
elif var == 'ex':
    c.update_yaxes(
        range = [0, 100], 
        type = 'linear'
    )
elif var == 'lx':
    c.update_yaxes(
        range = [0, 1e+6], 
        type = 'linear'
    )

st.plotly_chart(c, use_container_width=True)
