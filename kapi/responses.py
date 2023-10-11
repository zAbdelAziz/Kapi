from .parser.headers import *

import json


class BaseResponse:
	__slots__ = (
		'headers', 'body', 'output'
	)

	def __init__(self, status: int = 200):
		# TODO [Get http version]
		# TODO [Get status]
		self.headers: bytearray = bytearray()
		self.body: bytes | None
		self.output: bytes | None


class Response(BaseResponse):
	def __init__(self, data: str):
		super().__init__()
		# TODO [Serialize JSON USING MSGSPEC]
		self.data: bytes = bytes(data, "utf-8")
		self.headers = self.build_headers()
		self.output = b"".join([self.headers, self.data, SEP, SEP])

	@staticmethod
	def build_headers():
		# TODO [Optimize]
		http = b"".join([HTTP1_1, SPC])
		status = b"".join([STATUS_200, SEP])
		content_type = b"".join([CONTENT_TYPE, COL, SPC, HTML_TYPE, SEP])
		return b"".join([http, status, content_type, SEP])


class JSON(BaseResponse):
	def __init__(self, data: dict):
		super().__init__()
		# TODO [Serialize JSON USING MSGSPEC]
		self.data: bytes = json.dumps(data).encode('utf-8')
		self.headers = self.build_headers()
		self.output = b"".join([self.headers, self.data, SEP, SEP])

	@staticmethod
	def build_headers():
		# TODO [Optimize]
		http = b"".join([HTTP1_1, SPC])
		status = b"".join([STATUS_200, SEP])
		content_type = b"".join([CONTENT_TYPE, COL, SPC, JSON_TYPE, SEP])
		return b"".join([http, status, content_type, SEP])