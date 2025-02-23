# coding=utf-8

import sys, mmap, re
# import enchant

infinity = float("inf")
# d = enchant.Dict("en_US")
word_play = input

popMax = []

# Check version of Python
if sys.version_info[0] < 3:
	print("This program designed to be run with Python 3. Please run again with the Python version 3 interpreter.")
	sys.exit()

mm = None

class State:
	def __init__(self, prev):
		self.prev = prev
		#self.node = node

	def __hash__(self):
		return hash(self.prev)

	def __eq__(self, other):
		return self.prev == other.prev

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "State(prev='{}')".format(self.prev)

	"""Return whether this state is a terminal state or not"""
	def is_terminal(self):
		"""
		This isn't working for me for some reason
		"""
		# if d.check(self.word):
		
		return bool(re.search("\r\n{}\r\n".format(self.prev).encode("utf-8"), mm))
		# match = re.search("\r\n{}\r\n".format(self.prev).encode("utf-8"), mm)
		# print(self, "is_terminal?", bool(match), match)
		# return bool(match)
		
	"""Return all valid successors of this state"""
	def successors(self):
		return list(set([State(self.prev + match.decode("utf-8")[len(self.prev)+2]) for match in re.findall("\r\n{}..*\r\n".format(self.prev).encode("utf-8"), mm)]))

"""Return the state after the computer has made its move"""
def computer_move(state):
	pass

"""return a letter to play"""
def min_max_search(string):
	# maxList = []
	# minList = []
	letterToPlay  = {}
	inLength = len(string)

	for item in popMax:
		if(inLength%2 == len(item)%2):
			# minList.append(item)
			if not item[inLength] in letterToPlay:
				letterToPlay[item[inLength]] = 1
			else:
				letterToPlay[item[inLength]] += 1
		else:
			# maxList.append(item)
			if not item[inLength] in letterToPlay:
				letterToPlay[item[inLength]] = -1
			else:
				letterToPlay[item[inLength]] -= 1

	for element, val in letterToPlay.items():
		print(element, val)
	v=list(letterToPlay.values())
	k=list(letterToPlay.keys())
	toPlay = k[v.index(max(v))]

	return toPlay

"""Return the state after the player has made their move"""
def player_move(state):
    pass

class Node:
	def __init__(self):
		self.next_node = {}	#Initialize an empty hash (python dictionary)

		self.word_marker = False 
		# There can be words, Hot and Hottest. When search is performed, usually state transition upto leaf node is peformed and characters are printed. 

		# Then in this case, only Hottest will be printed. Hot is intermediate state. Inorder to mark t as a state where word is to be print, a word_marker is used



	def add_item(self, string):
		''' Method to add a string the Trie data structure'''
		
		if len(string) == 0:
			self.word_marker = True 
			return 
		
		key = string[0] #Extract first character

		string = string[1:] #Create a string by removing first character


		# If the key character exists in the hash, call next pointing node's add_item() with remaining string as argument

		if key in self.next_node:
			self.next_node[key].add_item(string)
		# Else create an empty node. Insert the key character to hash and point it to newly created node. Call add_item() in new node with remaining string.

		else:
			node = Node()
			self.next_node[key] = node
			node.add_item(string)


	def dfs(self, sofar=None):
		'''Perform Depth First Search Traversal'''
		
		# When hash of the current node is empty, that means it is a leaf node. 

		# Hence print sofar (sofar is a string containing the path as character sequences through which state transition occured)

		if list(self.next_node.keys()) == []:
			popMax.append(sofar)
			# print("in dfs ...keys() == []:",sofar)
			return
			
		if self.word_marker == True:
			popMax.append(sofar)
			# print("in dfs word_marker == True:",sofar)

		# Recursively call dfs for all the nodes pointed by keys in the hash

		for key in list(self.next_node.keys()):
			self.next_node[key].dfs(sofar+key)

	def search(self, string, sofar=""):
		'''Perform auto completion search and print the autocomplete results'''
		# Make state transition based on the input characters. 

		# When the input characters becomes exhaused, perform dfs() so that the tree gets traversed upto leaves and print the state characters

		if len(string) > 0:
			key = string[0]
			string = string[1:]
			if key in self.next_node:
				sofar = sofar + key
				self.next_node[key].search(string,sofar)
				
			else:
				print("No match")
		else:
			if self.word_marker == True:
				print("in search:",sofar)

			for key in list(self.next_node.keys()):
				self.next_node[key].dfs(sofar+key)




def fileparse(filename):
	'''Parse the input dictionary file and build the trie data structure'''
	fd = open(filename)

	root = Node()	
	line = fd.readline().strip('\r\n') # Remove newline characters \r\n

	while line !='':
		root.add_item(line)
		line = fd.readline().strip('\r\n')

	return root

if __name__ == "__main__":
	# Set up players to alternate
	players = (computer_move, player_move)
	turn = 1
	if len(sys.argv) != 2:
		print("Usage: ", sys.argv[0], "dictionary_file.txt")
		sys.exit(2)
		"""
	file = open(sys.argv[1], 'rb')
	mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

	test = State("sample")
	print(test, test.is_terminal(), test.successors())
	test = State("kern")
	print(test, test.is_terminal(), test.successors())
	test = State("xkcd")
	print(test, test.is_terminal(), test.successors())
	test = State("")

	print()
	print(test)
	while not test.is_terminal():
		# print(test.successors())
		test = test.successors()[0]
		print(test, test.is_terminal())
	"""
	root  = fileparse(sys.argv[1])

	print("Input:", end=' ')
	input = input()
	root.search(input)
	letter = str(min_max_search(input))
	print("back in main and: " + letter)

	while True:
		# Check for game end at begining of turn
		if board.is_terminal(input, root):
			break

		# Prompt player for move
		state = players[state.turn](state)
