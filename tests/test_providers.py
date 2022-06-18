from pathlib import Path

import pytest
from ape import networks
from ape.api import NetworkAPI
from ape.api.config import PluginConfig

from ape_pokt.providers import MissingProjectKeyError, PoktEthereumProvider


@pytest.fixture
def missing_token(mocker):
    mock = mocker.patch("os.environ.get")
    mock.return_value = None
    return mock


@pytest.fixture
def mock_network(mocker):
    mock = mocker.MagicMock(spec=NetworkAPI)
    mock.name = "MOCK_NETWORK"
    return mock


@pytest.fixture
def mock_config(mocker):
    return mocker.MagicMock(spec=PluginConfig)


@pytest.fixture
def pokt_provider(mock_network, mock_config) -> PoktEthereumProvider:
    return PoktEthereumProvider(
        name="pokt",
        network=mock_network,
        config=mock_config,
        request_header={},
        data_folder=Path("."),
        provider_settings={},
    )


def test_when_no_api_key_raises_error(missing_token, pokt_provider):
    with pytest.raises(MissingProjectKeyError) as err:
        pokt_provider.connect()

    expected = "Must set one of $WEB3_POKT_PROJECT_ID, $WEB3_POKT_API_KEY."
    assert expected in str(err.value)


def test_provider_works():
    with networks.ethereum.mainnet.use_provider("pokt") as provider:
        assert isinstance(provider, PoktEthereumProvider)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
