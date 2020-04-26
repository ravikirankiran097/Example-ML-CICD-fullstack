import os

from flask_restful_swagger import swagger

from analytics_api.analytics.nyc_taxi import NycAverageSpeed24hours
from analytics_api.resource import create_analytics_resources, ByDateSingle
from analytics_api.sources import DataSource

averagespeed24 = create_analytics_resources(
    analytics={'get': NycAverageSpeed24hours},
    resource_type=ByDateSingle,
    data_source=DataSource.from_bigquery(
        authentication=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        use_legacy_sql=False,
        use_query_cache=True),
)
averagespeed24.__doc__ = """Average speed (trip_distance / (dropoff_datetime - pickup_datetime)) of trips
Trips that ended in the past 24 hours from the provided date."""

averagespeed24.get = swagger.operation(notes="Returns the average speed in the last 24 hours for a given date",
                                       parameters=[
                                           {
                                               "name": "date",
                                               "description": "Single date to get the average speed in last 24 hours",
                                               "required": True,
                                               "allowMultiple": False,
                                               "dataType": 'Date in ISO 8601 format',
                                               "paramType": "query"
                                           }
                                       ],
                                       nickname="Average speed",
                                       responseMessages=[
                                           {
                                               "code": 400,
                                               "message": "Invalid input"
                                           },
                                           {
                                               "code": 200,
                                               "message": "Success"
                                           },
                                           {
                                               "code": 404,
                                               "message": "Connection Error"
                                           }
                                       ]
                                       )(averagespeed24.get)

averagespeed24 = swagger.model(averagespeed24)
