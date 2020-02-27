import logging

from examples.estate import app as estate_app
from examples.tutorial.t01_using_input_in_the_layout import app as t01app
from examples.tutorial.t02_first_data_provider import app as t02app
from examples.tutorial.t03_nested_data_providers import app as t03app
from examples.multipage import app as multipage_app


def test_estate_application(dash_duo):
    dash_duo.start_server(estate_app)


def test_multipage_application(dash_duo, caplog):
    caplog.set_level(logging.INFO)
    dash_duo.start_server(multipage_app)

    page_1_input = dash_duo.wait_for_element("#page-1-input")
    page_1_input.send_keys("abc")
    dash_duo.wait_for_text_to_equal("#page-1-output", "abc")
    assert "doing external call" not in [record.message for record in caplog.records]

    dash_duo.server_url = dash_duo.server_url + "/page-2"
    dash_duo.wait_for_text_to_equal("#expensive-data", "External api call")
    assert "doing external call" in [record.message for record in caplog.records]


def test_tutorial_01(dash_duo):
    dash_duo.start_server(t01app)


def test_tutorial_02(dash_duo):
    dash_duo.start_server(t02app)


def test_tutorial_03(dash_duo):
    dash_duo.start_server(t03app)
