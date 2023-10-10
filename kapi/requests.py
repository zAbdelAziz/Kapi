from httptools import HttpRequestParser


class Request(HttpRequestParser):
	__slots__ = (
		'reader', 'writer', 'loop', 'chunk_size',
		'message',
		'method', 'url', 'body', 'EOF',
		'handler', 'variables',
		'done'
	)

	def __init__(self, reader=None, writer=None, loop=None):
		super().__init__(self)
		self.reader, self.writer = reader, writer
		self.loop = loop
		self.chunk_size: int = 256
		self.message: bytearray = bytearray()
		self.url: bytes = None
		self.body: bytes = None
		self.EOF: bool = False
		self.method: bytes = None
		self.handler, self.variables = None, None
		self.variables: dict = None
		self.done: bool = False

	def on_url(self, url: bytes):
		self.url = url

	def on_body(self, body: bytes):
		self.body = body

	def on_message_complete(self):
		self.EOF = True

	async def add_message(self, data):
		self.message.extend(data)

	async def read(self):
		while True:
			data = await self.reader.read(self.chunk_size)
			# Save Message [in a separate task]
			self.loop.create_task(self.add_message(data))
			self.feed_data(data)
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

