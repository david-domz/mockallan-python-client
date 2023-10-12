# `mockallan` Python Client

Python client for [mockallan](https://github.com/david-domz/mockallan).


## Getting Started

1. First of all, we must create a `MockallanClient` instance.


```python
from mockallan_client import MockallanClient

mockallan_client = MockallanClient(base_url='http://localhost:8080')

```

2. We invoke `assert_called()` to verify that a particular endpoint was requested by our software under test.

If it was called then the assert method returns silently.

```python
mockallan_client.assert_called('POST', '/orders/order_e2b9/products')
```

3. Otherwise if it wasn't called then the assert method raises an assertion, similarly to the standard python `assert()` function.

```python
mockallan_client.assert_called('POST', '/orders')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "mockallan_client.py", line 19, in assert_called
    raise AssertionError(f'{title}. {detail}')
AssertionError: Expected POST /orders to be called 1 times. Called 0 times.


```

## Related Repositories

See `mockallan` at https://github.com/david-domz/mockallan.
See `mockallan-docker` at https://github.com/david-domz/mockallan-docker.
