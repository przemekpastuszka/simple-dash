"""
We would like to create multi-page app with some simple content
The clue of this example is to show how to dynamically load components and data based
on the page currently being displayed.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input

from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# here's a simple page, that renders back whatever user has typed in
# as you can see, we are also setting up callbacks for this particular page right away
page_1_layout = html.Div([
    dcc.Input(id='page-1-input'),
    html.Div(Input('page-1-input', 'value'), id='page-1-output')
])
setup_callbacks(app, page_1_layout)


# We will now create a second page, which is supposed to display piece of data
# that is expensive to obtain (i.e. it takes a long time to get).
# The most important thing is to make sure that expensive_data is only
# calculated when the second page is being shown to the user.
# We can assure this by wrapping the expensive data calculation into data_provider
# so it's only called when the component is visible to the user
@data_provider()
def expensive_data():
    app.logger.info("doing external call")
    return "External api call"


page_2_layout = html.Div([
    html.Strong(expensive_data, id='expensive-data')
])
setup_callbacks(app, page_2_layout)


@data_provider(Input('url', 'pathname'))
def current_page_layout(pathname):
    if pathname == '/page-2':
        return page_2_layout
    return page_1_layout


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=current_page_layout, id='page-content')
])
setup_callbacks(app, app.layout)

if __name__ == '__main__':
    app.run_server(debug=False)
