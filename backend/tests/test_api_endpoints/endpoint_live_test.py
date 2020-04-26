from flask import url_for
from tests.conftest import endpoints
import requests
import pytest


@pytest.mark.parametrize('endpoint', endpoints)
def test_endpoint_status(client, endpoint):
    res = client.get(url_for(endpoint))
    assert res.status_code == 200


@pytest.mark.usefixtures('live_server')
@pytest.mark.integrationtest
class TestLiveServer:

    @pytest.mark.parametrize('path', endpoints)
    def test_endpoint_live_path_is_up_and_running(self, path):
        url = url_for(path, _external=True)
        res = requests.get(url)
        assert res.status_code == 200
