"""Queries for nyc taxi analytics without their FROM clauses"""

query_count_trips_between_dates = """
SELECT
    DATE(pickup_datetime) AS date,
    count(*) AS total_trips
FROM `{tables}`
WHERE
        pickup_datetime IS NOT NULL
        AND DATE(pickup_datetime) >= DATE('{start_date}')
        AND DATE(pickup_datetime) <= DATE('{end_date}')
GROUP BY date
ORDER BY date
"""

query_fare_by_pickup_location = """
SELECT
    pickup_latitude,
    pickup_longitude,
    CAST(fare_amount AS FLOAT64) AS fare
   FROM `{tables}`
   WHERE
     pickup_datetime IS NOT NULL
     AND pickup_latitude IS NOT NULL
     AND pickup_longitude IS NOT NULL
     -- Fix for bad data
     AND pickup_latitude != 0
     AND pickup_latitude >= -90
     AND pickup_latitude <= 90
     AND pickup_longitude != 0
     AND pickup_longitude >= -180
     AND pickup_longitude <= 180
     -- Good to have but increases each query by 2GB when added
--      AND trip_distance != 0
--      AND pickup_latitude != dropoff_latitude
--      AND pickup_longitude != dropoff_longitude
     AND fare_amount IS NOT NULL
     AND CAST(fare_amount AS FLOAT64) > 0  -- Validates that a trip was proper
--      AND DATETIME_DIFF(dropoff_datetime, (pickup_datetime), HOUR) > 0
     AND DATE(pickup_datetime) = DATE('{date}')
"""

query_average_speed_24hours = """
WITH trips_ended_past_24_hours AS (
    SELECT
        trip_distance,
        dropoff_datetime,
        pickup_datetime,
    FROM `{tables}`
    WHERE
        trip_distance IS NOT NULL
        AND trip_distance > 0
        AND dropoff_datetime IS NOT NULL
        AND pickup_datetime IS NOT NULL
        AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, HOUR) > 0
        AND dropoff_datetime >= DATETIME_SUB(DATETIME '{date}', INTERVAL 24 HOUR)
        )
SELECT
  AVG(trip_distance / DATETIME_DIFF(dropoff_datetime, pickup_datetime, HOUR)) AS average_speed
FROM trips_ended_past_24_hours
"""
