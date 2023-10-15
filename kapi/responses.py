from . import json_encoder
from .parser.headers import *


class WebResponse:
	"""Simple HTTP Response"""

	__slots__ = (
		'chunk_size', '_data',
		'protocol', 'status',
		'_content_type', 'content_type', 'cache',
		'headers', 'body', 'path',
		'_eof'
	)

	def __init__(self,
				data: str | dict = None,
				path: str = None,
				protocol: bytes = HTTP1_1,
				status: int = 200,
				content_type: str = 'html',
				cache: bool = False,
				chunk_size=128,):

		self.chunk_size: int = chunk_size
		self._data: str | dict = data
		self._eof: bool = False
		self.body: bytearray = bytearray()

		self.protocol: bytes = protocol
		self.status: int = status
		# TODO [Use Assets and Body Cache] [Allow to edit max-age] ??
		self.cache: bytes = CACHE_ALL if cache else CACHE_NONE

		if path:
			content_type = path.split('.')[-1]
			self._data = path
		self._content_type = content_type
		self.content_type: bytes = MIME_TYPES.get(content_type)

	def build_headers(self):
		# TODO [Optimize] !!Important
		return b"".join([self.protocol, SPC, STATUS.get(self.status), SEP,
						CONTENT_TYPE, COL, SPC, self.content_type, SEP,
						self.cache, SEP, SEP])

	async def stream_data(self, request):
		if self.status == 200:
			match self.get_streamer():
				case 'txt':
					await self.stream_chunks(request, self._data)
				case 'json':
					# TODO [Optimize]
					self.write(request.writer, json_encoder.encode(self._data))
				case 'img':
					# TODO [Optimize]
					with open(self._data, 'rb') as f:
						self.write(request.writer, f.read())
		await request.writer.drain()

	def get_streamer(self):
		if self._content_type in MIME_IMG:
			return 'img'
		elif self._content_type in MIME_TXT:
			return 'txt'
		elif self._content_type == 'json':
			return 'json'

	async def stream_chunks(self, request, data):
		for i in range(0, len(data), self.chunk_size):
			chunk = memoryview(bytes(self._data[i:i + self.chunk_size], 'utf-8'))
			self.write(request.writer, chunk)
			request.loop.create_task(self.extend_body(chunk))
			if len(chunk) <= self.chunk_size or not chunk:
				self._eof = True
				break

	async def stream_f_chunks(self, request, data):
		for i in range(0, len(data), self.chunk_size):
			chunk = memoryview(self._data[i:i + self.chunk_size])
			print(chunk)
			self.write(request.writer, chunk)
			request.loop.create_task(self.extend_body(chunk))
			if len(chunk) <= self.chunk_size or not chunk:
				self._eof = True
				break

	@staticmethod
	def write(writer, chunk):
		writer.write(chunk)

	async def extend_body(self, chunk):
		self.body.extend(chunk)
