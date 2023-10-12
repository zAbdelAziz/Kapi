from .parser.headers import *

import json


class BaseResponse:
	__slots__ = (
		'protocol', 'status', 'content_type', 'cache',
		'headers', 'body', 'output'
	)

	def __init__(self, body: bytes = None, protocol: bytes = HTTP1_1,
				status: int = 200,
				content_type: bytes = HTML_TYPE,
				cache: bool = False
				):
		# TODO [Convert to Stream] !!important
		self.protocol: bytes = protocol
		self.status: int = status
		self.content_type: bytes = content_type
		self.cache = CACHE_ALL if cache else CACHE_NONE

		# TODO [Optimize]
		self.body: bytes = body
		if self.body and status == 200:
			self.headers: bytes = self.build_headers(STATUS_200)
			self.output = b"".join([self.headers, self.body, SEP, SEP])
		elif not self.body:
			# TODO [Cache]
			self.status = 204
			self.headers: bytes = self.build_headers(STATUS_204)
			self.output = b"".join([self.headers, SEP])

	def build_headers(self, status):
		# TODO [Optimize]
		return b"".join([self.protocol, SPC, status, SEP,
						 CONTENT_TYPE, COL, SPC, self.content_type, SEP,
						 self.cache,
						 SEP, SEP])


class Response(BaseResponse):
	def __init__(self, data: str = None, cache: bool = False):
		# TODO [Compress]
		body: bytes = bytes(data, "utf-8")
		super().__init__(body=body, content_type=HTML_TYPE, cache=cache)


class JSON(BaseResponse):
	def __init__(self, data: dict = None, cache: bool = True):
		# TODO [Serialize JSON USING MSGSPEC]
		body: bytes = json.dumps(data).encode('utf-8') if data else None
		super().__init__(body=body, content_type=JSON_TYPE, cache=cache)
