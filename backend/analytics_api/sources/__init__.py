# flake8: noqa
__doc__ = """
The sources module provides a middleware to connect to different data sources.
The main API is the DataSource class which is a top-level import from sources.

DataSource has a few constructor methods that will help to create and adapt to supported data sources and to standardize
an API for analytics resource endpoints

For now only bigquery is implemented via the method DataSource.from_big_query
This can be extended in the future to include other data sources such as NoSQL or RedShift as they can be wrapped
within a common API.
"""

from analytics_api.sources.core import DataSource
