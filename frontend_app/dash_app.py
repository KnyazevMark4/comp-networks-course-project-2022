from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import requests

app = Dash(__name__)


def get_prediction_from_backend(text):
    response = requests.post(
        'http://localhost:9158/predict_sentiments',
        json={'text': text}
    )
    return response.json()

@app.callback(
    Output('output-state', 'children'),
    Output(component_id='score-graph', component_property='figure'),
    Input('submit-button-state', 'n_clicks'),
    State('input', 'value')
)
def update_sentiment(n_clicks, text):
    prediction = get_prediction_from_backend(text)
    sentiment = prediction['pred_label']
    score_dict = prediction['probabilities']
    fig = get_figure(score_dict)
    return f'Sentiment: {sentiment}', fig


def get_figure(score_dict):
    sentiments, scores = list(zip(*score_dict.items()))

    df = pd.DataFrame()
    df['sentiment'] = sentiments
    df['score'] = scores

    fig = px.bar(df, x="sentiment", y="score", range_y=(0, 1))
    return fig


example_text = 'Текст для классификации'

initial_fig = get_figure(get_prediction_from_backend(example_text)['probabilities'])

app.layout = html.Div(children=[
    html.H1(children='Sentiment Classification'),

    html.Div(children='''
        Classes: negative, neutral, positive.
    '''),

    html.Br(),
    html.Label('Text Input:'),
    html.Br(),
    dcc.Input(id='input', value=example_text, type='text'),
    html.Button(id='submit-button-state', children='Predict sentiment'),
    html.H2(id='output-state'),
    dcc.Graph(
        id='score-graph',
        figure=initial_fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True, port=9131)
