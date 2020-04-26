import pytest

from webservice import application

freeze_time = (2020, 1, 28)


@pytest.fixture
def app():
    application.debug = True
    return application


endpoints_types = {'totaltrips': 'ByDateRange',
                   'averagefareheatmap': 'ByDateSingle',
                   'averagespeed24': 'ByDateSingle'}

endpoints = [endpoint.lower() for endpoint in (endpoints_types.keys())]
