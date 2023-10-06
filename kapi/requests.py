from httptools import HttpRequestParser


class Request:
	def __init__(self):
		self.chunk_size = 128
		self.url, self.body = None, None
		self.EOF = False

	def on_url(self, url: bytes):
		# TODO [Add task to resolve the url]  ??
		self.url = url

	def on_body(self, body: bytes):
		self.body = body

	def on_message_complete(self):
		self.EOF = True

	async def read(self, reader):
		_parser = HttpRequestParser(self)
		while True:
			data = await reader.read(self.chunk_size)
			_parser.feed_data(data)
			if not data or self.EOF:
				break

