from functools import wraps

from flask_restful import Resource, reqparse, marshal_with_field

from analytics_api.utils.datetime import extract_date_string, get_current_datetime
from analytics_api.utils.serialization import EnvelopeData


def strict_parse_arguments(parser):
    """
    Strict ensures that only specified parameters are accepted and http 400 error code is given
    when incorrect parameters are input
    """

    @wraps(strict_parse_arguments)
    def _actual_decorator(func):
        @wraps(func)
        def strict_wrapper(**kwargs):
            return func(**kwargs, **parser.parse_args(strict=True,
                                                      http_error_code=400))

        return strict_wrapper

    return _actual_decorator


class ByDateSingle(Resource):
    parser = reqparse.RequestParser()
    method_decorators = [marshal_with_field(EnvelopeData), strict_parse_arguments(parser)]

    parser.add_argument('date',
                        default=get_current_datetime,
                        type=extract_date_string,
                        help='Date to get data, inclusive')


class ByDateRange(Resource):
    parser = reqparse.RequestParser()
    method_decorators = [marshal_with_field(EnvelopeData), strict_parse_arguments(parser)]

    parser.add_argument('start',
                        default=get_current_datetime,
                        type=extract_date_string,
                        help='Start date to get data from, inclusive')
    parser.add_argument('end',
                        default=get_current_datetime,
                        type=extract_date_string,
                        help='End date to get data to, inclusive')
