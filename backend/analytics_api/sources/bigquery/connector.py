from typing import AnyStr, Any

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

from analytics_api.sources.connector_base import Connector, Authentication


class BQConnector(Connector):
    """ A Class used to represent connection with Biq Query DataBase """

    def __init__(self,
                 authentication: Any,
                 location: str = None,
                 project_id: str = None,
                 use_legacy_sql: bool = False,
                 use_query_cache: bool = False,
                 ):
        """
        Initializes a connection with big query database
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
        """

        self.authentication = BQAuthentication(authentication)
        self.use_legacy_sql = use_legacy_sql
        self.use_query_cache = use_query_cache
        self.location = location
        self.project_id = project_id

        self.client = None

    def authenticate(self):
        self.authentication.authenticate(self.project_id)

    def build_client(self):
        job_config = bigquery.QueryJobConfig(use_legacy_sql=self.use_legacy_sql,
                                             use_query_cache=self.use_query_cache)

        self.client = bigquery.Client(credentials=self.authentication.credentials,
                                      project=self.authentication.project_id,
                                      location=self.location,
                                      default_query_job_config=job_config)

    def execute(self, query: AnyStr) -> pd.DataFrame:
        """Queries the Big Query client using the given query, builds the client if is not built yet but does not
        authenticate

        :param query: A string, a query to run on bigquery
        :return dictionary
        """
        if self.client is None:
            self.build_client()
        if not len(query):
            return pd.DataFrame()

        result = self.client.query(query)
        return result.to_dataframe()


class BQAuthentication(Authentication):
    authentication_methods = {str: service_account.Credentials.from_service_account_file,
                              dict: service_account.Credentials.from_service_account_info,
                              type(None): lambda x: None}

    def __init__(self, authentication):
        self.authentication_method = self.authentication_methods[type(authentication)]
        self.authentication = authentication

        self.project_id = None
        self.credentials = None

    def authenticate(self, project_id=None):
        self.credentials = self.authentication_method(self.authentication)
        try:
            self.project_id = project_id if project_id else self.credentials.project_id
        except AttributeError:
            self.project_id = None  # No credentials has been set
