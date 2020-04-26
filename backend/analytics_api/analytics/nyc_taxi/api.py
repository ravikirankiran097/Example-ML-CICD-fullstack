from functools import partial

import pandas as pd

from analytics_api.analytics.api_base import Analytics
from analytics_api.utils.datetime import DT_FORMAT
from analytics_api.utils.errors import NoDataError, return_value_if_error_raised
from .constants import SUPPORTED_NYC_BQ_TABLES
from .geometry import convert_lat_long_into_s2_cells_level
from .util import (fill_sql_from_clause_using_table_names_and_columns,
                   get_table_names_with_start_end_dates)

get_table_names_with_start_end_dates = partial(get_table_names_with_start_end_dates,
                                               tables=SUPPORTED_NYC_BQ_TABLES)
return_empty_data_if_error = partial(return_value_if_error_raised, [])


class NycTotalTrips(Analytics):
    from analytics_api.analytics.nyc_taxi.sql_queries import query_count_trips_between_dates as query

    @classmethod
    @return_value_if_error_raised("", NoDataError)
    def get_data(cls, start, end):
        if start > end:
            end = start

        tables_to_query = get_table_names_with_start_end_dates(start, end)
        sql = fill_sql_from_clause_using_table_names_and_columns(cls.query,
                                                                 tables_to_query,
                                                                 ('pickup_datetime',))

        start, end = start.strftime(DT_FORMAT), end.strftime(DT_FORMAT)
        return sql.format(start_date=start, end_date=end)

    @classmethod
    @return_empty_data_if_error(NoDataError)
    def process_data(cls, data: pd.DataFrame):
        if data.size == 0:
            raise NoDataError("Input dataframe is empty")
        data['date'] = pd.to_datetime(data['date'])
        data['date'] = data['date'].dt.strftime(DT_FORMAT)

        return data.to_dict(orient='records')


class NycAverageFareHeatMap(Analytics):
    from analytics_api.analytics.nyc_taxi.sql_queries import query_fare_by_pickup_location as query

    @classmethod
    @return_value_if_error_raised("", NoDataError)
    def get_data(cls, date):
        tables_to_query = get_table_names_with_start_end_dates(date, date)
        sql = fill_sql_from_clause_using_table_names_and_columns(cls.query,
                                                                 tables_to_query,
                                                                 ('pickup_datetime',
                                                                  'pickup_latitude',
                                                                  'pickup_longitude',
                                                                  'fare_amount'))
        date = date.strftime(DT_FORMAT)
        return sql.format(date=date)

    @classmethod
    @return_empty_data_if_error(NoDataError)
    def process_data(cls, data: pd.DataFrame):
        if data.size == 0:
            raise NoDataError("Input dataframe is empty")

        def s2_cell_id(*args, **kwargs):
            return convert_lat_long_into_s2_cells_level(*args, **kwargs).ToToken()

        data['s2id'] = data.apply(lambda df: s2_cell_id(df['pickup_latitude'],
                                                        df['pickup_longitude'],
                                                        16), axis=1)
        # data = data.drop(columns=['pickup_latitude', 'pickup_longitude'])
        data_grouped_by_s2id_averaged = data.groupby('s2id').mean().reset_index()

        return data_grouped_by_s2id_averaged.to_dict(orient='records')


class NycAverageSpeed24hours(Analytics):
    from analytics_api.analytics.nyc_taxi.sql_queries import query_average_speed_24hours as query

    @classmethod
    @return_value_if_error_raised("", NoDataError)
    def get_data(cls, date):
        tables_to_query = get_table_names_with_start_end_dates(date, date)
        sql = fill_sql_from_clause_using_table_names_and_columns(cls.query,
                                                                 tables_to_query,
                                                                 ('trip_distance',
                                                                  'dropoff_datetime',
                                                                  'pickup_datetime',))
        date = date.strftime(DT_FORMAT)
        return sql.format(date=date)

    @classmethod
    @return_empty_data_if_error(NoDataError)
    def process_data(cls, data):
        if data.size == 0:
            raise NoDataError("Input dataframe is empty")

        return data.to_dict(orient='records')
