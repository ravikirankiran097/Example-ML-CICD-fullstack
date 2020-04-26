from functools import wraps


class NoDataError(Exception, BaseException):
    pass


def return_value_if_error_raised(default_value, error):
    """
    A decorator that replaces the return value of a function if the function raises an error
    :param default_value: value to return inplace of the function returns
    :param error: error to catch
    :return: decorated function
    """

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error:
                return default_value

        return _wrapped_func

    return decorator
