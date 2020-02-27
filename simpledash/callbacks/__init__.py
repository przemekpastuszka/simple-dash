from typing import List

from dash import Dash
from dash.dependencies import Output, State, Input
from dash.development.base_component import Component

from simpledash.inspector.accessors import NestedAccessor, PropertyAccessor
from simpledash.inspector.component import find_data_providers, DataProviderWithAccessor
from simpledash.inspector.layout import find_all_components


def setup_callbacks(app: Dash, layout=None):
    """
    Scans the layout to find instances of data_provider and sets callbacks for them

    :param app: the app to use for callbacks
    :param layout: layout which will be scanned. If not given, app.layout is going to be used
    """
    layout = layout or app.layout
    for component in find_all_components(layout):
        for component_property, data_providers in find_data_providers(component).items():
            _replace_data_providers_with_nones(component, component_property, data_providers)
            _setup_callback(app, component, component_property, data_providers)


def _replace_data_providers_with_nones(component: Component, component_property: str,
                                       data_providers: List[DataProviderWithAccessor]):
    for data_provider in data_providers:
        accessor = NestedAccessor(PropertyAccessor(component_property), data_provider.accessor)
        accessor.set(component, None)
    return component


def _setup_callback(app: Dash,
                    component: Component,
                    component_property: str,
                    data_providers: List[DataProviderWithAccessor]):
    inputs = _get_all_inputs(data_providers)
    if not inputs:
        inputs = [Input(component.id, 'id')]

    @app.callback(
        Output(component.id, component_property),
        inputs,
        [State(component.id, component_property)]
    )
    def execute(*args):
        context = dict(zip(inputs, args[:-1]))
        current_value = args[-1]

        for data_provider in data_providers:
            new_value = data_provider.data_provider.evaluate(context)
            current_value = data_provider.accessor.set(current_value, new_value)
        return current_value


def _get_all_inputs(data_providers):
    inputs = set()
    for data_provider in data_providers:
        inputs |= data_provider.data_provider.depends_on()
    inputs = list(sorted(inputs, key=lambda inp: (inp.component_id, inp.component_property)))
    return inputs
