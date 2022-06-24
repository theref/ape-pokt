from pathlib import Path

import pytest
from ape import networks
from ape.api import NetworkAPI, TransactionAPI
from ape.api.config import PluginConfig
from ape.exceptions import ContractLogicError
from web3 import Web3
from web3.exceptions import ContractLogicError as Web3ContractLogicError

from ape_pokt.providers import MissingProjectKeyError, PoktEthereumProvider

# from web3 import Web3


@pytest.fixture
def missing_token(mocker):
    mock = mocker.patch("os.environ.get")
    mock.return_value = None
    return mock


@pytest.fixture
def token(mocker):
    mock = mocker.patch("os.environ.get")
    mock.return_value = "TEST_TOKEN"
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


@pytest.fixture
def mock_transaction(mocker):
    return mocker.MagicMock(spec=TransactionAPI)


@pytest.fixture
def mock_web3(mocker):
    mock = mocker.MagicMock(spec=Web3)
    mock.eth = mocker.MagicMock()
    mock.manager = mocker.MagicMock()
    return mock


def test_when_no_api_key_raises_error(missing_token, pokt_provider):
    with pytest.raises(MissingProjectKeyError) as err:
        pokt_provider.connect()

    expected = "Must set one of $WEB3_POKT_PROJECT_ID, $WEB3_POKT_API_KEY."
    assert expected in str(err.value)


def test_provider_works():
    with networks.ethereum.mainnet.use_provider("pokt") as provider:
        assert isinstance(provider, PoktEthereumProvider)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0


def test_send_transaction_reverts(pokt_provider, mock_web3, mock_transaction):
    expected_revert_message = "EXPECTED REVERT MESSAGE"
    mock_web3.eth.send_raw_transaction.side_effect = Web3ContractLogicError(
        f"execution reverted : {expected_revert_message}"
    )
    pokt_provider._web3 = mock_web3

    with pytest.raises(ContractLogicError):
        pokt_provider.send_transaction(mock_transaction)
