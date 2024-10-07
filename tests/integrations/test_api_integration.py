from pytest import mark
from checkers.clients.api_client import Client


@mark.integration
def test_healthcheck(client: Client):
    assert client.healthcheck()
