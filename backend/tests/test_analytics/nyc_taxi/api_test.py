import datetime

import pandas as pd
import pytest

from analytics_api.analytics import nyc_taxi
from analytics_api.analytics.nyc_taxi import NycTotalTrips, NycAverageFareHeatMap, NycAverageSpeed24hours
from analytics_api.utils.errors import NoDataError


@pytest.fixture
def easy_query(monkeypatch):
    query = "SELECT * from {tables} where start_date = {start_date} and end_date = {end_date}"
    monkeypatch.setattr(NycTotalTrips, 'query', query)


@pytest.fixture
def easy_fill(monkeypatch):
    def fill_sql_from_clause(x, y, z):
        return "start={start_date},end={end_date}"

    monkeypatch.setattr(nyc_taxi.api, 'fill_sql_from_clause_using_table_names_and_columns',
                        fill_sql_from_clause)


@pytest.fixture()
def easy_tables_to_query(monkeypatch):
    monkeypatch.setattr(nyc_taxi.api, 'get_table_names_with_start_end_dates',
                        lambda start, end: ['yellow_2017', 'yellow_2018'])


@pytest.fixture
def get_table_names_with_start_end_dates_raises_no_data(monkeypatch):
    def raise_error(start, end):
        raise NoDataError

    monkeypatch.setattr(nyc_taxi.api, 'get_table_names_with_start_end_dates',
                        raise_error)


def test_nyc_total_trips_start_end(easy_query, easy_fill, easy_tables_to_query):
    expected = "start=2016-01-01,end=2017-01-02"

    assert NycTotalTrips.get_data(datetime.datetime(2016, 1, 1), datetime.datetime(2017, 1, 2)) == expected


def test_nyc_total_trips_start_exceeds_end(easy_query, easy_fill, easy_tables_to_query):
    expected = "start=2017-01-03,end=2017-01-03"
    assert NycTotalTrips.get_data(datetime.datetime(2017, 1, 3), datetime.datetime(2017, 1, 2)) == expected


def test_nyc_total_trips_no_data_error(easy_query, easy_fill, get_table_names_with_start_end_dates_raises_no_data):
    assert NycTotalTrips.get_data(datetime.datetime(2017, 1, 3), datetime.datetime(2017, 1, 2)) == ""


def test_nyc_total_trips_process_no_data():
    assert NycTotalTrips.process_data(pd.DataFrame()) == []


def test_nyc_average_fare_heatmap_process_no_data():
    assert NycAverageFareHeatMap.process_data(pd.DataFrame()) == []


def test_nyc_average_speed_process_no_data():
    assert NycAverageSpeed24hours.process_data(pd.DataFrame()) == []
