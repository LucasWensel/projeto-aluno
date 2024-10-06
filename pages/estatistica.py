import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output, State

dataset = pd.read_csv('projeto/datasets/Student_performance_data _.csv')

# cards
def card(titulo, conteudo):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H6(titulo, className="card-title, text-center"),
                html.H3(
                    conteudo,
                    className="card-text, text-center",
                ),
            ]
        ),
    style={"width": "12rem", "height": "1rem", 'padding': '0rem 0rem 6rem 0rem'},
    )
    return card

layout = dbc.Container([
    html.Div([
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        html.H6('Índice Grade Class ', className='text-center'),
                        dcc.Dropdown(
                            options=[
                                {'label':'Maior que 3.5', 'value':0},
                                {'label':'3.5 a 3'  , 'value':1},
                                {'label':'3 a 2.5', 'value':2},
                                {'label':'2.5 a 2', 'value':3},
                                {'label':'Menor que 2', 'value':4}
                            ],
                            id='gpa-dropdown',
                            clearable=False,
                            value=0
                        )
                    ], style={'display': 'flex', 'flex-direction': 'column'})
                ], width=3),
                
                dbc.Col([
                    html.Div([
                        # card_estudo_semanal,
                    ], style={'display': 'flex', 'justify-content': 'center'}, id='estudo-semanal')
                ], width=3),

                dbc.Col([
                    html.Div([
                        # card_faltas,
                    ], style={'display': 'flex', 'justify-content': 'center'}, id='faltas-value')
                ], width=3),
                dbc.Col([
                    html.Div([
                        # card_gpa
                    ], style={'display': 'flex', 'justify-content': 'center'}, id='gpa-value')
                ], width=3)

            ], justify='center'
        )
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('Opções', style={'text-align': 'center'}),
                    dcc.Dropdown(options=[
                        {'label':'Gênero', 'value':'Gender'},
                        {'label':'Tutoria', 'value': 'Tutoring'},
                        {'label':'Extracurricular', 'value': 'Extracurricular'},
                        {'label':'Esporte', 'value': 'Sports'},
                        {'label':'Música', 'value': 'Music'},
                        {'label':'Voluntário', 'value': 'Volunteering'}
                    ], id='labels-dropdown', clearable=False, value='Gender'),
                ], style={'display': 'flex', 'flex-direction': 'column'}),
                dcc.Graph(id='labels-value')
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(
                        [
                            html.H6('Pesquisar Aluno', className="card-title, text-center"),
                            dbc.Input(id='aluno', placeholder='Digite o id do aluno', type='number'),
                            dbc.Button('Pesquisar', id='submit-aluno', style={'margin-top': '1rem'})
                        ], style={'display':'flex', 'flex-direction': 'column','align-items': 'center'}
                    ),
                ], style={'border-bottom':'none', 'margin-bottom':'0px', 'border-radius':'5px 5px 0px 0px'}),
                html.Div([
                    html.Div([
                        dbc.Col([
                            html.H6('Gpa:', style={'margin-left':'1rem'}),
                            html.H6('Estudo semanal:', style={'margin-left':'1rem'}),
                            html.H6('Faltas:', style={'margin-left':'1rem'}),
                            html.H6('Genêro:', style={'margin-left':'1rem'}),
                            html.H6('Tutoria:', style={'margin-left':'1rem'}),
                            html.H6('Esporte:', style={'margin-left':'1rem'}),
                            html.H6('Música:', style={'margin-left':'1rem'}),
                            html.H6('Vuluntariado:', style={'margin-left':'1rem'}),
                            html.H6('Etnia:', style={'margin-left':'1rem'}),
                            html.H6('Educação dos pais:', style={'margin-left':'1rem'}),
                        ]),
                        dbc.Col([
                            html.Div(id='gpa-aluno'), 
                            html.Div(id='estudo-semanal-aluno'),
                            html.Div(id='faltas-aluno'),
                            html.Div(id='genero-aluno'),
                            html.Div(id='tutoria-aluno'),
                            html.Div(id='esporte-aluno'),
                            html.Div(id='musica-aluno'),
                            html.Div(id='voluntario-aluno'),
                            html.Div(id='etnia-aluno'),
                            html.Div(id='educacao-pais-aluno'),
                        ])
                    ], style={'display':'flex', 'align-content':'space-between'})
                ], style={'border':'1px solid lightgray', 'width':'100%', 'border-radius': '0px 0px 5px 5px', 'border-top':'none'})  
            ])
        ])
    ], style={'margin-top': '2rem'}),
])

# Média GPA
@app.callback(
    Output('gpa-value', 'children'),
    Input('gpa-dropdown', 'value'),
)
def gradeclass(value):
    if value == None:
        valor=''

    valor = dataset.query(f'GradeClass == {value}')['GPA'].mean()
    return card(titulo='Média GPA', conteudo=f'{valor:.2f}')

