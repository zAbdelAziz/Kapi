

class Route:
	def __init__(self):
		# TODO [Include more than 1 dynamic child]
		# TODO [Type hints?]
		self.static_children = {}
		self.dynamic_child = None
		self.handler = None


class Router:
	def __init__(self, routes: list = None):
		self.root = Route()
		# TODO [Decide on a more robust datastructure for segment_cache]
		#  (capture the order to keep the most recent on top) (FILO) (Array? Stack?)
		self.segment_cache = {}
		if routes:
			self.construct(routes)

	def add_route(self, path: str, handler):
		node = self.root
		# TODO [Create a default separator] (in config?)
		segments = path.strip('/').split('/')

		for segment in segments:
			# TODO [Create a default parameter indicator] (in config?)
			if segment.startswith("<") and segment.endswith(">"):
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

	def resolve(self, path: str):
		# TODO [Add Multithreading]
		# TODO [Convert to Async method?]
		# TODO [Limit Segment Cache size (somehow)] (!Important - Memory Leak)
		# TODO [segment_cache Check static only?]
		if not isinstance(path, str):
			# TODO [Add Security Measures]
			raise AttributeError('path should be a string')
		if path in self.segment_cache:
			return self.segment_cache[path]

		node = self.root
		# TODO [Create a default separator] (in config?)
		segments = path.strip('/').split('/')

		variables = {}

		for segment in segments:
			# TODO [Decide which to check first] (logically) (performance)
			if segment in node.static_children:
				node = node.static_children[segment]
			elif node.dynamic_child:
				variables[node.dynamic_child.variable] = segment
				node = node.dynamic_child
			else:
				result = (None, None)
				self.segment_cache[path] = result
				return result

		result = (node.handler, variables)
		self.segment_cache[path] = result
		return result

	def construct(self, routes):
		# TODO Add Default Routes for (errors)
		if isinstance(routes, list) or isinstance(routes, set) or isinstance(routes, tuple):
			for route in routes:
				self.add_route(*route)
		else:
			raise AttributeError('routes should be a list')