'''
Creates a board as defined by a parsed array. The array can be entered directly or found via a database ID
Examples:
	[['X', '1,1'], ['O', '2,2'], ['X', '0,1'], ['O', '2,1'], ['X', '2,0'], ['O', '0,2'], ['X', '1,2'], ['O', '1,0'], ['X', '0,0']]
'''
import numpy as np
import ast
import sqlite3
import sys
import os

import ttt

blankFill = "-"

def drawEnteredBoard():
	for i in range(len(enteredBoard)):
		stats["plays"].append([enteredBoard[i][1], enteredBoard[i][0]])
		board.update(enteredBoard[i][1], enteredBoard[i][0])
		board.draw(stats)
		sessionInfo()
		input()
def sessionInfo():
	print(
	"\n\tSession Name: " +
	str(printData[2]) +
	"\n\tGameID: " +
	str(printData[0]).rjust(5) +
	"\t" + "Time: " +
	str(printData[1]).rjust(27) + "\n" +
	"\t" + "Players:" +
	str(printData[4]).rjust(5) +
	"\t" + "Win Status: " +
	str(printData[5]).rjust(2) +
	"\t  " + "Turns: " +
	str(printData[3]).rjust(1)
	)

board = ttt.tttBoard()

stats = {"plays":[]}

method = str(input("Enter a reference ID () or enter data directly (1) or view a series of games (2)?\n\t> "))

if method == "1":
	enteredBoard = ast.literal_eval(input(f"Enter a database list\n\t> "))
	drawEnteredBoard()
elif method == "":
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
	
	dbcon.close()
	
	try:
		str(result[0])
	except Exception as e:
		sys.exit()
	
	# 0: id, 1: time, 2: sessionName, 3: turns, 4: numPlayers, 5: winStatus, 6: plays
	printData = [result[0], result[1], result[2], int(result[3]), int(result[4]), int(result[5])]
	enteredBoard = ast.literal_eval(result[6])
	
	
	drawEnteredBoard()
elif method == "2":
	query = "SELECT * FROM games " + input("Enter a valid SQL statement.\n\t> ")
	
	dbcon = sqlite3.connect('games.db')
	dbcur = dbcon.cursor()
	dbcur.execute(query)
	sessions = dbcur.fetchall()
	dbcon.close()
	
	try:
		str(sessions[0])
	except Exception as e:
		sys.exit()
	
	os.system("cls")
	print("\n\n")
	
	for x in range(len(sessions)):
		result = sessions[x]
		stats = {"plays":[]}
		
		# 0: id, 1: time, 2: sessionName, 3: turns, 4: numPlayers, 5: winStatus, 6: plays
		printData = [result[0], result[1], result[2], int(result[3]), int(result[4]), int(result[5])]
		enteredBoard = ast.literal_eval(result[6])
		
		for i in range(len(enteredBoard)):
			stats["plays"].append([enteredBoard[i][1], enteredBoard[i][0]])
			board.update(enteredBoard[i][1], enteredBoard[i][0])
		boardList = board.boardConst(stats)
		for line in boardList:
			print(line)
		sessionInfo()
		if x%10 == 0 and x != 0:
			input()

print("\n\n")
isFinished = ""
while isFinished != "exit":
	isFinished = input("\tDone\t")

print("\n\n\n")

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
