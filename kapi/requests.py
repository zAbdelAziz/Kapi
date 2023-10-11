from httptools import HttpRequestParser


class Request(HttpRequestParser):
	# TODO [Rewrite Streamer & HttpRequestParser -> to optimize the read]
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
		self.handler = None						# -> Response
		self.variables: dict = None

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
			response = await self.handler(**self.variables)
		else:
			response = await self.handler()

		return response

