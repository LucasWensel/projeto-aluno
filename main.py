from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app 
from pages import homepage, estatistica, formulario

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Análise de alunos", className="display-4 text-center"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Homepage", href="/", active="exact"),
                dbc.NavLink("Estatística por aluno", href="/estatisticas", active="exact"),
                dbc.NavLink("Previsão de notas", href="/formulario", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return homepage.layout
    elif pathname == "/estatisticas":
        return estatistica.layout
    elif pathname == "/formulario":
        return formulario.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


app.run_server(debug=True)