# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, sys, copy

BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '..OO.',
					 '.OO..',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '...O.',
					 '.....']]

Z_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '..OO.',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '.O...',
					 '.....']]

I_SHAPE_TEMPLATE = [['..O..',
					 '..O..',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 'OOOO.',
					 '.....',
					 '.....']]

O_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '.OO..',
					 '.....']]

J_SHAPE_TEMPLATE = [['.....',
					 '.O...',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..OO.',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '...O.',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '.OO..',
					 '.....']]

L_SHAPE_TEMPLATE = [['.....',
					 '...O.',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '..OO.',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '.O...',
					 '.....'],
					['.....',
					 '.OO..',
					 '..O..',
					 '..O..',
					 '.....']]

T_SHAPE_TEMPLATE = [['.....',
					 '..O..',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '..O..',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '..O..',
					 '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
		  'Z': Z_SHAPE_TEMPLATE,
		  'J': J_SHAPE_TEMPLATE,
		  'L': L_SHAPE_TEMPLATE,
		  'I': I_SHAPE_TEMPLATE,
		  'O': O_SHAPE_TEMPLATE,
		  'T': T_SHAPE_TEMPLATE}


def main():
	while True: # game loop
		runGame()

def printBoard(board):
	for i in range(BOARDHEIGHT):
		row = []
		for j in range (BOARDWIDTH):
			row.append(board[j][i])
		print('\t'.join(map(str,row)))

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()

    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()

            if not isValidPosition(board, fallingPiece):
                print "Score %i" % (score)
                return # can't fit a new piece on the board, so game over

        possibleBoards = getAllMoves(board, fallingPiece)

        bestBoard = None
        maxVal = -float("inf")
        for newBoard in possibleBoards:
            val = evaluateBoard(newBoard, -1, 1, -0.5, -0.5)
            if val > maxVal:
                maxVal =  val
                bestBoard = newBoard

        board = bestBoard
        score += removeCompleteLines(board)
        level, fallFreq = calculateLevelAndFallFreq(score)
        fallingPiece = None

def evaluateBoard(board, a, b, c, d):
    aggHeight, heights = getAggregateHeight(board)
    completeLines = getCompleteLines(board)
    holes = getNumHoles(board)
    bumpiness = getBumpiness(heights)

    return a * aggHeight + b * completeLines + c * holes + d * bumpiness


def getAggregateHeight(board):
    aggregateHeight = 0
    heights = []

    for i in range(BOARDWIDTH):
        colHeight = 0

        for j in range(BOARDHEIGHT):
            if board[i][j] != BLANK:
                colHeight = BOARDHEIGHT - j
                break

        heights.append(colHeight)
        aggregateHeight += colHeight

    return aggregateHeight, heights

def getNumHoles(board):
    holes = 0

    for i in range(BOARDWIDTH):
        foundBlock = False
        for j in range(BOARDHEIGHT):
            if board[i][j] != BLANK:
                foundBlock = True
            elif foundBlock == True:
                holes += 1

    return holes

def getBumpiness(heights):
    bumpiness = 0

    for i in range(1, BOARDWIDTH):
        bumpiness += abs(heights[i] - heights[i-1])

    return bumpiness


def getCompleteLines(board):
    numCompleteLines = 0

    for y in range(BOARDHEIGHT):
        if isCompleteLine(board, y):
            numCompleteLines += 1

    return numCompleteLines


def calculateLevelAndFallFreq(score):
	# Based on the score, return the level the player is on and
	# how many seconds pass until a falling piece falls one space.
	level = int(score / 10) + 1
	fallFreq = 0.27 - (level * 0.02)
	return level, fallFreq


def getNewPiece():
	# return a random new piece in a random rotation
	shape = random.choice(list(PIECES.keys()))
	newPiece = {'shape': shape,
				'rotation': random.randint(0, len(PIECES[shape]) - 1),
				'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
				'y': -2, # start it above the board (i.e. less than 0)
				'color': random.randint(0, 3)}
	return newPiece


def addToBoard(board, piece):
	# fill in the board based on piece's location, shape, and rotation
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
				board[x + piece['x']][y + piece['y']] = piece['color']
				if x + piece['x'] < 0 or y + piece['y'] < 0:
					return False
	return True


def getBlankBoard():
	# create and return a new blank board data structure
	board = []
	for i in range(BOARDWIDTH):
		board.append([BLANK] * BOARDHEIGHT)
	return board


def isOnBoard(x, y):
	return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
	# Return True if the piece is within the board and not colliding
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				return False
	return True


def isInRange(piece, adjX=0, adjY=0):
	# Return True if the piece is within the board, disregards collisions
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
	return True


# this method isn't perfect, as it fails with overhangs. The learners should not create these situations though
def getAllMoves(board, piece):
	def dropPiece(board, piece):
		i = 1
		while isValidPosition(board, piece, adjY=i):
			i+=1
		piece['y'] += i-1

	boardList = []

	numRotations = len(PIECES[piece['shape']])
	currRotPiece = copy.copy(piece)

	for rot in range(numRotations):
		currRotPiece['rotation'] = (currRotPiece['rotation'] + 1) % len(PIECES[currRotPiece['shape']])

		xshift = 0
		while True:
			if not isInRange(currRotPiece, adjX = xshift) and xshift > 0:
				break
			currXShiftPiece = copy.deepcopy(currRotPiece)
			currXShiftPiece['x'] += xshift
			if isValidPosition(board, currXShiftPiece):
				dropPiece(board, currXShiftPiece)

				currBoard = copy.deepcopy(board)
				if addToBoard(currBoard, currXShiftPiece):
					boardList.append(currBoard)
			# left first
			if xshift <= 0:
				xshift -= 1
			else:
				xshift += 1

			if not isInRange(currRotPiece, adjX = xshift) and xshift <= 0:
				xshift = 1

	return boardList


def isCompleteLine(board, y):
	# Return True if the line filled with boxes with no gaps.
	for x in range(BOARDWIDTH):
		if board[x][y] == BLANK:
			return False
	return True


def removeCompleteLines(board):
	# Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
	numLinesRemoved = 0
	y = BOARDHEIGHT - 1 # start y at the bottom of the board
	while y >= 0:
		if isCompleteLine(board, y):
			# Remove the line and pull boxes down by one line.
			for pullDownY in range(y, 0, -1):
				for x in range(BOARDWIDTH):
					board[x][pullDownY] = board[x][pullDownY-1]
			# Set very top line to blank.
			for x in range(BOARDWIDTH):
				board[x][0] = BLANK
			numLinesRemoved += 1
			# Note on the next iteration of the loop, y is the same.
			# This is so that if the line that was pulled down is also
			# complete, it will be removed.
		else:
			y -= 1 # move on to check next row up
	return numLinesRemoved


if __name__ == '__main__':
	main()
