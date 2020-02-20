from typing import List
from unittest.mock import Mock

import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from simpledash.callbacks import _replace_data_providers_with_nones, _setup_callback
from simpledash.data.data_providers import DataProvider, DashInput
from simpledash.inspector.accessors import NestedAccessor, Accessor, KeyAccessor
from simpledash.inspector.component import DataProviderWithAccessor

test_component = dcc.Graph(
    id='test',
    figure=dict(series=[{"x": Input("x", "z"), "y": Input("y", "z")}]),
    responsive=True
)


def test_replaces_data_providers_with_none():
    result = _replace_data_providers_with_nones(
        test_component, 'figure', [_x_provider(), _y_provider()])

    assert result.figure['series'][0]['x'] is None
    assert result.figure['series'][0]['y'] is None


def test_sets_up_callbacks_properly():
    app = Mock()

    _setup_callback(app, test_component, 'figure', [_x_provider(), _y_provider()])

    app.callback.assert_called_with(
        Output('test', 'figure'),
        [Input("x", "z"), Input("y", "z")],
        [State('test', 'figure')]
    )

    method = app.mock_calls[1][1][0]
    result = method("X", "Y", dict(series=[{"x": "x", "y": "y", "z": "z"}]))

    assert result == dict(series=[{"x": "X", "y": "Y", "z": "z"}])


def _x_provider():
    return _data_provider_with_accessor(
        [KeyAccessor('series'), KeyAccessor(0), KeyAccessor("x")],
        DashInput(Input("x", "z"), )
    )


def _y_provider():
    return _data_provider_with_accessor(
        [KeyAccessor('series'), KeyAccessor(0), KeyAccessor("y")],
        DashInput(Input("y", "z"))
    )


def _data_provider_with_accessor(accessors: List[Accessor], data_provider: DataProvider):
    return DataProviderWithAccessor(data_provider, NestedAccessor.from_list(accessors))
