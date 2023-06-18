import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('pgp_pointed-gun-at-person-details_pgpdetail.csv')

plotly_style = {
    'height': 400,
    'margin': {'autoexpand': True, 'b': 10, 'l': 10, 'r': 10, 't': 10}
}

colors = {
    'background': '#f9f9f9',
    'text': '#333',
    'plot_bgcolor': '#fff',
    'paper_bgcolor': '#f8f9fa',
    'font_color': '#333',
    'table_header_bg': '#f2f2f2',
    'table_header_font_color': '#333',
}

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css',
    'https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i',
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css',
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/1ebd237b/dash-uber-ride-demo.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={
        'font-family': 'Arial, sans-serif',
        'max-width': '800px',
        'margin': 'auto',
        'padding': '20px',
        'background-color': colors['background']
    },
    children=[
        html.H1("Dashboard Projektu", style={'text-align': 'center', 'color': colors['text']}),

        html.H2("Opis projektu", style={'color': colors['text'], 'margin-top': '40px'}),
        html.P(
            "Ten projekt ma na celu analizę danych związanych z przestępnościami w określonym regionie. Celem jest przewidzenie grupy przestępstw na podstawie dostępnych cech numerycznych i kategorycznych.",
            style={'color': colors['text']}),

        html.H2("Wizualizacja danych", style={'color': colors['text'], 'margin-top': '40px'}),

        html.Div([
            html.Label('Oś X:', style={'color': colors['text']}),
            dcc.Dropdown(
                id='x-axis-selector',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='CIT_AGE',
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'margin-bottom': '20px'}),

        html.Div([
            html.Label('Oś Y:', style={'color': colors['text']}),
            dcc.Dropdown(
                id='y-axis-selector',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='INC_YEAR',
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'margin-bottom': '20px'}),

        html.Div([
            html.Label('Typ wykresu:', style={'color': colors['text']}),
            dcc.Dropdown(
                id='chart-type-selector',
                options=[
                    {'label': 'Scatter', 'value': 'scatter'},
                    {'label': 'Bar', 'value': 'bar'},
                    {'label': 'Line', 'value': 'line'}
                ],
                value='scatter',
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'margin-bottom': '20px'}),

        dcc.Graph(id='chart-container', style=plotly_style),

        html.H2("Podsumowanie dla osi Y", style={'color': colors['text'], 'margin-top': '40px'}),
        html.P(f"Podsumowanie dla osi Y: ", id='y-axis-summary', style={'color': colors['text'], 'margin-bottom': '10px'}),
    ]
)


@app.callback(
    [Output('chart-container', 'figure'),
     Output('y-axis-summary', 'children')],
    [Input('x-axis-selector', 'value'),
     Input('y-axis-selector', 'value'),
     Input('chart-type-selector', 'value')]
)
def update_chart(x_axis, y_axis, chart_type):
    if not x_axis or not y_axis:
        return px.scatter(), ""

    if chart_type == 'scatter':
        chart_func = px.scatter
    elif chart_type == 'bar':
        chart_func = px.bar
    elif chart_type == 'line':
        chart_func = px.line
    else:
        chart_func = px.scatter

    fig = chart_func(df, x=x_axis, y=y_axis, color='SIMPLE_SUBJ_RE_GRP', title='Wykres punktowy')
    fig.update_layout(
        plot_bgcolor=colors['plot_bgcolor'],
        paper_bgcolor=colors['paper_bgcolor'],
        font=dict(color=colors['font_color'])
    )

    y_summary = df.groupby(y_axis).size().reset_index(name='Count')

    return fig, generate_summary_table(y_summary)


def generate_summary_table(data_frame):
    table_header = [
        html.Th(col, style={'background-color': colors['table_header_bg'], 'color': colors['table_header_font_color']}) for col in data_frame.columns
    ]

    table_body = [
        html.Tr([
            html.Td(data_frame.iloc[row_index][col_index]) for col_index in range(len(data_frame.columns))
        ]) for row_index in range(len(data_frame))
    ]

    return html.Table([
        html.Thead(table_header),
        html.Tbody(table_body)
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
