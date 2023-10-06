
class Response:
	def __init__(self, method, handler, variables):
		self.method = method
		self.handler = handler
		self.variables = variables

	async def serve(self, writer):
		print(f'handling {self.method}')
		# TODO [Identify response type]
		# TODO [Handle response] (e.g. add headers, serialize json)
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
