'''
Creates a board as defined by a parsed array. The array can be entered directly or found via a database ID
Examples:
	[['X', '1,1'], ['O', '2,2'], ['X', '0,1'], ['O', '2,1'], ['X', '2,0'], ['O', '0,2'], ['X', '1,2'], ['O', '1,0'], ['X', '0,0']]
'''
import numpy as np
import ast
import sqlite3
import sys
import ttt

blankFill = "-"

board = ttt.tttBoard()

stats = {"plays":[]}

method2 = str(input("Enter a reference ID () or enter data directly (1)?\n\t> "))

if method2 == "1":
	enteredBoard = ast.literal_eval(input(f"Enter a database list\n\t> "))
elif method2 == "":
	try:
		dbID = int(input("Enter a reference ID.\n\t> "))
	except Exception as e:
		sys.exit()
	
	dbcon = sqlite3.connect('games.db')
	dbcur = dbcon.cursor()
	dbcur.execute("""
	SELECT * FROM games WHERE id == :id
	""", {"id": dbID})
	
	result = dbcur.fetchone()
	
	try:
		str(result[0])
	except Exception as e:
		sys.exit()
	
	printData = [result[0], result[1], int(result[2]), int(result[3]), int(result[4])]
	enteredBoard = ast.literal_eval(result[5])
	
	dbcon.close()

for i in range(len(enteredBoard)):
	stats["plays"].append([enteredBoard[i][1], enteredBoard[i][0]])
	board.update(enteredBoard[i][1], enteredBoard[i][0])
	board.draw(stats)
	print(
	"\n\tGameID: " +
	str(printData[0]).rjust(5) +
	"\t" + "Time: " +
	str(printData[1]).rjust(27) + "\n" +
	"\t" + "Players:" +
	str(printData[3]).rjust(5) +
	"\t" + "Win Status: " +
	str(printData[4]).rjust(2) +
	"\t  " + "Turns: " +
	str(printData[2]).rjust(1)
	)
	input()

input("\tFinished\n")

'''
enteredBoard = input(f"Enter values\n\t> ").replace("[", "").replace("]", "").replace(" ", "").replace("\"", "").split(",")
board.b = np.empty(shape=(3,3), dtype='object')
i = 0
for r in range(3):
	for c in range(3):
		board.b[r][c] = enteredBoard[i]
		i += 1
input()

Examples:
	["X", "X", "X", "X", "X", "X", "O", "O", "O"]
	[X, X, X, X, X, X, O, O, O]
	X, X, X, X, X, X, O, O, O
'''
