

class Route:
	def __init__(self):
		self.static_children = {}
		self.dynamic_child = None
		self.handler = None


class Router:
	def __init__(self, routes):
		self.root = Route()
		self.segment_cache = {}
		if routes:
			self.construct(routes)

	def add_route(self, path, handler):
		node = self.root
		segments = path.strip('/').split('/')

		for segment in segments:
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

	def resolve(self, path):
		if path in self.segment_cache:
			return self.segment_cache[path]

		node = self.root
		segments = path.strip('/').split('/')

		variables = {}

		for segment in segments:
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
		for route in routes:
			self.add_route(*route)
