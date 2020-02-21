"""
This time we will create slightly more complicated app.
We would like to have two input fields (named A and B) and let user decide which one is going to be used
for rendering the output value. This choice will be done via dropdown.
"""

import dash

import dash_core_components as dcc
from dash.dependencies import Input
import dash_html_components as html

from examples.utils.dash_convenience import options_from
from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

input_a = dcc.Input(id='data-input-a', value="")
input_b = dcc.Input(id='data-input-b', value="")
input_chooser = dcc.Dropdown(id='input-chooser', options=options_from(['A', 'B']))

# use a `data_provider` annotation to indicate, that the method provides data based on inputs
# inputs used by function are declared as arguments to the decorator
# and are later on passed to the function as arguments
@data_provider(Input('data-input-a', 'value'), Input('data-input-b', 'value'), Input('input-chooser', 'value'))
def output_value(input_a_value, input_b_value, input_chooser_value):
    if input_chooser_value == "A":
        return input_a_value
    if input_chooser_value == "B":
        return input_b_value
    return ""


app.layout = html.Div([
    html.Div(["A: ", input_a], className='row'),
    html.Div(["B: ", input_b], className='row'),
    html.Div(["Which one to show? ", input_chooser], className='row'),
    html.Br(),
    # you simply use `data_provider` instance in the layout (as in previous example)
    html.Div(["Here's the output: ", output_value], className='row', id='output'),
    # but you can also run some simple operations on `data_provider`, like `upper()`
    html.Div(["Also in uppercase!: ", output_value.upper()], className='row', id='output-upper'),
])

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
