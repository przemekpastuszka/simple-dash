from examples.estate import app


def test_estate_application(dash_duo):
    dash_duo.start_server(app)
