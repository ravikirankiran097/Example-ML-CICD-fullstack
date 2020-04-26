from abc import ABC
from typing import Any

import pandas as pd


class Connector(ABC):

    def execute(self, query: Any) -> pd.DataFrame:
        raise NotImplementedError

    def authenticate(self, *args, **kwargs):
        raise NotImplementedError

    def build_client(self, *args, **kwargs):
        raise NotImplementedError


class Authentication(ABC):

    def authenticate(self, *args, **kwargs):
        raise NotImplementedError
