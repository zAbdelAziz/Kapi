import json


class Config:
	def __init__(self, config_path: str = None):
		if not config_path:
			self.data = self.init_config()
			self.save_config(self.data, 'config.json')
		else:
			self.data = self.read_config(config_path)

	@staticmethod
	def init_config():
		data = {}
		data['default_attrs'] = {'separator': '/', 'param_indicators': ['<', '>']}
		data['default_run'] = {'host': '127.0.0.1', 'port': 8080}
		return data

	@staticmethod
	def read_config(path):
		with open(path, 'r') as f:
			config = json.load(f)
		return config

	@staticmethod
	def save_config(data, config_path):
		with open(config_path, 'w') as f:
			json.dump(data, f, indent=4, sort_keys=True)

	def __getitem__(self, key):
		if key in self.data:
			return self.data[key]
		else:
			raise KeyError(f"{key} not found")

	def __setitem__(self, key, value):
		self.data[key] = value
