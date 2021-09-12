'''
Uses the ttt module to play a tic-tac-toe game, including a main menu
'''
# pyinstaller --onefile -i "NONE" tic_tac_toe.py
# https://perceptron.zacharyhine.com/tic-tac-toe/
# import time
# import datetime
# import numpy as np
# import re

import os
import sys
import sqlite3

import ttt

sys.setrecursionlimit(10000)

blankFill = "-"

def main_menu():
	os.system("cls")
	if dialogs:
		print("""
		
		\t ████████     ██      ██████
		\t    ██        ██     ██
		\t    ██        ██     ██
		\t    ██        ██     ██
		\t    ██        ██      ██████
		
		\t ████████   █████     ██████
		\t    ██     ██   ██   ██
		\t    ██     ███████   ██
		\t    ██     ██   ██   ██
		\t    ██     ██   ██    ██████
		
		\t ████████   ██████   ███████
		\t    ██     ██    ██  ██
		\t    ██     ██    ██  █████
		\t    ██     ██    ██  ██
		\t    ██      ██████   ███████
		
		
		
		""")
	
	if dialogs:
		print("\t> Would you like to play a game?\t\t\tEnter 2 for fast PvC")
		playGameNow = str(input("\t"))
	else:
		playGameNow = "y"
	
	if (playGameNow == "yes" or playGameNow == "1" or playGameNow == "y" or playGameNow == "2"):
		playGame = ttt.tttGame(dbcon, dbcur, sessionName, dialogs, 1 if playGameNow == "2" else 0)
		playGame.play()
	else:
		dbcon.close()
		sys.exit("Done playing.")

try:
	dialogs = int(input("Press enter to open.\nEnter a 0 to disable dialogs.\t"))
except Exception as e:
	dialogs = 1

try:
	sessionName = str(input("Enter a session name (optional)\n> "))
	if sessionName == "C.":
		sessionName = "Caleb"
except Exception as e:
	sessionName = ""

dbcon = sqlite3.connect('games.db')
dbcur = dbcon.cursor()

while True:
	main_menu()
