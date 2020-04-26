from datetime import datetime

DT_FORMAT = '%Y-%m-%d'


def extract_date_string(date_string: str) -> datetime:
    """
    Converts string to datetime if its provided in YYYY-mm-dd format

    >>> extract_date_string('2019-01-01')
    datetime.datetime(2019, 1, 1, 0, 0)

    >>> extract_date_string('2019-12-23')
    datetime.datetime(2019, 12, 23, 0, 0)

    :param date_string: string in YYYY-mm-dd format
    :return: datetime object
    """
    return datetime.strptime(date_string, DT_FORMAT)


def get_current_datetime():
    """Wrapper to get datetime now so that it can be monkey patched for testing purposes"""
    return datetime.now()
