"""
We will do exactly the same thing as previously, but this time with no syntax sugar -
uppercasing will be done by completely new data provider
"""

import dash

import dash_html_components as html
from dash.dependencies import Input

from examples.tutorial.t02_first_data_provider import input_a, input_b, input_chooser, output_value
from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


# you have two options
# you can either call the `output_value` function directly with all its arguments values
@data_provider(Input('data-input-a', 'value'), Input('data-input-b', 'value'), Input('input-chooser', 'value'))
def uppercase_output_value_1(input_a_value, input_b_value, input_chooser_value):
    v = output_value(input_a_value, input_b_value, input_chooser_value)
    return v.upper()


# or declare `output_value` as an input and get its value
@data_provider(output_value)
def uppercase_output_value_2(v):
    return v.upper()


app.layout = html.Div([
    html.Div(["A: ", input_a], className='row'),
    html.Div(["B: ", input_b], className='row'),
    html.Div(["Which one to show? ", input_chooser], className='row'),
    html.Br(),
    html.Div(["Here's the output: ", output_value], className='row', id='output'),
    html.Div(["Also in uppercase!: ", uppercase_output_value_1], className='row', id='output-upper-1'),
    html.Div(["Also in uppercase (2)!: ", uppercase_output_value_2], className='row', id='output-upper-2'),
])

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
