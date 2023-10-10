import asyncio
import websockets

from threading import Thread

# Temporary
# import cProfile
# import pstats

from .config import Config
from .routing import Router
from .requests import Request

import cProfile


# Temporary
# def f8_alt(x):
# 	# Increase profiler precision
# 	return "%14.9f" % x
# pstats.f8 = f8_alt


class App:
	def __init__(self, host: str = None, port: int = None, ws_port: int = None, routes=None, config_path: str = None):
		self.host, self.port, self.ws_port = host, port, ws_port
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])
		# Separate Threads, Loops and Servers
		self.http_thread, self.ws_thread = None, None
		self.loop, self.http_loop, self.ws_loop = None, None, None
		self.http_server, self.ws_server = None, None
		# Profile
		self.profiler = cProfile.Profile()

	async def start_http(self):
		self.http_server = await asyncio.start_server(self.handle_http, self.host, self.port)
		print(f'Starting HTTP Server at http://{self.host}:{self.port} ..')
		await self.http_server.serve_forever()

	async def start_websocket(self):
		self.websocket_server = await websockets.serve(self.handle_websocket, self.host, self.ws_port)
		print(f'Starting WebSocket Server at ws://{self.host}:{self.ws_port} ..')
		await self.websocket_server.wait_closed()

	async def start(self):
		self.http_loop = asyncio.new_event_loop()
		self.ws_loop = asyncio.new_event_loop()

		self.http_thread = Thread(target=self.http_loop.run_until_complete, args=(self.start_http(),))
		# self.http_thread.daemon = True

		self.ws_thread = Thread(target=self.ws_loop.run_until_complete, args=(self.start_websocket(),))
		# self.ws_thread.daemon = True

		try:
			self.http_thread.start()
			self.ws_thread.start()
		except KeyboardInterrupt:
			self.http_server.close()
			self.ws_server.close()
			self.cleanup()

	# Handle cleanup here
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
		self.loop = asyncio.get_event_loop()
		# asyncio.run(self.start_server())
		asyncio.run(self.start())

	async def handle_websocket(self, websocket, path):
		# TODO [Create a separate router] (Or perhaps add some variable to the existing)
		async for message in websocket:
			# Just an echo message for now
			await websocket.send(message)

	async def handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		# TODO [Fire and forget mechanism] !!Important
		request: Request = Request(reader=reader, writer=writer, loop=self.http_loop)

		# TODO Optimize Read Request [Currently Longest task]
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
