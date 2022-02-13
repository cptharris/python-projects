'''
Tic-Tac-Toe framework in Python
Relies on external computer decision module
Start a game with
	variable = ttt.tttGame(databaseConnection, databaseCursor)
	variable.play()

Pass the database connection and cursor, or comment out the sqlite storage section
'''

import numpy as np
import os
import re
import computer
import datetime
import sqlite3
import random

blankFill = "-"

class tttBoard:
	def __init__(self):
		# create the blank board
		self.b = np.empty(shape=(3,3), dtype='object')
		for r in range(3):
			for c in range(3):
				self.b[r][c] = blankFill

	def draw(self, stats):
		os.system("cls")
		
		boardList = self.boardConst(stats)
		
		print("\n\n")
		for i in boardList:
			print(i)
		print("\n\n")

	def boardConst(self, stats):
		spaces = "   "
		dashes = "-" + spaces.replace(" ", "--")
		
		# board list representing each line
		boardList = [
		"\t" + " " + spaces + "0" + spaces + ' ' + spaces + "1" + spaces + ' ' + spaces + "2" + spaces,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces,
		"\t" + "0" + spaces + self.b[0][0] + spaces + '|' + spaces + self.b[0][1] + spaces + '|' + spaces + self.b[0][2] + spaces,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces,
		"\t" + " " + dashes + "|" + dashes + "|" + dashes,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces,
		"\t" + "1" + spaces + self.b[1][0] + spaces + '|' + spaces + self.b[1][1] + spaces + '|' + spaces + self.b[1][2] + spaces,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces,
		"\t" + " " + dashes + "|" + dashes + "|" + dashes,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces,
		"\t" + "2" + spaces + self.b[2][0] + spaces + '|' + spaces + self.b[2][1] + spaces + '|' + spaces + self.b[2][2] + spaces,
		"\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces
		]
		
		# iterate through the board
		for i in range(len(boardList)):
			try:
				# playLists will max at 9 items
				playLists = str(stats["plays"][i])
			except Exception as e:
				playLists = ""
			boardList[i] += "\t" + playLists
		
		return boardList

	def update(self, cor, piece):
		cor = re.split(",", cor)
		try:
			row = int(cor[0])
			col = int(cor[1])
		except Exception as e:
			# invalid entry
			return False
		# check if valid
		if self.valid(row, col):
			self.b[row][col] = piece
			return True
		else:
			return False

	def valid(self, row, col):
		# check if within range and empty space
		if row not in range(3):
			return 0
		if col not in range(3):
			return 0
		return self.b[row][col] == blankFill
	
	def checkWin(self, piece):
		otherPiece = 'X' if piece == 'O' else 'O'
		#CHECK HORIZONTAL
		for r in range(3):
			if (self.b[r][0] == piece and self.b[r][1] == piece and self.b[r][2] == piece):
				return piece
		#CHECK VERTICAL
		for c in range(3):
			if (self.b[0][c] == piece and self.b[1][c] == piece and self.b[2][c] == piece):
				return piece
		#CHECK MAIN DIAGONAL
		if (self.b[0][0] == piece and self.b[1][1] == piece and self.b[2][2] == piece):
			return piece
		#CHECK OTHER DIAGONAL
		if (self.b[0][2] == piece and self.b[1][1] == piece and self.b[2][0] == piece):
			return piece
		
		#CHECK HORIZONTAL
		for r in range(3):
			if (self.b[r][0] == otherPiece and self.b[r][1] == otherPiece and self.b[r][2] == otherPiece):
				return otherPiece
		#CHECK VERTICAL
		for c in range(3):
			if (self.b[0][c] == otherPiece and self.b[1][c] == otherPiece and self.b[2][c] == otherPiece):
				return otherPiece
		#CHECK MAIN DIAGONAL
		if (self.b[0][0] == otherPiece and self.b[1][1] == otherPiece and self.b[2][2] == otherPiece):
			return otherPiece
		#CHECK OTHER DIAGONAL
		if (self.b[0][2] == otherPiece and self.b[1][1] == otherPiece and self.b[2][0] == otherPiece):
			return otherPiece
		
		# checks for open space
		for r in range(3):
			for c in range(3):
				if self.valid(r, c):
					return False
		return "tie"

