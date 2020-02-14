from typing import Generator

from dash.development.base_component import Component


def find_all_components(component: Component) -> Generator[Component]:
    children = getattr(component, 'children', [])
    children = children if isinstance(children, list) else [children]
    for child in children:
        if isinstance(child, Component):
            for descendant in find_all_components(child):
                yield descendant
    yield component
