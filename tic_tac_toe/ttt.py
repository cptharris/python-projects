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

blankFill = "-"

class tttBoard:
	def __init__(self):
		self.b = np.empty(shape=(3,3), dtype='object')
		for r in range(3):
			for c in range(3):
				self.b[r][c] = blankFill

	def draw(self):
		os.system("cls")
		spaces = "   "
		dashes = "-" + spaces.replace(" ", "--")
		print("\n\n")
		print("\t" + " " + spaces + "0" + spaces + ' ' + spaces + "1" + spaces + ' ' + spaces + "2" + spaces)
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\t" + "0" + spaces + self.b[0][0] + spaces + '|' + spaces + self.b[0][1] + spaces + '|' + spaces + self.b[0][2] + spaces)
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\t" + " " + dashes + "|" + dashes + "|" + dashes)
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\t" + "1" + spaces + self.b[1][0] + spaces + '|' + spaces + self.b[1][1] + spaces + '|' + spaces + self.b[1][2])
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\t" + " " + dashes + "|" + dashes + "|" + dashes)
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\t" + "2" + spaces + self.b[2][0] + spaces + '|' + spaces + self.b[2][1] + spaces + '|' + spaces + self.b[2][2])
		print("\t" + " " + spaces + " " + spaces + '|' + spaces + " " + spaces + '|' + spaces + " " + spaces)
		print("\n\n")

	def update(self, cor, piece):
		cor = re.sub("\s", "", cor)
		cor = re.split(",", cor)
		try:
			row = int(cor[0])
			col = int(cor[1])
		except Exception as e:
			return False
		if self.valid(row, col):
			self.b[row][col] = piece
			return True
		else:
			return False

	def valid(self, row, col):
		if row not in range(3):
			return 0
		if col not in range(3):
			return 0
		return self.b[row][col] == blankFill
	
	def checkWin(self, piece):
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
		
		for r in range(3):
			for c in range(3):
				if self.valid(r, c):
					return False
		return "tie"

class tttGame:
	def __init__(self, dbConnection, dbCursor, dialogs=1):
		self.dialogs = dialogs
		self.dbConnection = dbConnection
		self.dbCursor = dbCursor
		self.board = tttBoard()
		
		self.turn = 0
		self.player = "P0"
		self.piece = "X"
		self.gameover = False
		
		self.stats = {"turns":0,"plays":[]}
		
		self.numPlayers = self.setPlayers()
	
	def setPlayers(self):
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
			self.board.draw()
			self.setPiece()
			
			isValid = 0
			while not isValid:
				selectedCor = self.requestInput()
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
			
			self.board.draw()
			
			if winStatus == self.piece:
				self.gameover = True
				if self.dialogs:
					print(f"\t{self.player} wins!")
			elif winStatus == "tie":
				self.gameover = True
				if self.dialogs:
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
			"turns": self.stats["turns"],
			"numPlayers": self.numPlayers,
			"winStatus": winStatusValue,
			"plays": str(self.stats["plays"])
		}
		self.dbCursor.execute("""
		INSERT INTO games(time, turns, numPlayers, plays, winStatus)
		VALUES (:time, :turns, :numPlayers, :plays, :winStatus)
		""", exitData)
		
		self.dbConnection.commit()
