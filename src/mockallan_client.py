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


	def config(self, stub_config: dict):
		"""Set stub configuration.

		Args:
			stub_config (dict):	Stub configuration object.

		Raises:
			requests.InvalidJSONError
			requests.ConnectionError

		"""
		url = f'{self._base_url}/config'

		response = requests.put(url, json=stub_config, timeout=self._timeout)

		if response.status_code == 400:
			# TO DO: raise BadRequestResponse()
			raise AssertionError()


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
		"""Assert that an endpoint was called.

		Args:
			method (str):
			path (str):

		Raises:
			BadRequest
			Conflict
			ServerError

		"""
		url = f'{self._base_url}/assert-called?method={method}&path={path}'

		response = requests.get(url, timeout=self._timeout)

		self._handle_assert_called_response(response)


	def assert_called_once(self, method: str, path: str):
		"""Asserts that a particular endpoint was called once.

		Args:
			method (str):
			path (str):

		Raises:
			BadRequest
			Conflict
			ServerError

		"""
		url = f'{self._base_url}/assert-called-once?method={method}&path={path}'

		response = requests.get(url, timeout=self._timeout)

		self._handle_assert_called_response(response)


	def assert_called_with(
			self,
			method: str,
			path: str,
			body: Any,
			content_type: str = '',
			mockallan_validator = None):
		"""Asserts that a particular endpoint was called with certain request body.

		Args:
			method (str):
			path:
			body (dict | str | bytes):
			content_type (str):
			mockallan_validator:

		"""
		url = f'{self._base_url}/assert-called-with?method={method}&path={path}'

		MockallanClient._post_assert_with(url, body, content_type, mockallan_validator)


	def assert_called_once_with(
			self,
			method: str,
			path: str,
			body: Any,
			content_type: str = '',
			mockallan_validator = None):
		"""Asserts that a particular endpoint was called with a request body.

		Args:
			method (str):
			path:
			body (dict | str | bytes):
			content_type (str):
			mockallan_validator:

		"""
		url = f'{self._base_url}/assert-called-once-with?method={method}&path={path}'

		MockallanClient._post_assert_with(url, body, content_type, mockallan_validator)


	def call_count(self) -> int:

		raise NotImplementedError


	def call_args(self) -> Any:
		"""Retrieves the request body that the mock was last called with. """

		url = f'{self._base_url}/call-args'

		response = requests.get(url)
		if response.status_code == 409:
			# TO DO: Raise exception: No request was performed by the software under test.
			raise AssertionError()


	def call_args_list(self) -> list[dict]:
		"""Retrieves all the request and response bodies that the mock was called with. """

		request_list = {}
		url = f'{self._base_url}/call-args-list'

		response = requests.get(url)
		if response.status_code == 200:
			request_list = response.json()

		# TO DO

		return request_list


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

		MockallanClient._handle_assert_called_response(response)


	@staticmethod
	def _handle_assert_called_response(response: requests.Response):

		if response.status_code == 400:
			# TO DO: Raise BadRequest()
			raise AssertionError()

		if response.status_code == 409:
			# TO DO: Raise ConflictResponse()
			raise AssertionError()

		if int(response.status_code / 200) == 5:
			# TO DO: ServerErrorResponse()
			raise AssertionError(f'{response.status_code} {response.text}')
