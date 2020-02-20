import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
from dash.dependencies import Input

from examples.utils import options_from, range_slider, shuffle
from simpledash.callbacks import setup_callbacks
from simpledash.data.data_providers import data_provider

dataset_chooser = dcc.Dropdown(id='dataset',
                               options=options_from(['seq', 'fib', 'sqr']),
                               value="seq")


@data_provider()
def all_datasets():
    return {
        'seq': pandas.Series(shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
        'fib': pandas.Series(shuffle([1, 2, 3, 5, 8, 13, 21, 34])),
        'sqr': pandas.Series(shuffle([1, 2, 4, 8, 16, 32, 64]))
    }


@data_provider(all_datasets, Input(dataset_chooser.id, 'value'))
def dataset(datasets, dataset_name):
    return datasets[dataset_name]


dataset_filter = range_slider(id='dataset-filter',
                              min_max_from=dataset)


@data_provider(dataset, Input(dataset_filter.id, 'value'))
def filtered_dataset(dataset_value, filter_value):
    return dataset_value[dataset_value.between(filter_value[0], filter_value[1])]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(["Dataset: ", dataset_chooser], className='row'),
    html.Div(["Filter by value: ", dataset_filter], className='row'),
    html.Div(["Original dataset size is: ", html.Strong(dataset.size, id='original size')], className='row'),
    html.Div(["Filtered dataset size is: ", html.Strong(filtered_dataset.size, id='filtered size')], className='row'),
    html.Div(["First value in dataset is: ", html.Strong(filtered_dataset.iloc[0], id='first item')], className='row'),
    html.Div(["Average value in dataset is: ", html.Strong(filtered_dataset.mean(), id='mean')], className='row'),
])

setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
