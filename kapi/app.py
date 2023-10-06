import asyncio
import json

from .config import Config
from .routing import Router
from .requests import Request


class App:
	def __init__(self, routes=None, config_path=None):
		self.host, self.port = None, None
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])
		self.handler = Request()

	async def handle_request(self, reader, writer):
		data = await reader.read()
		request = data.decode()

		path = self.extract_path(request)
		handler, variables = await self.router.resolve(path)

		if handler and variables:
			print('handling dynamic')
			response = await handler(variables)
		elif handler and not variables:
			print('handling static')
			response = await handler()
		else:
			print('handling 404')
			raise NotImplemented('Could not find handler for the request')

		# response = json.dumps(response)
		# http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
		http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\nContent-Type: text/html\r\n\r\n{response}"

		writer.write(http_response.encode())
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
		print(f'Starting Server at http://{self.host} on {self.port}..')
		async with server:
			await server.serve_forever()

	def run(self, host: str = None, port: int = None):
		asyncio.run(self.start_server(host, port))