class tttGame:
	def __init__(self, dbConnection, dbCursor, sessionName="", dialogs=1, auto=0):
		self.dialogs = dialogs
		self.dbConnection = dbConnection
		self.dbCursor = dbCursor
		self.sessionName = sessionName
		self.board = tttBoard()
		
		# start on a random turn
		self.turn = random.randint(0, 1)
		self.setPiece()
		self.gameover = False
		
		self.stats = {"turns":0,"plays":[]}
		
		self.numPlayers = self.setPlayers(auto)
	
	def setPlayers(self, auto):
		if auto:
			return 1
		if self.dialogs:
			numPlayers = -1
			while numPlayers == -1:
				try:
					numPlayers = int(input("\t> How many players?\n\t"))
				except Exception as e:
					numPlayers = -1
			return numPlayers
		else:
			return 0
	
	def setPiece(self):
		if self.turn == 0:
			self.piece = "X"
			self.player = "P1"
		elif self.turn == 1:
			self.piece = "O"
			self.player = "P2"
	
	def requestInput(self):
		if self.dialogs:
			print(f"\t{self.player} enter row,col: ")
		if self.numPlayers == 2:
			return str(input("\t"))
		elif self.numPlayers == 1:
			if self.turn == 0:
				return str(input("\t"))
			else:
				return computer.computer_choice(self.board, self.piece)
		elif self.numPlayers == 0:
			return computer.computer_choice(self.board, self.piece)
	
	def play(self):
		while not self.gameover:
			self.board.draw(self.stats)
			self.setPiece()
			
			isValid = 0
			while not isValid:
				selectedCor = self.requestInput()
				# split the coordinate into row,col
				selectedCor = re.sub("\s", "", selectedCor)
				selectedCor = re.sub("\.", ",", selectedCor).strip().strip(",").strip()
				isValid = self.board.update(selectedCor, self.piece)
				if not isValid:
					if self.dialogs:
						print("\tInvalid move, please try again.")
				else:
					self.stats["plays"].append([self.piece, selectedCor])
			
			self.turn += 1
			self.turn %= 2
			self.stats["turns"] += 1
			
			winStatus = self.board.checkWin(self.piece)
			
			if winStatus:
				self.gameover = True
				self.board.draw(self.stats)
			
			if self.dialogs:
				if winStatus == self.piece:
					print(f"\t{self.player} wins!")
				elif winStatus == ('X' if self.turn == 0 else 'O'):
					print(f"\t{'X' if self.turn == 0 else 'O'} wins!")
				elif winStatus == "tie":
					print("\t> A strange game. The only winning move is not to play.")
			
			if winStatus:
				if self.dialogs:
					print("\tEND OF GAME")
				
				self.submitSQL(winStatus)
				
				if self.dialogs:
					input("\tPress enter to restart.")
	
	def submitSQL(self, winStatus):
		# return
		
		if winStatus == "X":
			winStatusValue = 1
		elif winStatus == "O":
			winStatusValue = -1
		else:
			winStatusValue = 0
		
		exitData = {
			"time": str(datetime.datetime.now()),
			"sessionName": self.sessionName,
			"turns": self.stats["turns"],
			"numPlayers": self.numPlayers,
			"winStatus": winStatusValue,
			"plays": str(self.stats["plays"])
		}
		self.dbCursor.execute("""
		INSERT INTO games(time, sessionName, turns, numPlayers, plays, winStatus)
		VALUES (:time, :sessionName, :turns, :numPlayers, :plays, :winStatus)
		""", exitData)
		
		self.dbConnection.commit()
