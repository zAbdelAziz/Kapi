
class Response:
	def __init__(self):
		pass

	async def prepare(self, headers: str = None) -> bytes:
		# TODO [Identify response type]
		# TODO [Handle response] (e.g. add headers, serialize json)
		return bytes(f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r
				\r\n
				<!doctype html>
				<html>
				<p>Tester</p>
				</html>
				\r\n\r\n
				""", "utf-8")
