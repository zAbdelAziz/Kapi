from config import Config
from routing import Router, Route


class App:
	def __init__(self, routes=None, config_path=None,):
		self.config = Config(config_path)
		self.router = Router(routes, self.config['default_attrs'])

