BQ_DATASET = 'bigquery-public-data.new_york_taxi_trips'

_SUPPORTED_NYC_BQ_TABLES = ['tlc_green_trips_2014', 'tlc_green_trips_2015', 'tlc_green_trips_2016',
                            'tlc_green_trips_2017', 'tlc_yellow_trips_2015', 'tlc_yellow_trips_2016',
                            'tlc_yellow_trips_2017']
SUPPORTED_NYC_BQ_TABLES = [f"{BQ_DATASET}.{nyc_bq_table}" for nyc_bq_table in _SUPPORTED_NYC_BQ_TABLES]
