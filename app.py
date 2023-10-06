import multiprocessing
import asyncio

from config import Config
from routing import Router


class App:
	def __init__(self, routes=None, config_path=None):
		self.host, self.port = None, None
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])

	async def handle_request(self, reader, writer):
		data = await reader.read()
		request = data.decode()

		path = self.extract_path(request)

		handler, variables = self.router.resolve(path)

		if handler and variables:
			print('handling dynamic')
			response = handler(variables)
			print(response)
		elif handler and not variables:
			print('handling static')
			response = handler()
		else:
			print('handling 404')
			raise NotImplemented('Could not find handler for the request')

		writer.write(response.encode())
		await writer.drain()
		writer.close()

	@staticmethod
	def extract_path(request):
		lines = request.split('\n')
		if len(lines) > 0:
			request_line = lines[0]
			parts = request_line.split()
			if len(parts) > 1:
				return parts[1]
		return "/"

	async def start_server(self, host: str, port: int):
		self.host = host if host else self.config['default_run']['host']
		self.port = port if port else self.config['default_run']['port']

		server = await asyncio.start_server(self.handle_request, self.host, self.port)
		print(f'Starting Server at {self.host} on {self.port}..')
		async with server:
			await server.serve_forever()

	def run(self, host: str = None, port: int = None):
		asyncio.run(self.start_server(host, port))
