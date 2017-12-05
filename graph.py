import igraph, re

words = open("oxford.txt", 'rt').read()

class State:
	def __init__(self, prev, turn):
		self.prev = prev
		self.turn = turn

	def __hash__(self):
		return hash((self.prev, self.turn))

	def __eq__(self, other):
		return (self.prev == other.prev) and (self.turn == other.turn)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "State(prev='{}')".format(self.prev)

	"""Return whether this state is a terminal state (i.e. spells a word)"""
	def is_terminal(self):
		return bool(re.search("\n{}\n".format(self.prev), words))
		
	"""Return all valid successors of this state"""
	def successors(self):
		return list(set([State(self.prev + match[len(self.prev)+1], (self.turn+1)%2) for match in re.findall("\n{}..*\n".format(self.prev), words)]))

def recurse(state, graph):
	successors = state.successors()
	for successor in successors:
		graph.add_vertex(str(hash(successor)), label=successor.prev, color="white")
		graph.add_edge(str(hash(state)), str(hash(successor)), color="white")
		recurse(successor, graph)

if __name__ == "__main__":
	state = State("pres", 0)
	graph = igraph.Graph()
	graph.add_vertex(str(hash(state)), label="pres", color="white")
	recurse(state, graph)

	plt = igraph.Plot(bbox=(1500, 1500), background="black")
	plt.add(graph, layout=graph.layout("tree"), background="black", margin=50, vertex_size=75, bbox=(1500, 1500))
	plt.save("graph.png")