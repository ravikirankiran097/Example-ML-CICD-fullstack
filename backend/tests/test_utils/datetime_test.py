import pytest
from analytics_api.utils.datetime import extract_date_string
from datetime import datetime


@pytest.mark.parametrize('given', (
    '2019-04-34',
    '2019-13-26',
    '201-04-26',
    '20195-04-26',)
                         )
def test_fail_if_wrong_date_string(given):
    with pytest.raises(ValueError):
        extract_date_string(given)


@pytest.mark.parametrize('given,expected',
                         (('2019-04-26', datetime(2019, 4, 26)),
                          ('2019-4-26', datetime(2019, 4, 26)),
                          ('2019-04-2', datetime(2019, 4, 2))
                          )
                         )
def test_extract_date_string(given, expected):
    assert extract_date_string(given) == expected


@pytest.mark.freeze_time('2020-1-28')
def test_get_current_datetime():
    assert datetime.now() == datetime(2020, 1, 28)
