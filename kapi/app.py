import asyncio
import json

from .config import Config
from .routing import Router
from .requests import Request


class App:
	def __init__(self, host=None, port=None, routes=None, config_path=None):
		self.host, self.port = host, port
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])
		self.request = Request()

	async def start_server(self):
		server = await asyncio.start_server(self.handle, self.host, self.port)
		print(f'Starting Server at http://{self.host} on {self.port}..')
		async with server:
			await server.serve_forever()

	def run(self, host: str = None, port: int = None):
		self.host = host if host else self.config['default_run']['host']
		self.port = port if port else self.config['default_run']['port']
		asyncio.run(self.start_server())

	async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		x = await self.request.read_request(reader)
		print(x)
		data = bytes(f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r
				\r\n
				<!doctype html>
				<html>
				<p>Tester</p>
				</html>
				\r\n\r\n
				""", "utf-8")
		writer.write(data)
		await writer.drain()
		writer.close()
		print('Done')
