import dash_core_components as dcc
from dash.dependencies import Input

from simpledash.inspector.accessors import NestedAccessor, Accessor
from simpledash.inspector.component import find_data_providers_used_in_component

input_a = Input("a", "x")
input_b = Input("b", "x")
input_c = Input("c", "x")

dummy_component = dcc.Graph(figure=dict(
    series=[{
        "x": input_a,
        "y": input_b,
        "marker": ("something", {
            "color": input_c
        })
    }]
))

def test_retrieves_data_providers_and_their_accessors():
    providers_with_accessors = find_data_providers_used_in_component(dummy_component)
    assert providers_with_accessors.keys() == {'figure'}

    providers_with_accessors


def _linearize_accessors(accessor: Accessor):
    if isinstance(accessor, NestedAccessor):
        return _linearize_accessors(accessor.a) + _linearize_accessors(accessor.b)
    return [accessor]
