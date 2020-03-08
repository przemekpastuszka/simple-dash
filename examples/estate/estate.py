"""
We would like to create a visualisation, which will help us analyse market of flats for rent in some city.
What we'd like to see:
- what is the relation between area and rent price?
- where is the rent price highest (i.e. what locations in a city are most expensive

We do have dataset with both historical and available offers - we'd like to be able to distinguish between them.
(it'd be also nice if we could filter the data by price and area beforehand)
"""
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas
from dash.dependencies import Input

from examples.utils.dash_convenience import options_from, plain_scatter_plot, colorized_map_plot, range_slider
from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

data_file_path = root_dir = Path(__file__).parent / "flats.csv"
flats = pandas.read_csv(data_file_path)

# let user decide whether they want to see all data or only data about (still) available flats
# or historical data (about flats that have already been rented)
availability_filter = dcc.Dropdown(id='type_filter',
                                   options=options_from(['All', 'Only available', 'Already rented']),
                                   value="All")


# this data provider uses the availability_filter to present right subset of data
@data_provider(Input(availability_filter.id, 'value'))
def flats_by_availability(required_availability):
    if required_availability == 'All':
        return flats
    if required_availability == 'Only available':
        return flats[flats['is_available'] == True]
    return flats[flats['is_available'] == False]


# here are the range sliders we'll use to filter on area and rent_price
# as you can see, min-max of the slider is dynamically driven by data subset
# e.g. if you've chosen 'Only available', then min and max of the price_filter will be set to min and max price
# of the available flat for rent in the city
area_filter = range_slider('areafilter', min_max_from=flats_by_availability['area'])
price_filter = range_slider('pricefilter', min_max_from=flats_by_availability['rent_price'])


# apply filtering by area and price
@data_provider(flats_by_availability, Input(area_filter.id, 'value'), Input(price_filter.id, 'value'))
def flats_to_display(df, area_filter_value, price_filter_value):
    df = df[df['area'].between(area_filter_value[0], area_filter_value[1])]
    df = df[df['rent_price'].between(price_filter_value[0], price_filter_value[1])]
    return df


# the task was to plot price against area, but we will actually give user a choice of both X and Y columns
x_column_chooser = dcc.Dropdown(id='x-column-chooser', options=options_from(['area', 'rent_price', 'floor']),
                                value='area')
y_column_chooser = dcc.Dropdown(id='y-column-chooser', options=options_from(['area', 'rent_price', 'floor']),
                                value='rent_price')
relation_plot = plain_scatter_plot(
    'relation-plot',
    x=flats_to_display[Input(x_column_chooser.id, 'value')],
    y=flats_to_display[Input(y_column_chooser.id, 'value')],
    customdata=flats_to_display.index  # we're going to use this, when someone clicks on a marker
)

# the task was to colorize the markers on the map by price, but we'll give user other options to choose from too
color_chooser = dcc.Dropdown(id='color-chooser', options=options_from(['area', 'rent_price', 'floor']),
                             value='rent_price')
map_plot = colorized_map_plot(
    'map',
    lat=flats_to_display['latitude'],
    lng=flats_to_display['longitude'],
    colors=flats_to_display[Input(color_chooser.id, 'value')],
    customdata=flats_to_display.index,
    center=dict(
        lat=50.049683,
        lon=19.944544
    )
)


# additionally, it'd be nice to give user ability to click the marker on the graph and show the details of the estate
# this function does exactly that, with some additional complexity, because we have two plots on separate tabs
@data_provider(Input('tabs', 'value'), Input(relation_plot.id, 'clickData'), Input(map_plot.id, 'clickData'))
def selected_point(tabs_value, relation_click_data, map_click_data):
    click_data = relation_click_data if tabs_value == "tab-1" else map_click_data
    if click_data:
        point_index = click_data['points'][0]['customdata']
        return flats.loc[point_index]
    return {col: None for col in flats.columns}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div([
        html.Details([
            html.Summary("Filters"),
            html.Div(["Category: ", availability_filter], className='row'),
            html.Div(["Filter by area: ", area_filter], className='row'),
            html.Div(["Filter by rent price: ", price_filter], className='row'),
        ], open=True, className='row'),
        html.Details([
            html.Summary("Selected point"),
            html.Div(["Area: ", html.Strong(selected_point['area'], id='area'), " m2"], className='row'),
            html.Div(["Rent price: ", html.Strong(selected_point['rent_price'], id='rent_price'), " zl"], className='row')
        ], open=True, className='row')
    ], className='three columns'),
    html.Div([
        dcc.Tabs([
            dcc.Tab([
                html.Div(["x: ", x_column_chooser], className='row'),
                html.Div(["y: ", y_column_chooser], className='row'),
                relation_plot
            ], label="Plot"),
            dcc.Tab([
                html.Div(["Colorize graph by: ", color_chooser], className='row'),
                map_plot,
            ], label="Map")
        ], id='tabs')
    ], className='nine columns')
], className='row')

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
