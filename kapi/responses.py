from . import json_encoder, __BASEDIR__
from .parser.headers import *


class BaseResponse:
	__slots__ = (
		'protocol', 'status', 'content_type', 'cache',
		'headers', 'body', 'output'
	)

	def __init__(self, body: bytes = None, protocol: bytes = HTTP1_1,
				status: int = 200,
				content_type: str = 'text',
				cache: bool = False
				):
		# TODO [Convert to Stream] !!important
		self.protocol: bytes = protocol
		self.status: int = status
		self.content_type: bytes = MIME_TYPES.get(content_type)
		# TODO [Use Assets and Body Cache] [Allow to edit max-age] ??
		self.cache: bytes = CACHE_ALL if cache else CACHE_NONE

		# TODO [Optimize]
		self.body: bytes = body
		if self.body and status == 200:
			self.headers: bytes = self.build_headers(STATUS.get(self.status))
			self.output = b"".join([self.headers, self.body, SEP, SEP])
		elif not self.body:
			# TODO [Cache]
			self.status = 204
			self.headers: bytes = self.build_headers(STATUS.get(self.status))
			self.output = b"".join([self.headers, SEP])

	def build_headers(self, status):
		# TODO [Optimize] !!Important
		return b"".join([self.protocol, SPC, status, SEP,
						CONTENT_TYPE, COL, SPC, self.content_type, SEP,
						self.cache, SEP, SEP])


class Response(BaseResponse):
	# @lru_cache(maxsize=None)
	def __init__(self, data: str = None, cache: bool = False):
		# TODO [Compress]
		body: bytes = bytes(data, "utf-8")
		super().__init__(body=body, content_type='html', cache=cache)


class JSON(BaseResponse):
	def __init__(self, data: dict = None, cache: bool = True):
		body: bytes = json_encoder.encode(data) if data else None
		# body: bytes = json.dumps(data).encode('utf-8') if data else None
		super().__init__(body=body, content_type='json', cache=cache)


class Static(BaseResponse):
	def __init__(self, path: str = None, cache: bool = True):
		# TODO [Optimize] (Stream response) !!Important
		with open(path, 'rb') as f:
			body = f.read()
		super().__init__(body=body, content_type=path.split('.')[-1], cache=cache)
