import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('gun_pointed.csv')

colors = {
    'background': '#f9f9f9',
    'text': '#333',
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
            "Ten projekt ma na celu analizę danych związanych z przestępnościami w mieście Phoenix. Celem jest przewidzenie grupy na podstawie dostępnych cech numerycznych i kategorycznych.",
            style={'color': colors['text']}),

        html.H2("Heatmapa", style={'color': 'black', 'margin-top': '40px'}),
        html.Iframe(srcDoc=open('heatmap.html', 'r').read(), width='100%', height='500px'),

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
                value='PGP_COUNT',
                clearable=False,
                style={'width': '200px'}
            )
        ], style={'margin-bottom': '20px'}),

        html.Div([
            html.Label('Rodzaj wykresu:', style={'color': colors['text']}),
            dcc.RadioItems(
                id='chart-type-selector',
                options=[
                    {'label': 'Wykres punktowy', 'value': 'scatter'},
                    {'label': 'Wykres słupkowy', 'value': 'bar'},
                    {'label': 'Histogram', 'value': 'histogram'}
                ],
                value='scatter',
                labelStyle={'display': 'block'},
                style={'width': '200px'}
            )
        ], style={'margin-bottom': '40px'}),

        html.Div(id='chart-container'),

        html.H2("Podsumowanie danych", style={'color': colors['text'], 'margin-top': '40px'}),

        html.Div(id='data-summary')
    ]
)


@app.callback(
    Output('chart-container', 'children'),
    Input('x-axis-selector', 'value'),
    Input('y-axis-selector', 'value'),
    Input('chart-type-selector', 'value')
)
def update_chart(x_axis, y_axis, chart_type):
    if not x_axis or not y_axis:
        return html.Div()

    if chart_type == 'scatter':
        fig = px.scatter(df, x=x_axis, y=y_axis, color='SIMPLE_SUBJ_RE_GRP', title='Wykres punktowy')
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_axis, y=y_axis, color='SIMPLE_SUBJ_RE_GRP', title='Wykres słupkowy')
    else:
        fig = px.histogram(df, x=x_axis, y=y_axis, color='SIMPLE_SUBJ_RE_GRP', title='Histogram')

    chart = dcc.Graph(figure=fig)
    return chart


@app.callback(
    Output('data-summary', 'children'),
    Input('x-axis-selector', 'value'),
    Input('y-axis-selector', 'value')
)
def update_data_summary(x_axis, y_axis):
    if not x_axis or not y_axis:
        return html.Div()

    x_axis_description = {
        'INC_IR_NO': 'Numer zdarzenia',
        'INC_DATE': 'Data zdarzenia',
        'INC_YEAR': 'Rok zdarzenia',
        'INC_TIME': 'Godzina zdarzenia',
        'INC_DAY_WEEK': 'Dzień tygodnia',
        'INC_LOC_COUNTY': 'Sektor miasta',
        'HUNDRED_BLOCK': 'Adres zdarzenia',
        'INC_CITY': 'Nazwa miasta',
        'INC_STATE': 'Stan',
        'INC_ZIPCODE': 'Kod pocztowy',
        'INC_PRECINCT': 'Obszar zdarzenia',
        'CIT_NUMBER': 'ID osoby',
        'CIT_GENDER': 'Płeć osoby',
        'CIT_AGE': 'Wiek osoby',
        'SUBJ_AGE_GROUP': 'Przedział wiekowy',
        'CIT_RACE': 'Rasa',
        'CIT_ETHNICITY': 'Pochodzenie',
        'SIMPLE_SUBJ_RE_GRP': 'Rasa/Pochodzenie',
        'CITIZEN_CHARGE': 'Zarzut'
    }

    y_axis_description = {
        'INC_IR_NO': 'Numer zdarzenia',
        'INC_DATE': 'Data zdarzenia',
        'INC_YEAR': 'Rok zdarzenia',
        'INC_TIME': 'Godzina zdarzenia',
        'INC_DAY_WEEK': 'Dzień tygodnia',
        'INC_LOC_COUNTY': 'Sektor miasta',
        'HUNDRED_BLOCK': 'Adres zdarzenia',
        'INC_CITY': 'Nazwa miasta',
        'INC_STATE': 'Stan',
        'INC_ZIPCODE': 'Kod pocztowy',
        'INC_PRECINCT': 'Obszar zdarzenia',
        'CIT_NUMBER': 'ID osoby',
        'CIT_GENDER': 'Płeć osoby',
        'CIT_AGE': 'Wiek osoby',
        'SUBJ_AGE_GROUP': 'Przedział wiekowy',
        'CIT_RACE': 'Rasa',
        'CIT_ETHNICITY': 'Pochodzenie',
        'SIMPLE_SUBJ_RE_GRP': 'Rasa/Pochodzenie',
        'CITIZEN_CHARGE': 'Zarzut'
    }

    if x_axis in x_axis_description:
        x_axis_label = f"{x_axis} - {x_axis_description[x_axis]}"
    else:
        x_axis_label = x_axis

    if y_axis in y_axis_description:
        y_axis_label = f"{y_axis} - {y_axis_description[y_axis]}"
    else:
        y_axis_label = y_axis

    x_axis_summary = html.P(f"{x_axis_label}", style={'margin-bottom': '10px'})
    y_axis_summary = html.P(f"{y_axis_label}", style={'margin-bottom': '10px'})
    summary = html.Div([x_axis_summary, y_axis_summary])
    return summary


if __name__ == '__main__':
    app.run_server(debug=True)