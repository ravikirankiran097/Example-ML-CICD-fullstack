# flake8: noqa
__doc__ = """
The resource module provides a function called create_analytics_resources which helps to construct a Resource Class
The resource class is built using resource types which is provided by this module.
The function serves as a glue to integrate between DataSource objects, Analytics objects and resource types to create
a Resource Class

Resource types provide the interface of an endpoint, that is what sort of parameters should an endpoint accept
and what the variables of the endpoints are.
Resource types can be extended to provide more types when new types of endpoints are required.
"""

from analytics_api.resource.create import create_analytics_resources
from analytics_api.resource.endpoints import (
    ByDateSingle, ByDateRange
)
