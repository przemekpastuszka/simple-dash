"""
Let's create a simplest possible app with single Input component, that renders back whatever the user has typed in.
"""

import dash
import dash_core_components
import dash_html_components as html
from simpledash.callbacks import setup_callbacks

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    dash_core_components.Input(id='data-input', className='row'),

    # with Simple Plotly Dash you can use a dash dependency object directly in the layout
    # it will be replaced by actual `input_box.value` and updated every time it changes
    html.Div(dash.dependencies.Input('data-input', 'value'), className='row', id='output-div')
])

setup_callbacks(app)  # this will scan the layout and create all necessary callback functions

if __name__ == '__main__':
    app.run_server(debug=True)
