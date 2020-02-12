import dash_html_components as html
import dash_core_components as dcc

from simpledash.inspector.layout import find_all_components

summary = html.Summary("Filters", id='filters')
category = dcc.Dropdown(id='category_chooser')
strong = html.Strong("Category: ", id='category_label')
category_div = html.Div([strong, category], id='category_div')
details = html.Details([summary, category_div], id='details')
layout = html.Div(children=[details], id='layout')


def test_find_all_components():
    all_components = {
        summary,
        category,
        category_div,
        details,
        strong,
        layout
    }
    assert _get_ids(find_all_components(layout)) == _get_ids(all_components)


def _get_ids(components):
    return set(c.id for c in components)
