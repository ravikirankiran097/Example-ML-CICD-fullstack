import pytest
from flask_restful import reqparse

from analytics_api.resource.create import add_method


@pytest.fixture
def dummy_resource():
    class DummyResource:
        parser = reqparse.RequestParser()
        parser.add_argument('test')

    return DummyResource


def test_add_method():
    class NoMethod:
        pass

    with pytest.raises(AttributeError):
        NoMethod().test()

    def new_method():
        return "something"

    add_method(NoMethod, new_method, 'added_method')
    assert NoMethod().added_method() == "something"
