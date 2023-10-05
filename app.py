from config import Config
from routing import Router, Route


class App:
	def __init__(self, config, routes):
		self.config = Config(config)
		self.router = Router(routes)

