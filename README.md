# Mockallan Python Client

Python client for [mockallan](https://github.com/david-domz/mockallan).

## Getting Started

1. Create a `MockallanClient` instance.


```python
from mockallan_client import MockallanClient

mockallan_client = MockallanClient(base_url='http://localhost:8080')

```

2. Run our software under test (SUT).
   

3. Invoke `assert_called()` to verify that a particular endpoint was called by our SUT.

```python
mockallan_client.assert_called('POST', '/orders/order_e2b9/products')
```

- If it was called then the assert method returns silently.
- Otherwise, if it wasn't called then the assert method raises an `AssertError` exception, similarly to the standard python `assert`.

E.g.
```python
mockallan_client.assert_called('POST', '/orders')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "mockallan_client.py", line 19, in assert_called
    raise AssertionError(detail)
AssertionError: Expected POST /orders to be called 1 times. Called 0 times.

```

## Using `mockallan-python-client` In `pytest` Environment

```python
import pytest
from mockallan_client import MockallanClient


@pytest.fixture(scope='session')
def mockallan_client() -> MockallanClient:

    return MockallanClient(base_url='http://localhost:8080')


def test_order_add_product(mockallan_client: MockallanClient):

    # ... Run software under test use case...

    mockallan_client.assert_called_once('POST', '/orders/order_e2b9/products')
```

## Related Repositories

- [mockallan](https://github.com/david-domz/mockallan) - lightweight HTTP server mock.
- [mockallan-docker](https://github.com/david-domz/mockallan-docker) - Containerized lightweight HTTP server mock.
