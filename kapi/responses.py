from . import json_encoder
from .parser.headers import *


class WebResponse:
	__slots__ = (
		'protocol', 'status', 'content_type', 'cache',
		'headers', 'body', 'path', 'output'
	)

	def __init__(self, data: str | dict = None, path: str = None,
				protocol: bytes = HTTP1_1, status: int = 200,
				content_type: str = 'html',
				cache: bool = False
				):
		# TODO [Convert to Stream] !!important
		self.protocol: bytes = protocol
		self.status: int = status
		# TODO [Use Assets and Body Cache] [Allow to edit max-age] ??
		self.cache: bytes = CACHE_ALL if cache else CACHE_NONE

		if path:
			content_type = path.split('.')[-1]
		self.content_type: bytes = MIME_TYPES.get(content_type)

		self.encode_data(content_type, data, path=path)

		self.headers: bytes = self.build_headers(STATUS.get(self.status))

		# TODO [Optimize]
		if self.body and status == 200:
			self.output = b"".join([self.headers, self.body, SEP, SEP])
		elif not self.body:
			self.status = 204
			self.headers: bytes = self.build_headers(STATUS.get(self.status))
			self.output = b"".join([self.headers, SEP])

	def build_headers(self, status):
		# TODO [Optimize] !!Important
		return b"".join([self.protocol, SPC, status, SEP,
						CONTENT_TYPE, COL, SPC, self.content_type, SEP,
						self.cache, SEP, SEP])

	def encode_data(self, content_type, data, path=None):
		if content_type in MIME_IMG:
			content_type = 'img'
		match content_type:
			case 'html' | 'text' | 'js' | 'css':
				self.body: bytes = bytes(data, 'utf-8')
			case 'json':
				self.body: bytes = json_encoder.encode(data) if data else None
			case 'img':
				with open(path, 'rb') as f:
					self.body: bytes = f.read()