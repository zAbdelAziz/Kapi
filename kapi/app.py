import asyncio

from .config import Config
from .routing import Router
from .requests import Request
from .responses import Response


class App:
	def __init__(self, host: str = None, port: int = None, routes=None, config_path: str = None):
		self.host, self.port = host, port
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])
		self.loop = None

	async def start_server(self):
		server = await asyncio.start_server(self.handle, self.host, self.port)
		print(f'Starting Server at http://{self.host} on {self.port}..')
		self.loop = asyncio.get_event_loop()
		async with server:
			await server.serve_forever()

	def run(self, host: str = None, port: int = None):
		self.host = host if host else self.config['default_run']['host']
		self.port = port if port else self.config['default_run']['port']
		asyncio.run(self.start_server())

	async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		# TODO [Fire and forget mechanism] !!Important
		request = Request(reader=reader, writer=writer)
		await request.read()
		request.method, request.handler, request.variables = await self.router.resolve(request.url)
		if request.handler is not None:
			await request.serve()
		else:
			# TODO Handle 404
			writer.close()
