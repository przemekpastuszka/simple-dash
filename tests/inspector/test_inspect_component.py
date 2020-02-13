import dash_core_components as dcc
from dash.dependencies import Input

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

    providers_with_accessors = [(x.data_provider._dash_input, repr(x.accessor)) for x in providers_with_accessors['figure']]
    assert (input_a, "[series][0][x]") in providers_with_accessors
    assert (input_b, "[series][0][y]") in providers_with_accessors
    assert (input_c, "[series][0][marker](1)[color]") in providers_with_accessors
