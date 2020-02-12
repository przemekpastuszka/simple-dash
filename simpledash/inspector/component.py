from collections import defaultdict
from typing import List

from dash.dependencies import Input
from dash.development.base_component import Component

from simpledash.data.data_provider import DataProvider
from simpledash.inspector.accessors import Accessor, KeyAccessor, TupleAccessor


class ProxyAccessors:
    def __init__(self, proxy: DataProvider):
        self.proxy = proxy
        self.accessors = DummyAccessor()

    def prepend(self, accessor: Accessor) -> 'ProxyAccessors':
        self.accessors.prepend(accessor)
        return self

    def __repr__(self):
        return "{} = {}".format(self.accessors, self.proxy)

def find_proxies_used_in(obj) -> List[ProxyAccessors]:
    def proxies_in(iterator, accessor_clazz):
        data = []
        for k, v in iterator:
            data += [proxy.prepend(accessor_clazz(k)) for proxy in find_proxies_used_in(v)]
        return data

    if isinstance(obj, (DataProvider, Input)):
        return [ProxyAccessors(DataProvider.to_provider(obj))]

    if isinstance(obj, dict):
        return proxies_in(obj.items(), KeyAccessor)

    if isinstance(obj, list):
        return proxies_in(enumerate(obj), KeyAccessor)

    if isinstance(obj, tuple):
        return proxies_in(enumerate(obj), TupleAccessor)

    return []


def find_proxies_used_in_component(component: Component):
    proxies = defaultdict(list)
    for attr, attr_value in component.__dict__.items():
        for proxy in find_proxies_used_in(attr_value):
            proxies[attr].append(proxy)
    return proxies
