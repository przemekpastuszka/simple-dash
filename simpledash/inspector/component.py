from collections import defaultdict
from typing import Dict, List

from dash.dependencies import Input
from dash.development.base_component import Component

from simpledash.data.data_providers import DataProvider
from simpledash.inspector.accessors import Accessor, KeyAccessor, TupleAccessor, DummyAccessor, NestedAccessor


class DataProviderWithAccessor:
    def __init__(self, data_provider: DataProvider, accessor: Accessor):
        self.data_provider = data_provider
        self.accessor = accessor


def find_data_providers(component: Component) -> Dict[str, List[DataProviderWithAccessor]]:
    proxies = defaultdict(list)
    for attr, attr_value in component.__dict__.items():
        for proxy in _find_data_providers(attr_value):
            proxies[attr].append(proxy)
    return proxies


def _find_data_providers(obj, root_accessor: Accessor = None) -> List[DataProviderWithAccessor]:
    root_accessor = root_accessor or DummyAccessor()

    def data_providers_in(iterator, accessor_clazz):
        data = []
        for k, v in iterator:
            data += _find_data_providers(v, NestedAccessor(root_accessor, accessor_clazz(k)))
        return data

    if isinstance(obj, (DataProvider, Input)):
        return [DataProviderWithAccessor(DataProvider.to_provider(obj), root_accessor)]

    if isinstance(obj, dict):
        return data_providers_in(obj.items(), KeyAccessor)

    if isinstance(obj, list):
        return data_providers_in(enumerate(obj), KeyAccessor)

    if isinstance(obj, tuple):
        return data_providers_in(enumerate(obj), TupleAccessor)

    return []
