from typing import Any

import pandas as pd

from analytics_api.sources.bigquery.connector import BQConnector


class DataSource:

    def __init__(self, client):
        self.client = client
        self.client_built = False

    def build(self):
        """Lazy building, only when query is required"""
        self.client.authenticate()
        self.client.build_client()
        self.client_built = True

    def execute(self, query: Any) -> pd.DataFrame:
        """
        Always returns a pandas DataFrame regardless of client used
        :param query: input arguments to call on client's execute method
        :return: pd.DataFrame
        """
        if not self.client_built:
            self.build()

        return self.client.execute(query)

    @classmethod
    def from_bigquery(cls, authentication,
                      location: str = None,
                      project_id: str = None,
                      use_legacy_sql: bool = False,
                      use_query_cache: bool = False
                      ):
        """
        :param authentication: Authentication object to pass to Google Client Credentials
            Can be a dict containing the Json Secrets service account or a path to the json secrets service account file
        :param location: Default location for jobs / datasets / tables
            Good to specify so that Analytics can be made agnostic
        :param project_id: A string, optional
            The project ID for for the project which the client acts on behalf of. If not passed, falls back to the
            default inferred from the environment
        :param use_legacy_sql: Whether to use the new Standard SQL or fall back to legacy
        :param use_query_cache: Whether to cache past queries to save speed and money

        :raises google.auth.exceptions.DefaultCredentialsError – Raised if ``credentials`` is not specified and the
        library fails to acquire default credentials.
        :return: DataSource
        """
        client = BQConnector(authentication,
                             location=location,
                             project_id=project_id,
                             use_legacy_sql=use_legacy_sql,
                             use_query_cache=use_query_cache
                             )
        return cls(client)

    @classmethod
    def from_redshift(cls, authentication):
        """ Future extension example"""
        raise NotImplementedError

    @classmethod
    def from_postgres(cls, authentication):
        """ Future extension example"""
        raise NotImplementedError
