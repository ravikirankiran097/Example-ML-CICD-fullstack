import pytest
from flask_restful import reqparse

from analytics_api.resource.create import create_analytics_resources


@pytest.fixture
def dummy_resource():
    class DummyResource:
        parser = reqparse.RequestParser()
        parser.add_argument('test')

    return DummyResource


@pytest.fixture
def dummydatasource():
    class DummyDataSource:

        @classmethod
        def execute(cls, query):
            return {"data": query}

    return DummyDataSource


@pytest.fixture
def dummy_analytics():
    class Analytics:

        @classmethod
        def get_data(cls, test):
            test = {'query': 5}
            return test

        @classmethod
        def process_data(cls, data):
            data['data3'] = 7
            return data

    return Analytics


def test_create_analytics_resources_kwargs(dummy_resource, dummy_analytics, dummydatasource):
    new_analytics_resource = create_analytics_resources({"get": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        )
    # This specific output is required as it indicates the order of which the methods were called
    assert new_analytics_resource().get(test=6) == {'data': {'query': 5}, 'data3': 7}

    with pytest.raises(TypeError):
        # Position args should not work so that it becomes strict
        assert new_analytics_resource().get(6) == {'data': {'query': 5}, 'data3': 7}


def test_create_analytics_resources_endpoints_paths(dummy_resource, dummy_analytics, dummydatasource):
    new_analytics_resource = create_analytics_resources({"get": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        )
    assert new_analytics_resource().get(test=6) == {'data': {'query': 5}, 'data3': 7}

    new_analytics_resource = create_analytics_resources({"post": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        )
    with pytest.raises(TypeError):
        # get should not work anymore because there was no assignment
        assert new_analytics_resource().get(test=6) == {'data': {'query': 5}, 'data3': 7}
    # _post should work now
    assert new_analytics_resource().post(test=6) == {'data': {'query': 5}, 'data3': 7}


def test_create_analytics_resources_endpoint_name(dummy_resource, dummy_analytics, dummydatasource):
    new_analytics_resource = create_analytics_resources({"get": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        )
    # Tests the default name to be of the same name as dummy_analytics
    assert new_analytics_resource.__name__ == dummy_analytics.__name__.lower()

    new_analytics_resource = create_analytics_resources({"blablabla": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        )
    # Tests the default name to be of the same name as dummy_analytics, doesn't matter what key it was, can be anything
    assert new_analytics_resource.__name__ == dummy_analytics.__name__.lower()

    new_analytics_resource = create_analytics_resources({"get": dummy_analytics},
                                                        dummy_resource,
                                                        dummydatasource,
                                                        endpoint_name="helloworld"
                                                        )
    assert new_analytics_resource.__name__ == "helloworld"
