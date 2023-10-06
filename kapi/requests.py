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
