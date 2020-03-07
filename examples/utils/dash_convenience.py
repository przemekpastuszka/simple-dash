import dash_core_components as dcc

from simpledash.data.data_providers import data_provider


def options_from(series):
    return [dict(label=v, value=v) for v in series]


def plain_scatter_plot(id, x, y, customdata):
    return dcc.Graph(id, figure=dict(
        data=[
            dict(x=x,
                 y=y,
                 customdata=customdata,
                 mode='markers')
        ]
    ))


def range_slider(id, min_max_from):
    return dcc.RangeSlider(
        id,
        min=min_max_from.min(),
        max=min_max_from.max(),
        value=(min_max_from.min(), min_max_from.max()),
        tooltip={'always_visible': True, 'placement': 'bottomRight'}
    )


def colorized_map_plot(id, lat, lng, colors,
                       customdata,
                       center,
                       zoom=10):
    return dcc.Graph(id, figure={
        'data': [
            {
                'lat': lat,
                'lon': lng,
                'mode': 'markers',
                'type': 'scattermapbox',
                'marker': {
                    'color': colors,
                    'cmin': colors.min(),
                    'cmax': colors.max(),
                    'colorscale': 'Jet',
                    'colorbar': dict(thickness=20)
                },
                'customdata': customdata
            }
        ],
        'layout': {
            'mapbox': dict(
                style='stamen-toner',
                center=center,
                zoom=zoom
            )
        }
    })
