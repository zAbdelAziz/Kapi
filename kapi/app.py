import asyncio
import websockets

# Temporary
import cProfile
import pstats

from .config import Config
from .routing import Router
from .requests import Request


# from .responses import Response


# Temporary
def f8_alt(x):
	# Increase profiler precision
	return "%14.9f" % x
pstats.f8 = f8_alt


class App:
	def __init__(self, host: str = None, port: int = None, ws_port: int = None, routes=None, config_path: str = None):
		self.host, self.port, self.ws_port = host, port, ws_port
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])
		self.loop = None
		self.profiler = cProfile.Profile()

	async def start_server(self):
		http_server = await asyncio.start_server(self.handle_http, self.host, self.port)
		print(f'Starting Server at http://{self.host}:{self.port} ..')

		websocket_server = await websockets.serve(self.handle_websocket, self.host, self.ws_port)
		print(f'Starting WebSocket Server at ws://{self.host}:{self.ws_port} ..')

		self.loop = asyncio.get_event_loop()
		try:
			async with http_server, websocket_server:
				await asyncio.gather(http_server.serve_forever(), websocket_server.wait_closed())
		except KeyboardInterrupt:
			http_server.close()
			websocket_server.close()

		finally:
			self.cleanup()

	def cleanup(self):
		pass

	def run(self, host: str = None, port: int = None):
		self.host = host if host else self.config['default_run']['host']
		self.port = port if port else self.config['default_run']['port']
		asyncio.run(self.start_server())

	async def handle_websocket(self, websocket, path):
		# TODO [Create a separate router] (Or perhaps add some variable to the existing)
		async for message in websocket:
			# Just an echo message for now
			await websocket.send(message)

	async def handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		# TODO [Fire and forget mechanism] !!Important
		request = Request(reader=reader, writer=writer)

		# TODO Optimize Read [Currently Longest task]
		await request.read()

		request.method, request.handler, request.variables = await self.router.resolve(request.url)

		if request.handler is not None:
			# self.profiler.enable()
			await request.serve()
		# self.profiler.disable()
		# self.profiler.print_stats(sort='cumulative')
		else:
			# TODO Handle 404
			writer.close()

	# self.profiler.disable()
	# self.profiler.print_stats(sort='cumulative')
