
class Response:
	def __init__(self, method, handler, variables):
		self.method = method
		self.handler = handler
		self.variables = variables

	async def serve(self, writer):
		print(f'handling {self.method} {self.handler} {self.variables}')
		# TODO [Identify response output type]
		# 	TODO [Serialize JSON]
		if self.variables:
			output = await self.handler(**self.variables)
		else:
			output = await self.handler()

		# TODO [Create Headers] (based on output?)
		headers = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'

		# TODO [Faster Serialization]?
		if output:
			data = bytes(f"{headers} {output} \r\n\r\n", "utf-8")
			writer.write(data)
		await writer.drain()
		writer.close()
