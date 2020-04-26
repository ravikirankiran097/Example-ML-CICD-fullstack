from copy import deepcopy
from typing import Type, Dict, AnyStr, Callable

from flask_restful import Resource

from analytics_api.analytics.api_base import Analytics
from analytics_api.sources import DataSource


def create_analytics_resources(analytics: Dict[AnyStr, Type[Analytics]],
                               resource_type: Type[Resource],
                               data_source: DataSource,
                               endpoint_name: AnyStr = None,
                               ) -> Type[Resource]:
    """
    Creates a Analytics Resource Class by piecing together from a DataSource object, analytics and a Resource.type
    Type, the class itself.

    Available endpoint methods:
        get
        delete
        put
        post

    :param analytics: dict
        of the form {str: Analytics}
        where str refers to the API method (get, post etc) which is implemented in resource_type
        and Analytics is an Analytics child class from the analytics module, which implements get_data and process_data
         To be used to receive parameters from resource and then get and process data from data source.
    :param resource_type: A class inheriting from AnalyticsResource
    :param data_source: DataSource object
    :param endpoint_name: str optional
        endpoint name (defaults to :`resource_type.__name__.lower`
            Can be used to reference this route from the webservice Api class.
    :return: A new class that inherits from Resource, all methods need to be fed by key word arguments
        Can be used to add a new resource into the webservice Api
    """

    name = endpoint_name if endpoint_name else analytics[list(analytics.keys())[0]].__name__.lower()

    class AugmentedResourceClass(resource_type):
        parser = deepcopy(resource_type.parser)

        def get(self):
            raise NotImplementedError

        def post(self):
            raise NotImplementedError

    AugmentedResourceClass.__name__ = name

    for rest_key, analytics in analytics.items():
        def rest_method(**kwargs):
            data = data_source.execute(analytics.get_data(**kwargs))
            return analytics.process_data(data)

        add_method(AugmentedResourceClass, rest_method, f"{rest_key}")

    return AugmentedResourceClass


def add_method(cls: Type, func: Callable, name: str):
    """
    Adds a method to a class inplace
    :param cls: Class
    :param func: Function to add as a method
    :param name: Name of new method for instance of class to call
    """

    def new_method(self, *args, **kwargs):
        return func(*args, **kwargs)

    setattr(cls, name, new_method)
