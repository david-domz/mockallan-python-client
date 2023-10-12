import requests


class MockallanClient:

	def __init__(self, base_url: str):

		self._base_url = base_url
		self._timeout = 20.0

	def assert_called(self, method: str, path: str):

		url = f'{self._base_url}/assert-called?method={method}&path={path}'

		response = requests.get(url, timeout=self._timeout)
		if response.status_code == 409:
			detail = response.json()['detail']
			raise AssertionError(detail)

		if int(response.status_code / 200) == 5:
			raise AssertionError(f'{response.status_code} {response.text}')


	def assert_called_with(self, http_request, content_type: str, mockallan_validator: str = ''):
		...
