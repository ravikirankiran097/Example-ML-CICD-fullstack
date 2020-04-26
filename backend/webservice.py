import json
import typing

from flask import Flask
from flask import make_response
from flask_restful import Api
from flask_restful_swagger import swagger


application = Flask("analytics_api")

api = Api(
    application,
    default_mediatype='application/json',
)

api = swagger.docs(api,
                   apiVersion='0.1',
                   api_spec_url='/spec',
                   basePath='0.0.0.0:8080',
                   resourcePath='/',
                   produces='application/json',
                   description="This is an analytics service over nyc taxi green and yellow data at BigQuery, provides "
                               "endpoints: /total_trips, /average_fare_heatmap and /average_speed_24hrs"
                   )


@api.representation('application/json')
def output_data_pretty(data: typing.Any, code: int, headers=None):
    """
    Replaces the default json.dumps with one that sorts and indents the keys for pretty print.
    """
    formatted_data = json.dumps(data,
                                sort_keys=True,
                                indent=1)
    resp = make_response(formatted_data, code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(totaltrips, '/total_trips',
                 endpoint='totaltrips')
api.add_resource(averagefareheatmap, '/average_fare_heatmap',
                 endpoint='averagefareheatmap')
api.add_resource(averagespeed24, '/average_speed_24hrs',
                 endpoint='averagespeed24')

if __name__ == '__main__':
    application.run(host='0.0.0.0',
                    port=8080,
                    debug=True)
