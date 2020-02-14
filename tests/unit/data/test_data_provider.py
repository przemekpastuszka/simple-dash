import pytest
from dash.dependencies import Input

from simpledash.data.data_provider import DataProvider, DataProviderOperationException, StaticValueProvider, \
    DashInput

dummy_data_provider = DataProvider()
input_a = Input('a', 'x')
input_b = Input('b', 'x')
input_c = Input('c', 'x')


def test_lists_dependencies():
    some_input = DashInput(input_c).x()

    provider = StaticValueProvider(1).add(input_a, some_input)[input_c].xyz
    assert provider.depends_on() == {input_a, input_c}


def test_evaluates_data_provider():
    provider = DashInput(input_a)[0][input_b].lower()

    assert provider.evaluate({input_a: [["AAA"]], input_b: 0}) == "aaa"


def test_raises_for_conditional_on_data_provider():
    with pytest.raises(DataProviderOperationException):
        if dummy_data_provider:
            pass


def test_raises_when_iterating_over_data_provider():
    with pytest.raises(DataProviderOperationException):
        [x for x in dummy_data_provider]


def test_raises_when_comparing_data_provider_to_anything_else():
    with pytest.raises(DataProviderOperationException):
        dummy_data_provider == 10


def test_raises_when_assigning_to_data_provider():
    with pytest.raises(DataProviderOperationException):
        dummy_data_provider[10] = "aa"
