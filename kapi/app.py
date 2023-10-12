import asyncio
import websockets

from threading import Thread

# Temporary
# import cProfile
# import pstats

from .config import Config
from .routing import Router
from .default_routes import route_404

from .requests import Request
from .responses import BaseResponse

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
		# Profiler
		self.profiler = cProfile.Profile()

	async def start_http(self):
		self.http_server = await asyncio.start_server(self.handle_http, self.host, self.port)
		print(f'Starting HTTP Server at http://{self.host}:{self.port} ..')
		await self.http_server.serve_forever()

	async def start_websocket(self):
		self.ws_server = await websockets.serve(self.handle_websocket, self.host, self.ws_port)
		print(f'Starting WebSocket Server at ws://{self.host}:{self.ws_port} ..')
		await self.ws_server.wait_closed()

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
			self.http_thread.join()
			self.ws_thread.join()
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
		asyncio.run(self.start_server())
		# asyncio.run(self.start())

	async def handle_websocket(self, websocket, path):
		# TODO [Create a separate router] (Or perhaps add some variable to the existing)
		async for message in websocket:
			# Just an echo message for now
			await websocket.send(message)

	async def handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		# TODO [Fire and forget mechanism] !!Important
		request: Request = Request(reader=reader, writer=writer, loop=self.loop)

		# TODO Optimize Read Request [Currently Longest task]
		await request.read()

		request.method, request.handler, request.variables = await self.router.resolve(request.url)

		# self.profiler.enable()
		if request.handler is not None:
			try:
				# TODO [Cache Output] (compress and return it to the app?) | (Store it somehow?)
				response = await request.serve()
			except:
				# TODO [Handle Errors like 40x, 50x]
				response = BaseResponse(status=500)
				error = str(500)
				response.output = bytes(f"'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n' <html> Something went Wrong - {error}</html> \r\n\r\n", "utf-8")
		else:
			# TODO [Handle 404]
			path = f"/404{request.url.decode()}"
			print(bytes(path, 'utf-8'))
			request.method, request.handler, request.variables = await self.router.resolve(bytes(path, 'utf-8'))
			response = await request.serve()

		if response:
			# TODO [Ensure Response is a BaseRequest Child]
			writer.write(response.output)

		# TODO [Upgrade connection?]
		await writer.drain()
		writer.close()
		# self.profiler.disable()
		# self.profiler.print_stats(sort='cumulative')
		writer.close()

		# TODO [Handle Websocket Upgrade]
