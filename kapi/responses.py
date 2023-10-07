
class Response:
	def __init__(self, method, handler, variables):
		self.method = method
		self.handler = handler
		self.variables = variables
		self.done = False

	async def serve(self, writer):
		# print(f'handling {self.method} {self.handler} {self.variables}')
		if self.variables:
			output = await self.handler(**self.variables)
		else:
			output = await self.handler()
		# TODO [Identify response output type] (JSON? HTML? Image? Audio? Websocket?! ..?!!)
		# 	TODO [Serialize JSON]
		# 	TODO [Handle Websocket]
		# 	TODO [Cache Static Output] (compress and return it to the app?) | (Store it somehow?)

		# TODO [Create Headers] (based on output?)
		headers = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'

		if output:
			# TODO [Faster Serialization]?
			data = bytes(f"{headers} <html>{output}</html> \r\n\r\n", "utf-8")
			writer.write(data)
		await writer.drain()
		writer.close()
		self.done = True
