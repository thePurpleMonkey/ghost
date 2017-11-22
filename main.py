# coding=utf-8

import sys, mmap, re, random, urllib.request
words = None

infinity = float("inf")

# Check version of Python
if sys.version_info[0] < 3:
	print("This program designed to be run with Python 3. Please run again with the Python version 3 interpreter.")
	sys.exit()

class State:
	def __init__(self, prev, turn, challenge=False):
		self.prev = prev
		self.turn = turn
		self.challenge = challenge
		self.word = None

	def __hash__(self):
		return hash(self.prev)

	def __eq__(self, other):
		return self.prev == other.prev

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "State(prev='{}')".format(self.prev)

	"""Return whether this state is a terminal state (i.e. spells a word)"""
	def is_terminal(self):
		return bool(re.search("\n{}\n".format(self.prev), words))
		
	"""Return all valid successors of this state"""
	def successors(self):
		return list(set([State(self.prev + match[len(self.prev)+2], (self.turn+1)%2) for match in re.findall("\n{}..*\n".format(self.prev), words)]))

"""Return the state after the computer has made its move"""
def computer_move(state):
	#return State(state.prev, (state.turn+1)%2) # nop
	return min_max_search(state)

"""Perform Minimax search for optimal next move"""
def min_max_search(state):
	successors = []

	# Iterate over each successor of this state
	for successor in state.successors():
		result = min_search(successor, -infinity, infinity)

		successors.append((result, successor))

	if len(successors) > 0:
		# We found at least one valid successor
		return sorted(successors, key=lambda x: x[0])[0][1]
	else:
		# There are no valid successors. Player must not have a word
		state.challenge = True
		state.turn = (state.turn+1)%2	# Change turn to player
		return state

def max_search(state, alpha, beta):
	if state.is_terminal():
		return state.turn

	v = -infinity

	for successor in state.successors():
		result = min_search(successor, alpha, beta)

		v = max(v, result)

		if v >= beta:
			return v

		alpha = max(alpha, v)

	return v

def min_search(state, alpha, beta):
	if state.is_terminal():
		return state.turn

	v = infinity

	for successor in state.successors():
		result = max_search(successor, alpha, beta)

		v = min(v, result)
		if v <= alpha:
			return v

		beta = min(beta, v)

	return v

"""Return the state after the player has made their move"""
def player_move(state):
	print("Current letters:", state.prev)
	if not state.challenge:
		# Not being challenged, enter a letter
		new_letter = input("Please enter a letter to play: ")[0].lower()
		return State(state.prev + new_letter, (state.turn+1)%2)
	else:
		# We've been challenged. Must type in a valid word or we lose
		state.word = input("You've been challenged! Please type a word that begins with the current letters: ").strip().lower()
		return state

class Node:
	popMax = []	# Static class member

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
			self.popMax.append(sofar)
			# print("in dfs ...keys() == []:",sofar)
			return
			
		if self.word_marker == True:
			self.popMax.append(sofar)
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
	line = fd.readline().strip('\n') # Remove newline characters \n

	while line !='':
		root.add_item(line)
		line = fd.readline().strip('\n')

	return root

if __name__ == "__main__":
	# Set up players to alternate
	players = (computer_move, player_move)
	turn = random.randint(0, 1)	# Choose a random player to go first

	# try:
	# 	# Get online dictionary
	# 	words = urllib.request.urlopen("https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt").read().decode("utf-8")
	# 	# print(type(words))
	# 	# print("Newline style: ", ("Windows \\r\\n" if "\r\n" in words >= 0 else "Unix \\n"))
	# except Exception as e:
	# 	print("Error obtaining online dictionary: {}".format(e))
	# 	print("Falling back to local dictionary")

	if len(sys.argv) != 2:
		print("Usage: ", sys.argv[0], "dictionary_file.txt")
		sys.exit(2)

	words = open(sys.argv[1], 'rt').read()
		# print("Newline style: ", ("Windows \\r\\n" if words.find("\r\n") >= 0 else "Unix \\n"))

	state = State("", turn)

	while True:
		# Check for game end at begining of turn
		if state.is_terminal():
			print("Game over")
			if (state.turn):
				print("Your opponent spelled '{}'. You win!".format(state.prev))
			else:
				print("You spelled '{}'. You lose. :(".format(state.prev))

			break
		if state.word:
			is_word = bool(re.search("\n{}\n".format(state.word), words))
			if (is_word and state.turn == 1) or (not is_word and state.turn == 0):
				print("You win!")
			else:
				print("You lose.")

			break


		# Prompt player for move
		state = players[state.turn](state)
