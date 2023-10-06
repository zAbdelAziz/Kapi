from httptools import HttpRequestParser


class BaseRequest:
	def __init__(self):
		self.url, self.header = None, None
		self.EOF = False

	def on_header(self, name: bytes, value: bytes):
		self.header = {name: value}

	def on_url(self, url: bytes):
		# TODO [Add task to resolve the url]  ??
		self.url = url

	def on_message_complete(self):
		self.EOF = True


class Requests:
	def __init__(self):
		self.chunk_size = 128

	async def read_request(self, request: BaseRequest, reader):
		_parser = HttpRequestParser(request)
		while True:
			data = await reader.read(self.chunk_size)
			_parser.feed_data(data)
			if not data or request.EOF:
				break

