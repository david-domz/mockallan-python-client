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
    raise AssertionError(f'{title}. {detail}')
AssertionError: Expected POST /orders to be called 1 times. Called 0 times.

```

## Using `mockallan-python-client` In `pytest` Environment

```python
import pytest

@pytest.fixture(scope='session)
def mockallan_client() -> MockallanClient:

    return MockallanClient(base_url='http://localhost:8080')


def test_order_add_product(mockallan_client: MockallanClient):

    # ... Run software under test use case...

    mockallan_client.assert_called('POST', '/orders/order_e2b9/products')
```

## Related Repositories

See `mockallan` at https://github.com/david-domz/mockallan.
See `mockallan-docker` at https://github.com/david-domz/mockallan-docker.
