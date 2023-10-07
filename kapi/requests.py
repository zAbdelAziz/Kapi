from httptools import HttpRequestParser


class Request:
	def __init__(self, reader=None, writer=None):
		self.reader, self.writer = reader, writer
		self.parser = HttpRequestParser(self)
		self.chunk_size = 128
		self.url, self.body = None, None
		self.EOF = False
		self.method = None
		self.handler, self.variables = None, None
		self.handler = None
		self.variables = None
		self.done = False

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

	async def serve(self):
		# print(f'handling {self.method} {self.handler} {self.variables}')
		if self.variables:
			output = await self.handler(**self.variables)
		else:
			output = await self.handler()
		# TODO [Identify response output type] (JSON? HTML? Image? Audio? Websocket?! ..?!!)
		# 	TODO [Serialize JSON]
		# 	TODO [Handle Websocket]
		# 	TODO [Cache Static Output] (compress and return it to the app?) | (Store it somehow?)

		# TODO [Create Headers] (based on output?)
		headers = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'

		if output:
			# TODO [Faster Serialization]?
			data = bytes(f"{headers} <html>{output}</html> \r\n\r\n", "utf-8")
			self.writer.write(data)
		await self.writer.drain()
		self.writer.close()
		self.done = True
