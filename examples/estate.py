import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
from dash.dependencies import Input

from simpledash.callbacks import setup_callbacks
from simpledash.data.data_provider import data_provider

estates = pandas.DataFrame(columns=[
    'type', 'area', 'price', 'lat', 'lng', 'desc'], data=[
    ('flat', 20, 1600, 50.07, 20.03, 'Pretty little flat'),
    ('flat', 78, 3400, 50.08, 20.04, 'Biggest flat you can get'),
    ('flat', 25, 1700, 50.02, 19.99, 'Reasonable choice'),
    ('flat', 60, 2000, 50.05, 20.01, 'Big yet cheap'),
    ('house', 98, 5500, 50.04, 19.94, 'House near the river'),
    ('house', 90, 3500, 50.02, 19.97, 'Cozy house')
])


def options_from(series):
    return [dict(label=v, value=v) for v in series]


category_filter = dcc.Dropdown(id='type_filter', options=options_from(['flat', 'house']), value="flat")


@data_provider(Input(category_filter.id, 'value'))
def estates_by_type(estate_type):
    return estates[estates['type'] == estate_type]


area_filter = dcc.RangeSlider('areafilter',
                              min=estates_by_type['area'].min(),
                              max=estates_by_type['area'].max(),
                              value=(estates_by_type['area'].min(), estates_by_type['area'].max()))

price_filter = dcc.RangeSlider('pricefilter',
                               min=estates_by_type['price'].min(),
                               max=estates_by_type['price'].max(),
                               value=(estates_by_type['price'].min(), estates_by_type['price'].max()))


@data_provider(estates_by_type, Input(area_filter.id, 'value'), Input(price_filter.id, 'value'))
def estates_to_display(df, area_filter_value, price_filter_value):
    df = df[df['area'].between(area_filter_value[0], area_filter_value[1])]
    df = df[df['price'].between(price_filter_value[0], price_filter_value[1])]
    return df


color_chooser = dcc.Dropdown(id='color-chooser', options=options_from(['area', 'price']), value='area')

map_plot = dcc.Graph('map', figure={
    'data': [
        {
            'lat': estates_to_display['lat'],
            'lon': estates_to_display['lng'],
            'mode': 'markers',
            'type': 'scattermapbox',
            'marker': {
                'color': estates_to_display[Input(color_chooser.id, 'value')],
                'cmin': estates_to_display[Input(color_chooser.id, 'value')].min(),
                'cmax': estates_to_display[Input(color_chooser.id, 'value')].max(),
                'colorscale': 'Jet',
                'colorbar': dict(thickness=20, title=Input(color_chooser.id, 'value'))
            },
            'customdata': estates_to_display.index
        }
    ],
    'layout': {
        'mapbox': dict(
            style='stamen-toner',
            center=dict(
                lat=50.049683,
                lon=19.944544
            ),
            zoom=10
        )
    }
})


@data_provider(Input(map_plot.id, 'clickData'))
def selected_point(click_data):
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
    html.Div(["Colorize graph by: ", color_chooser], className='row'),
    map_plot,
    html.Div(["Area: ", html.Strong(selected_point['area'], id='area'), " m2"], className='row'),
    html.Div(["Price: ", html.Strong(selected_point['price'], id='price'), " zl"], className='row'),
    html.Div(html.Iframe([], srcDoc=selected_point['desc'], id='desc', className='nine columns'),
             className='row')
])

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False)
