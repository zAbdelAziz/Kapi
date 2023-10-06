from httptools import HttpRequestParser


class Request:
	def __init__(self, reader=None):
		self.reader = reader
		self.parser = HttpRequestParser(self)
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

	async def read(self):
		while True:
			data = await self.reader.read(self.chunk_size)
			self.parser.feed_data(data)
			if not data or self.EOF:
				break

