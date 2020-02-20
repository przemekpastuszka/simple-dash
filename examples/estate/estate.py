import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
from dash.dependencies import Input

from examples.utils import plain_scatter_plot, options_from, colorized_map_plot, range_slider
from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

estates = pandas.DataFrame(columns=[
    'type', 'area', 'price', 'lat', 'lng', 'floor', 'desc'], data=[
    ('flat', 20, 1600, 50.07, 20.03, 0, 'Pretty little flat'),
    ('flat', 78, 3400, 50.08, 20.04, 3, 'Biggest flat you can get'),
    ('flat', 25, 1700, 50.02, 19.99, 10, 'Reasonable choice'),
    ('flat', 60, 2000, 50.05, 20.01, 15, 'Big yet cheap'),
    ('house', 98, 5500, 50.04, 19.94, 0, 'House near the river'),
    ('house', 90, 3500, 50.02, 19.97, 0, 'Cozy house')
])

category_filter = dcc.Dropdown(id='type_filter', options=options_from(['flat', 'house']), value="flat")


@data_provider(Input(category_filter.id, 'value'))
def estates_by_type(estate_type):
    return estates[estates['type'] == estate_type]


area_filter = range_slider('areafilter', min_max_from=estates_by_type['area'])
price_filter = range_slider('pricefilter', min_max_from=estates_by_type['price'])


@data_provider(estates_by_type, Input(area_filter.id, 'value'), Input(price_filter.id, 'value'))
def estates_to_display(df, area_filter_value, price_filter_value):
    df = df[df['area'].between(area_filter_value[0], area_filter_value[1])]
    df = df[df['price'].between(price_filter_value[0], price_filter_value[1])]
    return df


color_chooser = dcc.Dropdown(id='color-chooser', options=options_from(['area', 'price', 'floor']), value='area')
x_column_chooser = dcc.Dropdown(id='x-column-chooser', options=options_from(['area', 'price', 'floor']), value='area')
y_column_chooser = dcc.Dropdown(id='y-column-chooser', options=options_from(['area', 'price', 'floor']), value='price')

relation_plot = plain_scatter_plot(
    'relation-plot',
    x=estates_to_display[Input(x_column_chooser.id, 'value')],
    y=estates_to_display[Input(y_column_chooser.id, 'value')],
    customdata=estates_to_display.index
)

map_plot = colorized_map_plot(
    'map',
    lat=estates_to_display['lat'],
    lng=estates_to_display['lng'],
    colors=estates_to_display[Input(color_chooser.id, 'value')],
    customdata=estates_to_display.index,
    center=dict(
        lat=50.049683,
        lon=19.944544
    )
)


@data_provider(Input('tabs', 'value'), Input(relation_plot.id, 'clickData'), Input(map_plot.id, 'clickData'))
def selected_point(tabs_value, relation_click_data, map_click_data):
    click_data = relation_click_data if tabs_value == "tab-1" else map_click_data
    if click_data:
        point_index = click_data['points'][0]['customdata']
        return estates.loc[point_index]
    return {col: None for col in estates.columns}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Details([
        html.Summary("Filters"),
        html.Div(["Category: ", category_filter], className='row'),
        html.Div(["Filter by area: ", area_filter], className='row'),
        html.Div(["Filter by price: ", price_filter], className='row'),
    ], open=True),
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
    ], id='tabs'),
    html.Div(["Area: ", html.Strong(selected_point['area'], id='area'), " m2"], className='row'),
    html.Div(["Price: ", html.Strong(selected_point['price'], id='price'), " zl"], className='row'),
    html.Div(html.Iframe([], srcDoc=selected_point['desc'], id='desc', className='nine columns'),
             className='row')
])

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False)
