'''
Creates a board as defined by a parsed array.
Accets an array with optional brackets, spaces, and quotation marks
Examples:
	["X", "X", "X", "X", "X", "X", "O", "O", "O"]
	[X, X, X, X, X, X, O, O, O]
	X, X, X, X, X, X, O, O, O
'''
import numpy as np
import ttt

blankFill = "-"

enteredBoard = input(f"Enter values\n\t> ").replace("[", "").replace("]", "").replace(" ", "").replace("\"", "").split(",")

board = ttt.tttBoard()

board.b = np.empty(shape=(3,3), dtype='object')
i = 0
for r in range(3):
	for c in range(3):
		board.b[r][c] = enteredBoard[i]
		i += 1

board.draw();

# ["X", "X", "X", "X", "X", "X", "O", "O", "O"]
