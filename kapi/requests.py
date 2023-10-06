import os
import asyncio
from typing import AsyncIterator


class Request:
	def __init__(self):
		self.chunk_size = 128

	@staticmethod
	async def read_request(reader: asyncio.StreamReader):
		lines = []
		line = await reader.readline()
		while line and line != b'\r\n':
			lines.append(line)
			line = await reader.readline()
		return lines

	async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
		x = await self.read_request(reader)
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
