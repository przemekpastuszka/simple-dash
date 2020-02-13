from dash import Dash

from simpledash.inspector.accessors import NestedAccessor, PropertyAccessor
from simpledash.inspector.component import find_data_providers
from simpledash.inspector.layout import find_all_components


def setup_callbacks(app: Dash):
    for component in find_all_components(app.layout):
        for component_property, data_providers in find_data_providers(component).items():
            _replace_data_providers_with_nones(component, component_property, data_providers)
            _setup_callback(app, component, component_property, data_providers)


def _replace_data_providers_with_nones(component, component_property, data_providers):
    for data_provider in data_providers:
        accessor = NestedAccessor(PropertyAccessor(component_property), data_provider.accessor)
        accessor.set(component, None)


def _setup_callback(app, component, component_property, data_providers):
    inputs = set()
    for data_provider in data_providers:
        inputs |= data_provider.data_provider.depends_on()
    inputs = list(inputs)
