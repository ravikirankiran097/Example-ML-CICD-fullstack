import pytest

from analytics_api.sources.bigquery.connector import BQConnector
from analytics_api.sources.connector_base import Connector
from analytics_api.sources.core import DataSource


@pytest.fixture()
def bq_dummy(monkeypatch):
    def fake_execute(query):
        return "BigQuery"

    def dummy():
        return

    monkeypatch.setattr(BQConnector, 'execute', fake_execute)
    monkeypatch.setattr(BQConnector, 'build_client', dummy)
    monkeypatch.setattr(BQConnector, 'authenticate', dummy)


@pytest.fixture()
def connector_dummy():
    class TestConnector(Connector):

        def __init__(self):
            self.client_built = False
            self.authenticated = False

        def build_client(self, *args, **kwargs):
            self.client_built = True

        def authenticate(self, *args, **kwargs):
            self.authenticated = True

        def execute(self, query):
            return query

    return TestConnector


def test_datasource_bigquery_build():
    test_bigquery_source = DataSource.from_bigquery(None,
                                                    'test_location',
                                                    '123',
                                                    use_legacy_sql=False,
                                                    use_query_cache=True,
                                                    )
    assert isinstance(test_bigquery_source.client, BQConnector)
    assert test_bigquery_source.client.location == 'test_location'
    assert test_bigquery_source.client.project_id == '123'
    assert test_bigquery_source.client.use_legacy_sql is False
    assert test_bigquery_source.client.use_query_cache is True

    test_bigquery_source = DataSource.from_bigquery('test',
                                                    use_legacy_sql=True,
                                                    use_query_cache=True,
                                                    )
    assert test_bigquery_source.client.use_legacy_sql is True
    assert test_bigquery_source.client.use_query_cache is True

    test_bigquery_source = DataSource.from_bigquery('test',
                                                    use_legacy_sql=False,
                                                    use_query_cache=False,
                                                    )
    assert test_bigquery_source.client.use_legacy_sql is False
    assert test_bigquery_source.client.use_query_cache is False


def test_datasource_build(connector_dummy):
    test_datasource = DataSource(connector_dummy())

    assert test_datasource.client.client_built is False
    assert test_datasource.client.authenticated is False

    test_datasource.build()

    assert test_datasource.client.client_built is True
    assert test_datasource.client.authenticated is True


def test_datasource_build_lazy(connector_dummy):
    test_datasource = DataSource(connector_dummy())
    assert test_datasource.client.client_built is False
    test_datasource.execute(500)
    assert test_datasource.client_built is True


def test_datasource_execute_no_mutation(connector_dummy):
    test_datasource = DataSource(connector_dummy())
    assert test_datasource.execute(500) == 500
