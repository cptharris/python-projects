import random

def computer_choice(board, piece):
	gameBoard = board.b
	moves = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
	if piece == "X":
		otherPiece = "O"
	elif piece == "O":
		otherPiece = "X"
	
	if board.valid(1, 1):
		return "1,1"
	
	#CHECK HORIZONTAL
	for r in range(3):
		if (gameBoard[r][0] != piece and gameBoard[r][1] == otherPiece and gameBoard[r][2] == otherPiece):
			# player wins with [{r},0]
			moves[r][0] = -1
		if (gameBoard[r][0] == otherPiece and gameBoard[r][1] != piece and gameBoard[r][2] == otherPiece):
			# player wins with [{r},1]
			moves[r][1] = -1
		if (gameBoard[r][0] == otherPiece and gameBoard[r][1] == otherPiece and gameBoard[r][2] != piece):
			# player wins with [{r},2]
			moves[r][2] = -1
	#CHECK VERTICAL
	for c in range(3):
		if (gameBoard[0][c] != piece and gameBoard[1][c] == otherPiece and gameBoard[2][c] == otherPiece):
			# player wins with [0,{c}]
			moves[0][c] = -1
		if (gameBoard[0][c] == otherPiece and gameBoard[1][c] != piece and gameBoard[2][c] == otherPiece):
			# player wins with [1,{c}]
			moves[1][c] = -1
		if (gameBoard[0][c] == otherPiece and gameBoard[1][c] == otherPiece and gameBoard[2][c] != piece):
			# player wins with [2,{c}]
			moves[2][c] = -1
	#CHECK MAIN DIAGONAL
	if (gameBoard[0][0] != piece and gameBoard[1][1] == otherPiece and gameBoard[2][2] == otherPiece):
		# player wins with [0,0]
		moves[0][0] = -1
	if (gameBoard[0][0] == otherPiece and gameBoard[1][1] != piece and gameBoard[2][2] == otherPiece):
		# player wins with [1,1]
		moves[1][1] = -1
	if (gameBoard[0][0] == otherPiece and gameBoard[1][1] == otherPiece and gameBoard[2][2] != piece):
		# player wins with [2,2]
		moves[2][2] = -1
	#CHECK OTHER DIAGONAL
	if (gameBoard[0][2] != piece and gameBoard[1][1] == otherPiece and gameBoard[2][0] == otherPiece):
		# player wins with [0,2]
		moves[0][2] = -1
	if (gameBoard[0][2] == otherPiece and gameBoard[1][1] != piece and gameBoard[2][0] == otherPiece):
		# player wins with [1,1]
		moves[1][1] = -1
	if (gameBoard[0][2] == otherPiece and gameBoard[1][1] == otherPiece and gameBoard[2][0] != piece):
		# player wins with [2,0]
		moves[2][0] = -1
	
	#CHECK HORIZONTAL
	for r in range(3):
		if (gameBoard[r][0] != otherPiece and gameBoard[r][1] == piece and gameBoard[r][2] == piece):
			# computer wins with [{r},0]
			moves[r][0] = 1
		if (gameBoard[r][0] == piece and gameBoard[r][1] != otherPiece and gameBoard[r][2] == piece):
			# computer wins with [{r},1]
			moves[r][1] = 1
		if (gameBoard[r][0] == piece and gameBoard[r][1] == piece and gameBoard[r][2] != piece):
			# computer wins with [{r},2]
			moves[r][2] = 1
	#CHECK VERTICAL
	for c in range(3):
		if (gameBoard[0][c] != otherPiece and gameBoard[1][c] == piece and gameBoard[2][c] == piece):
			# computer wins with [0,{c}]
			moves[0][c] = 1
		if (gameBoard[0][c] == piece and gameBoard[1][c] != otherPiece and gameBoard[2][c] == piece):
			# computer wins with [1,{c}]
			moves[1][c] = 1
		if (gameBoard[0][c] == piece and gameBoard[1][c] == piece and gameBoard[2][c] != otherPiece):
			# computer wins with [2,{c}]
			moves[2][c] = 1
	#CHECK MAIN DIAGONAL
	if (gameBoard[0][0] != otherPiece and gameBoard[1][1] == piece and gameBoard[2][2] == piece):
		# computer wins with [0,0]
		moves[0][0] = 1
	if (gameBoard[0][0] == piece and gameBoard[1][1] != otherPiece and gameBoard[2][2] == piece):
		# computer wins with [1,1]
		moves[1][1] = 1
	if (gameBoard[0][0] == piece and gameBoard[1][1] == piece and gameBoard[2][2] != otherPiece):
		# computer wins with [2,2]
		moves[2][2] = 1
	#CHECK OTHER DIAGONAL
	if (gameBoard[0][2] != otherPiece and gameBoard[1][1] == piece and gameBoard[2][0] == piece):
		# computer wins with [0,2]
		moves[0][2] = 1
	if (gameBoard[0][2] == piece and gameBoard[1][1] != otherPiece and gameBoard[2][0] == piece):
		# computer wins with [1,1]
		moves[1][1] = 1
	if (gameBoard[0][2] == piece and gameBoard[1][1] == piece and gameBoard[2][0] != otherPiece):
		# computer wins with [2,0]
		moves[2][0] = 1
	
	for r in range(3):
		for c in range(3):
			if (moves[r][c] == 1):
				if board.valid(r, c):
					return str(r) + "," + str(c)
	
	for r in range(3):
		for c in range(3):
			if (moves[r][c] == -1):
				if board.valid(r, c):
					return str(r) + "," + str(c)
	
	return str(random.randint(0, 2)) + "," + str(random.randint(0, 2))
