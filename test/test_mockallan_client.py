import pytest
from mockallan_client import MockallanClient


@pytest.fixture
def mockallan_client() -> MockallanClient:

	return MockallanClient(base_url='http://127.0.0.1:8080')



def test_assert_called_assert_success(mockallan_client: MockallanClient):

	mockallan_client.post(
		'/orders/order_9b3e',
		json={"foo": "bar"},
		headers={
			"Content-Type": "application/json"
		}
	)
	mockallan_client.assert_called('POST', '/orders/order_9b3e')


def test_assert_called_assert_error(mockallan_client: MockallanClient):

	with pytest.raises(AssertionError):
		mockallan_client.assert_called('POST', '/orders/order_9b3e')


def test_aaa(mockallan_process, mockallan_client: MockallanClient):

	with pytest.raises(AssertionError):
		mockallan_client.assert_called('POST', '/orders/order_9b3e')
