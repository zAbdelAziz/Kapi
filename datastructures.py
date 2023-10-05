

class TNode:
	def __init__(self):
		self.children = {}
		self.data = {}

	def add(self, data):
		self.data = data


class Trie:
	def __init__(self):
		self.root = TNode()

	def _add(self, term, data):
		node = self.root
		for char in term:
			if char not in node.children:
				node.children[char] = TNode()
			node.children[char].add(data)
			node = node.children[char]

	def _search(self, term, node=None):
		if node is None:
			node = self.root
		for char in term.lower():
			if char not in node.children:
				return {}
			node = node.children[char]
			print(node)
		return node.data