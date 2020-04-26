from abc import ABC


class Analytics(ABC):
    """ Standardized interface to write analytics
    where get_data is the steps to retrieve data from data source
    while process_data is to post process that data if required, before serving it
    """

    @classmethod
    def get_data(cls, **kwargs):
        """
        get data is to be used as the arguments and kwargs for data_source execute
        """
        raise NotImplementedError

    @classmethod
    def process_data(cls, data):
        """
        process_data would be called on the return values from data_source execute after get_data is provided as
        arguments
        """
        raise NotImplementedError
