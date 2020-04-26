import os

from flask_restful_swagger import swagger

from analytics_api.analytics.nyc_taxi import NycAverageFareHeatMap
from analytics_api.resource import create_analytics_resources, ByDateSingle
from analytics_api.sources import DataSource

averagefareheatmap = create_analytics_resources(
    analytics={'get': NycAverageFareHeatMap},
    resource_type=ByDateSingle,
    data_source=DataSource.from_bigquery(
        authentication=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        use_legacy_sql=False,
        use_query_cache=True),

)
averagefareheatmap.__doc__ = """The average fare (fare_amount) per pick up location S2 ID at level 16
For the given date, based on the pickup time of the trip.
"""

averagefareheatmap.get = swagger.operation(notes="Returns the average fare heatmap as a list of dictionaries with s2id "
                                                 "paired with average fare for a given date",
                                           parameters=[
                                               {
                                                   "name": "date",
                                                   "description": "Single date to get the average fare heatmap of",
                                                   "required": True,
                                                   "allowMultiple": False,
                                                   "dataType": 'Date in ISO 8601 format',
                                                   "paramType": "query"
                                               }
                                           ],
                                           nickname="Average fare",
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
                                           )(averagefareheatmap.get)

averagefareheatmap = swagger.model(averagefareheatmap)
