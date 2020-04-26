import os

from flask_restful_swagger import swagger

from analytics_api.analytics.nyc_taxi import NycTotalTrips
from analytics_api.resource import create_analytics_resources, ByDateRange
from analytics_api.sources import DataSource

totaltrips = create_analytics_resources(
    analytics={'get': NycTotalTrips},
    resource_type=ByDateRange,
    data_source=DataSource.from_bigquery(
        authentication=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        use_legacy_sql=False,
        use_query_cache=True)
)
totaltrips.__doc__ = """Total number of trips per day in the date range,
 Based on the pickup time of the trip."""
totaltrips.get = swagger.operation(notes="Gets the total count of trips, inclusive from a given range of dates",
                                   parameters=[
                                       {
                                           "name": "start",
                                           "description": "Start date, inclusive to get total count of trips",
                                           "required": True,
                                           "allowMultiple": False,
                                           "dataType": 'Date in ISO 8601 format',
                                           "paramType": "query"
                                       },
                                       {
                                           "name": "end",
                                           "description": "End date, inclusive to get total count of trips,"
                                                          "defaults to today's date when query is not given",
                                           "required": False,
                                           "allowMultiple": False,
                                           "dataType": 'Date in ISO 8601 format',
                                           "paramType": "query"
                                       },
                                   ],
                                   nickname="Total trip count",
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
                                   )(totaltrips.get)

totaltrips = swagger.model(totaltrips)
