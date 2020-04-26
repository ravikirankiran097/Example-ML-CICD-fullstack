import pytest

from analytics_api.utils.errors import return_value_if_error_raised, NoDataError


def test_return_value_if_error_raised_catch():
    @return_value_if_error_raised(0, OSError)
    def test():
        raise OSError

    assert test() == 0


def test_return_value_if_error_raised_no_catch():
    with pytest.raises(ValueError):
        @return_value_if_error_raised(0, OSError)
        def test():
            raise ValueError

        assert test() != 0


def test_no_data_error_exception_not_caught():
    def test():
        raise ValueError

    with pytest.raises(ValueError):
        try:
            a = test()
        except NoDataError:  # No catch
            a = 2
        assert a != 2


def test_no_data_error_exception_caught():
    def test():
        raise NoDataError

    try:
        a = test()
    except NoDataError:  # Catch on specific error
        a = 1
    assert a == 1
