import warnings
from .default_routes import *


class Route:
	def __init__(self):
		self.static_children = {}
		self.dynamic_child = None
		self.variable = None
		self.handler = None
		self.method = None


class Router:
	def __init__(self, routes: list = None, default_attrs: dict = None):
		self.root = Route()

		# TODO [Decide on a more robust datastructure for segment_cache]
		#  (capture the order to keep the most recent on top) (FILO) (Array? Stack?)
		self.segment_cache = {}
		self.default_separator = '/' if not default_attrs else default_attrs['separator']
		self.default_param_indicators = ('<', '>') if not default_attrs else default_attrs['param_indicators']
		if routes:
			self.construct(routes)

	def add_route(self, path: str, handler, method: str = 'get'):
		node = self.root
		segments = path.strip(self.default_separator).split(self.default_separator)

		for segment in segments:
			if len(segment.strip(self.default_param_indicators[1]).split(self.default_param_indicators[1])) > 1:
				raise ValueError('Only 1 dynamic parameter per segment is permitted, please separate parameters by "/"')
			if ' ' in segment:
				warnings.warn('Adding " " in routes and urls are not the best practices, please use a better convention.')

			if segment.startswith(self.default_param_indicators[0]) and segment.endswith(self.default_param_indicators[1]):
				variable = segment[1:-1]
				if not node.dynamic_child:
					node.dynamic_child = Route()
				node = node.dynamic_child
				node.variable = variable
			else:
				if segment not in node.static_children:
					node.static_children[segment] = Route()
				node = node.static_children[segment]

		node.handler = handler
		node.method = method

	async def resolve(self, path: bytes):
		if not path:
			return None, None, None
		path = path.decode()
		# TODO [Convert to Async method?]
		# TODO [Limit Segment Cache size (somehow)] (!Important - Memory Leak)
		# TODO [segment_cache Check static only?]
		# TODO [Add Security Measures]
		# TODO [Add efficient error handling]
		# if not isinstance(path, str):
		# 	raise AttributeError('path should be a string')
		if path in self.segment_cache:
			return self.segment_cache[path]

		node = self.root
		segments = path.strip(self.default_separator).split(self.default_separator)

		variables = {}

		for segment in segments:
			if segment in node.static_children:
				node = node.static_children[segment]
			elif node.dynamic_child:
				variables[node.dynamic_child.variable] = segment
				node = node.dynamic_child
			else:
				result = (None, None, None)
				# result = ('get', route_404, {"url": path})
				self.segment_cache[path] = result
				return result

		result = (node.method, node.handler, variables)
		self.segment_cache[path] = result
		return result

	def construct(self, routes):
		if isinstance(routes, list) or isinstance(routes, set) or isinstance(routes, tuple):
			for route in routes:
				self.add_route(*route)
			# TODO [Add Default Routes]
			if b'/404/<url>' not in routes or b'/404' not in routes:
				self.add_route('/404/<url>', route_404, 'get')
				# TODO [Optimize Static / favicon]
			self.add_route('/static/<url>', route_static, 'get')
			self.add_route('favicon.ico', route_favicon, 'get')
		elif isinstance(routes, dict):
			raise NotImplementedError('Routes should be either a list, set or a tuple')
			# for r_name, r_handler, in routes.items():
			# 	self.add_route(r_name, r_handler)
		else:
			raise AttributeError('routes should be a list')