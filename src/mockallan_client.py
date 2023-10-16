from typing import Any
from enum import Enum
import requests


class Validator(Enum):
	JSON = 'json'
	JSONSCHEMA = 'jsonschema'
	REGEX = 'regex'


class MockallanClient:
	"""
	
	Attributes:
		_base_url (str):	Mockallan API base URL.
		_timeout (float):	Timeout in seconds passed into requests methods.

	"""
	def __init__(self, base_url: str, timeout = 20.0):

		self._base_url = base_url
		self._timeout = timeout

	def post(self, path: str, data = None, json=None, headers=None) -> requests.Response:
		"""Simulates a POST request by our System Under Test (SUT). """

		return self.request('POST', path, data, json, headers)

	def get(self, path: str, data = None, json=None, headers=None) -> requests.Response:
		"""Simulates a GET request by our System Under Test (SUT). """

		return self.request('GET', path, data, json, headers)

	def put(self, path: str, data = None, json=None, headers=None) -> requests.Response:
		"""Simulates a PUT request by our System Under Test (SUT). """

		return self.request('PUT', path, data, json, headers)

	def patch(self, path: str, data = None, json=None, headers=None) -> requests.Response:
		"""Simulates a PATCH request by our System Under Test (SUT). """

		return self.request('PATCH', path, data, json, headers)

	def request(self, method: str, path: str, data = None, json=None, headers=None) -> requests.Response:
		"""Simulates a request by our System Under Test (SUT). """

		url = f'{self._base_url}{path}'

		return requests.request(method, url, data=data, json=json, headers=headers)


	def assert_called(self, method: str, path: str):

		url = f'{self._base_url}/assert-called?method={method}&path={path}'

		response = requests.get(url, timeout=self._timeout)

		self._assert_response(response)


	def assert_called_once(self, method: str, path: str):

		url = f'{self._base_url}/assert-called-once?method={method}&path={path}'

		response = requests.get(url, timeout=self._timeout)

		self._assert_response(response)


	def assert_called_with(
			self,
			method: str,
			path: str,
			body: Any,
			content_type: str = '',
			mockallan_validator = None):

		url = f'{self._base_url}/assert-called-with?method={method}&path={path}'

		MockallanClient._post_assert_with(url, body, content_type, mockallan_validator)


	def assert_called_once_with(
			self,
			method: str,
			path: str,
			body: Any,
			content_type: str = '',
			mockallan_validator = None):

		url = f'{self._base_url}/assert-called-once-with?method={method}&path={path}'

		MockallanClient._post_assert_with(url, body, content_type, mockallan_validator)


	def call_count(self) -> int:

		raise NotImplementedError


	def call_args(self) -> Any:
		"""This is either None (if the mock hasn’t been called), or the request body that the mock was last called with. """

		raise NotImplementedError


	def call_args_list(self) -> list[dict]:

		raise NotImplementedError


	@staticmethod
	def _post_assert_with(url: str, body: Any, content_type: str = '', mockallan_validator: Validator | None = None):

		if content_type in ('application/json', 'application/jsonschema'):
						
			response = requests.post(url, json=body, headers={'Content-Type': content_type})

		elif content_type in ('text/plain', 'application/xml'):

			response = requests.post(url, body, headers={'Content-Type': content_type})

		elif mockallan_validator == Validator.JSON:

			response = requests.post(url, json=body, headers={'Content-Type': 'application/json'})

		elif mockallan_validator == Validator.JSONSCHEMA:

			response = requests.post(url, json=body, headers={'Content-Type': 'application/jsonschema'})

		elif mockallan_validator == Validator.REGEX:

			response = requests.post(url, body, headers={'Content-Type': 'text/plain'})
		else:
			response = requests.post(url, body)

		MockallanClient._assert_response(response)


	@staticmethod
	def _assert_response(response: requests.Response):

		if response.status_code == 409:
			detail = response.json()['detail']
			raise AssertionError(detail)

		if int(response.status_code / 100) == 4:
			title = response.json()['title']
			detail = response.json()['detail']
			raise AssertionError(f'{title}. {detail}')

		if int(response.status_code / 200) == 5:
			raise AssertionError(f'{response.status_code} {response.text}')
