from config import Config
from routing import Router
import asyncio


class App:
	def __init__(self, routes=None, config_path=None):
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

	async def run(self, host: str = None, port: int = None):
		if not host:
			host = self.config['default_run']['host']
		if not port:
			port = self.config['default_run']['port']
		server = await asyncio.start_server(self.handle_request, host, port)
		print(f'Starting Server at {host} on {port}..')
		async with server:
			await server.serve_forever()
