import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

dataset = pd.read_csv('projeto/datasets/Student_performance_data _.csv')

# Gráficos
gf_alunos = px.bar(y=dataset['GradeClass'].value_counts(), width=600, height=400, color=dataset['GradeClass'].value_counts())
gf_alunos.update_layout(
    title='Quantidade de alunos por classe em toda escola',
    font_family='DejaVu Sans',
    font_size=12,
    title_font_size=18,
    xaxis_title='Grade Class',
    yaxis_title='Quantidade',
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4],
        ticktext=['Menor que 2.0',  '2.5 a 2', '3 a 2.5', '3.5 a 3', 'Maior que 3.5']
    ),
    plot_bgcolor='white',
    title_font_color= 'black',
    font_color= 'black',
    showlegend=False,
    title_x=0.53,
    title_y=0.89,
)

gf_idade = px.pie(dataset, names='Age').update_layout(
    font_family='DejaVu Sans',
    title = 'Distribuição de alunos por iddade',
    title_font_size=18,
    font_size=14,
    title_x = 0.5,
    title_y=0.89,
    title_font_color= 'black',
    font_color= 'black',
    width = 400,
    height = 400,
)

# Variáveis dos dados
n_alunos = dataset['StudentID'].shape[0]
n_extra_alunos = dataset['Extracurricular'].value_counts()[0]
media_estudo_semanal_v = dataset['StudyTimeWeekly'].mean()
gpa = dataset['GPA'].mean()

# Elementos da página inicial

quantidade_alunos = f'{n_alunos}'
gpa = f'{gpa:.2f}'
tempo_estudo_semanal = f'{media_estudo_semanal_v:.2f} min' 
extracurricular = f'{n_extra_alunos}'


# Card
def card(titulo, elemento):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H6(titulo, className="card-title, text-center"),
                html.H3(
                    elemento,
                    className="card-text, text-center",
                ),
            ]
        ),
    style={"width": "12rem", "height": "1rem", 'padding': '0rem 0rem 6rem 0rem'},
    )
    return card

n_alunos_card = card('Alunos', quantidade_alunos)
card_gpa = card('Média de notas geral', gpa)
estudo_semanal = card('Média estudo semanal', tempo_estudo_semanal)
n_extracurricular = card('Extracurricular', extracurricular)

# Layout

layout =dbc.Container([
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                    html.H1('Relatório de alunos', className='text-center')
                                )
                        ],
                        align='center',
                        justify='center',
                        class_name='mt-1')
                ]
            ),
            html.Div(
                [
                    dbc.Row([
                        dbc.Col(n_alunos_card),
                        dbc.Col(card_gpa),
                        dbc.Col(estudo_semanal),
                        dbc.Col(n_extracurricular)
                    ], justify='center')
                ], style={'display': 'flex', 'justify-content': 'center'}
            ),

            html.Div(
                [
                    dbc.Row(
                        [   
                            html.Div([
                                dbc.Col(dcc.Graph(id='classes-gpa', figure = gf_alunos)),
                                dbc.Col(dcc.Graph(id='composicao-idade', figure = gf_idade))
                                ], style={'display': 'flex', 'justify-content': 'center'})
                        ]
                    )
                ]
            )
        ])