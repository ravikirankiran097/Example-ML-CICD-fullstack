from abc import ABC, abstractmethod

import pytest
from flask import url_for

from analytics_api.resource import create
from tests.conftest import endpoints_types


@pytest.fixture()
def patch_endpoint_resource_to_return_inputs(monkeypatch):
    def patched_get(self):
        return {key: str(value) for key, value in dict(**self.parse_args()).items()}

    def patched_add_method(cls, func, name):
        def new_method(self, *args, **kwargs):
            return patched_get(*args, **kwargs)

        setattr(cls, name, new_method)

    monkeypatch.setattr(create, 'add_method', patched_add_method)


@pytest.mark.integrationtest
class ByDateTest(ABC):

    @property
    @abstractmethod
    def endpoint_type(self):
        return NotImplementedError

    @property
    def endpoints(self):
        return [endpoints for endpoints, endpoint_type in endpoints_types.items()
                if endpoint_type == self.endpoint_type]


class TestByDateSingle(ByDateTest):
    endpoint_type = 'ByDateSingle'

    @pytest.mark.parametrize('get_params', ('2019-04-23',
                                            '2019-4-25',
                                            '2019-04-02',
                                            '2019-04-2',
                                            '2019-11-2'
                                            ))
    def test_correct_parameters(self, patch_endpoint_resource_to_return_inputs, client, get_params):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string={'date': get_params})
            assert res.status_code == 200

    @pytest.mark.parametrize('get_params', ({'data': 123},  # Incorrect field
                                            {'date': 'test'},  # Incorrect data type
                                            {'date': 20190425},  # Incorrect data type
                                            {'start': '2019-04-23',
                                             'end': '2019-04-23'},  # Wrong parameters
                                            {'date': '2019-04-23',
                                             'end': '2019-04-25'}  # Contains unnecessary parameter, 'end'
                                            ))
    def test_incorrect_parameters_fail(self, patch_endpoint_resource_to_return_inputs, client, get_params):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string=get_params)
            assert res.status_code == 400

    @pytest.mark.freeze_time('2020-1-28')
    def test_incomplete_parameters(self, client, patch_endpoint_resource_to_return_inputs):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string=None)

            assert res.status_code == 200
            result = res.get_json()
            assert result == {"data": []}


class TestByDateRange(ByDateTest):
    endpoint_type = 'ByDateRange'

    @pytest.mark.parametrize('test_params', [test_param for test_params in ([{'start': '2019-04-23',
                                                                              'end': test_date},
                                                                             {'start': test_date,
                                                                              'end': '2019-04-23'}] for test_date in
                                                                            ['2019-04-23',
                                                                             '2019-4-25',
                                                                             '2019-04-02',
                                                                             '2019-04-2',
                                                                             '2019-11-2'
                                                                             ]) for test_param in test_params]

                             )
    def test_correct_parameters(self, patch_endpoint_resource_to_return_inputs, client, test_params):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string=test_params)
            assert res.status_code == 200

    @pytest.mark.parametrize('get_params', ({'start': 123, 'end': 123},  # Incorrect data type
                                            {'start': 123, 'end': '2019-04-23'},  # Incorrect 1 data type
                                            {'starto': '2019-04-23', 'end': '2019-04-23'},  # Incorrect data field
                                            {'start': '2019-04-23', 'endo': '2019-04-23'},  # Incorrect data field
                                            {'date': '2019-04-23'},  # Incorrect data field
                                            {'start': '2019-04-23', 'end': '2019-04-23',
                                             'date': '2019-04-03'},  # Unnecessary parameter

                                            ))
    def test_incorrect_parameters_fail(self, patch_endpoint_resource_to_return_inputs, client, get_params):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string=get_params)
            assert res.status_code == 400

    @pytest.mark.parametrize('test_incomplete_parameter, expectation', (
        (None, {"data": []}),
    ))
    @pytest.mark.freeze_time('2020-1-28')
    def test_incomplete_parameters(self, client, test_incomplete_parameter, expectation,
                                   patch_endpoint_resource_to_return_inputs):
        for endpoint in self.endpoints:
            url = url_for(endpoint.lower())
            res = client.get(url, query_string=test_incomplete_parameter)

            assert res.status_code == 200
            result = res.get_json()
            assert result == expectation