# Média estudo semanal
@app.callback(
    Output('estudo-semanal', 'children'),
    Input('gpa-dropdown', 'value')
)
def tempo_estudo_semanal(value):
    valor = dataset.query(f'GradeClass == {value}')['StudyTimeWeekly'].mean()
    return card(titulo='Média estudo semanal', conteudo=f'{valor:.2f}')

# Contagem Faltas
@app.callback(
    Output('faltas-value', 'children'),
    Input('gpa-dropdown', 'value')
)
def faltas(value):
    valor = dataset.query(f'GradeClass == {value}')['Absences'].count()
    return card(titulo='Faltas', conteudo=f'{valor}')

# Gráfico
@app.callback(
    Output('labels-value', 'figure'),
    Input('gpa-dropdown', 'value'),
    Input('labels-dropdown', 'value')
)
def grafico(gpa, label):
    df = dataset.query(f'GradeClass == {gpa}')

    if label == 'Gender':
        fig = px.bar(x=df[label].unique(), y=df[label].value_counts(), color_discrete_sequence=px.colors.qualitative.G10).update_layout(
                width=530,
                height=400,
                xaxis_title=f'{label}',
                yaxis_title='Quantidade',
                title=f'{label}',
                title_x=0.5,
                title_y=0.9,
                plot_bgcolor = 'rgba(0, 0, 0, 0)',
                paper_bgcolor= 'rgba(0, 0, 0, 0)',
                xaxis=dict(
                        tickmode='array',
                        tickvals=[0, 1],
                        ticktext=['Masculino',  'Feminino']
                    ),
                title_font_color= 'black',
                font_family='DejaVu Sans',
                font_size=12,
                title_font_size=20,
                font_color= 'black'
                )
        return fig
    
    else:
        fig = px.bar(x=df[label].unique(), y=df[label].value_counts(), color_discrete_sequence=px.colors.qualitative.G10).update_layout(
            width=530,
            height=400,
            xaxis_title=f'{label}',
            yaxis_title='Quantidade',
            title=f'{label}',
            title_x=0.5,
            title_y=0.89,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            xaxis=dict(
                    tickmode='array',
                    tickvals=[0, 1],
                    ticktext=['Não',  'Sim']
                ),
            title_font_color= 'black',
            font_family='DejaVu Sans',
            font_size=12,
            title_font_size=20,
            font_color= 'black',
        )
        return fig
    
# Pesquisar aluno
@app.callback(
    [Output('gpa-aluno', 'children'),
    Output('estudo-semanal-aluno', 'children'),
    Output('faltas-aluno', 'children'),
    Output('genero-aluno', 'children'),
    Output('tutoria-aluno', 'children'),
    Output('esporte-aluno', 'children'),
    Output('musica-aluno', 'children'),
    Output('voluntario-aluno', 'children'),
    Output('etnia-aluno', 'children'),
    Output('educacao-pais-aluno', 'children')],
    Input('submit-aluno', 'n_clicks'),
    State('aluno', 'value')
)
def pesquisar_aluno(n_clicks, aluno):

    if n_clicks == 0:
        return ''

    df = dataset.query(f'StudentID == {aluno}')

    if df['Gender'].empty:
        faltas = '0'
    else:
        faltas = f'{df['Absences'].values[0]}'


    if df['Gender'].empty:
        genero = 'Masculino'
    else:
        genero = 'Feminino'

    if df['Tutoring'].empty:
        tutoring = 'Não'
    else:
        tutoring = 'Sim'
    
    if df['Sports'].empty:
        sports = 'Não'
    else:
        sports='Sim'

    if df['Music'].empty:
        music = 'Não'
    else:
        music = 'Sim'

    if df['Volunteering'].empty:
        volunteering = 'Não'
    else:
        volunteering = 'Sim'

    etnias = ['Afro Americano', 'Asiático', 'Outro']
    if df['Ethnicity'].empty:
        ethicity = 'Europeu'
    else:
        ethicity = etnias[df['Ethnicity'].values[0]]

    educacoes = ['Nenhuma', 'Ensino médio', 'Faculdade', 'Bacharel', 'Maior']
    if df['ParentalEducation'].empty:
        parental = 'Nenhuma'
    else:
        parental = educacoes[df['ParentalEducation'].values[0]]

    return html.H6(f'{round(df.GPA.values[0], 2)}'), html.H6(f'{round(df['StudyTimeWeekly'].values[0], 2)}'), html.H6(faltas), html.H6(genero), \
           html.H6(tutoring), html.H6(sports), html.H6(music), html.H6(volunteering), html.H6(ethicity), \
           html.H6(parental)
        