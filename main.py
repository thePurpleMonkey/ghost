# coding=utf-8

import sys

infinity = float("inf")

# Check version of Python
if sys.version_info[0] < 3:
	print("This program designed to be run with Python 3. Please run again with the Python version 3 interpreter.")
	sys.exit()

class State:
	def __init__(self, turn):
		self.turn = turn

	"""Return whether this state is a terminal state or not"""
	def is_terminal(self):
		pass
	
	"""Return all valid successors of this state"""
	def successors(self):
		pass

"""Return the state after the computer has made its move"""
def computer_move(state):
	pass

"""Return the state after the player has made their move"""
def player_move(state):
	pass

if __name__ == "__main__":
	# Set up players to alternate
	players = (computer_move, player_move)

	while True:
		# Check for game end at begining of turn
		if state.is_terminal():
			break

		# Prompt player for move
		state = players[state.turn](state)