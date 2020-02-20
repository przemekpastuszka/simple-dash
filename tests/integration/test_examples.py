from examples.estate.estate import app as estate_app
from examples.tutorial.t01_using_input_in_the_layout import app as t01app
from examples.tutorial.t02_first_data_provider import app as t02app
from examples.tutorial.t03_nested_data_providers import app as t03app


def test_estate_application(dash_duo):
    dash_duo.start_server(estate_app)


def test_tutorial_01(dash_duo):
    dash_duo.start_server(t01app)


def test_tutorial_02(dash_duo):
    dash_duo.start_server(t02app)


def test_tutorial_03(dash_duo):
    dash_duo.start_server(t03app)
