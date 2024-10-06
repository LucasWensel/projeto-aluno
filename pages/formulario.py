from app import app
from dash import html

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

model_hgbc = pd.read_pickle('projeto/models/hgbc_model.pkl')
dataset = pd.read_csv('projeto/datasets/Student_performance_data _.csv')


layout = dbc.Container([
    html.H3('Formulário de previsão GPA', className='text-center'),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Idade'),
                dbc.Select(id='idade', options=[
                    {'label':'15', 'value': 15},
                    {'label':'16', 'value': 16},
                    {'label':'17', 'value': 17},
                    {'label':'18', 'value': 18},
                ])
            ]),
            dbc.CardGroup([
                dbc.Label('Sexo'),
                dbc.Select(id='sexo', options=[
                    {'label': 'Masculino', 'value': 0},
                    {'label': 'Feminino', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Etnia'),
                dbc.Select(id='etnia', options=[
                    {'label': 'Europeu', 'value': 0},
                    {'label': 'Afro Americano', 'value': 1},
                    {'label': 'Asiático', 'value': 2},
                    {'label': 'Outro', 'value': 3}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Educação dos pais'),
                dbc.Select(id='educacao-pais', options=[
                    { 'label': 'Nenhuma', 'value': 0},
                    { 'label': 'Ensino médio', 'value': 1},
                    { 'label': 'Faculdade', 'value': 2},
                    { 'label': 'Bacharel', 'value': 3},
                    { 'label': 'Maior', 'value': 4}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Tempo de estudo por semana'),
                dbc.Input(id='tempo-estudo', type='number', placeholder='Selecione a média do tempo em minutos por semana')
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Faltas'),
                dbc.Input(id='faltas', type='number')
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Resultado', style={'margin-left':'0.5rem'}),
                html.Div(id='gpa-previsao', style={'margin-top': '1.5rem'})
            ], style={'margin-top': '1rem', 'border':'1px solid lightgray', 'border-radius': '5px', 'height': '4rem'})
        ]),
        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Tutoria'),
                dbc.Select(id= 'tutoria', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ]),
            dbc.CardGroup([
                dbc.Label('Ajuda dos pais'),
                dbc.Select(id='ajuda-pais', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Atividade extracurricular'),
                dbc.Select(id='atividade-extracurricular', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Esporte'),
                dbc.Select(id='esporte', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Musica'),
                dbc.Select(id='musica', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Label('Voluntariado'),
                dbc.Select(id='voluntariado', options=[
                    {'label': 'Não', 'value': 0},
                    {'label': 'Sim', 'value': 1}
                ])
            ], style={'margin-top': '1rem'}),
            dbc.CardGroup([
                dbc.Button(id='submit-aluno', children='Pesquisar', n_clicks=0),
            ], class_name='mt-3')
        ])
    ])
])

@app.callback(
    Output('gpa-previsao', 'children'),
    Input('submit-aluno', 'n_clicks'),
    [
        State('idade', 'value'),
        State('sexo', 'value'),
        State('etnia', 'value'),
        State('educacao-pais', 'value'),
        State('tempo-estudo', 'value'),
        State('faltas', 'value'),
        State('tutoria', 'value'),
        State('ajuda-pais', 'value'),
        State('atividade-extracurricular', 'value'),
        State('esporte', 'value'),
        State('musica', 'value'),
        State('voluntariado', 'value')
    ],
    prevent_initial_call=True
)
def previsao(n_clicks, idade, sexo, etnia, educacao_pais, tempo_estudo, faltas, tutoria, ajuda_pais, atividade_extracurricular, esporte, musica, voluntariado):
    if n_clicks == 0:
        return ''


    df = dataset.drop(columns=['StudentID', 'GPA', 'GradeClass'])
    df_previsao = pd.DataFrame(columns=df.columns, data=[[idade, sexo, etnia, educacao_pais, tempo_estudo, faltas, tutoria, ajuda_pais, atividade_extracurricular, esporte, musica, voluntariado]])
    previsao = model_hgbc.predict(df_previsao)

    if previsao == 0:
        mensagem = 'Gpa maior que 3.5'
    elif previsao == 1:
        mensagem = 'Gpa entre 3 e 3.5'
    elif previsao == 2:
        mensagem = 'Gpa entre 2.5 e 3'
    elif previsao == 3:
        mensagem = 'Gpa entre 2 e 2.5'
    else:
        mensagem = 'Gpa menor que 2'

    
    return html.H5(f'{mensagem}')