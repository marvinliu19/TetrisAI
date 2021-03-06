# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, copy
from pygame.locals import *

# WEIGHT VECTOR (only parameters that should change)
ALPHA = -.516
BETA = .76
GAMMA = -.356
DELTA = -.1844

FPS = 1000
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', '.', '.', 'O', '.'],
					['.', '.', '.', '.', '.']]]

Z_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', 'O', '.', '.', '.'],
					['.', '.', '.', '.', '.']]]

I_SHAPE_TEMPLATE = [[['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['O', 'O', 'O', 'O', '.'],
					['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.']]]

O_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', '.', '.', '.']]]

J_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', 'O', '.', '.', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', '.', '.', 'O', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', '.', '.', '.']]]

L_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', '.', '.', 'O', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', 'O', '.', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']]]

T_SHAPE_TEMPLATE = [[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', 'O', 'O', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', '.', '.', '.'],
					['.', 'O', 'O', 'O', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']],
					[['.', '.', '.', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', 'O', 'O', '.', '.'],
					['.', '.', 'O', '.', '.'],
					['.', '.', '.', '.', '.']]]

PIECES = {'S': S_SHAPE_TEMPLATE,
		  'Z': Z_SHAPE_TEMPLATE,
		  'J': J_SHAPE_TEMPLATE,
		  'L': L_SHAPE_TEMPLATE,
		  'I': I_SHAPE_TEMPLATE,
		  'O': O_SHAPE_TEMPLATE,
		  'T': T_SHAPE_TEMPLATE}


def main():
	global DISPLAYSURF, BASICFONT, BIGFONT
	pygame.init()

	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
	pygame.display.set_caption('Tetromino')

	showTextScreen('Tetromino')
	while True: # game loop
		runGame()
		showTextScreen('Game Over')


# Helper method for debugging
def printBoard(board):
	for i in range(BOARDHEIGHT):
		row = []
		for j in range (BOARDWIDTH):
			row.append(board[j][i])
		print('\t'.join(map(str,row)))

# Main game loop function
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
                return # can't fit a new piece on the board, so game over

        # Get all the moves available
        possibleBoards = getAllMoves(board, fallingPiece)

        # Find the best move by using evaluateBoard
        bestBoard = None
        maxVal = -float("inf")
        for newBoard in possibleBoards:
            val = evaluateBoard(newBoard, ALPHA, BETA, GAMMA, DELTA)
            if val > maxVal:
                maxVal =  val
                bestBoard = newBoard

        board = bestBoard
        score += removeCompleteLines(board)
        level, fallFreq = calculateLevelAndFallFreq(score)
        fallingPiece = None

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        time.sleep(1/FPS)


# Returns a score for the board based on the 4 heuristics
def evaluateBoard(board, a, b, c, d):
    totHeight, heights = getTotalHeight(board)
    completeLines = getCompleteLines(board)
    holes = getNumHoles(board)
    heightVar = getHeightVar(heights)

    return a * totHeight + b * completeLines + c * holes + d * heightVar


# Calculates the total height heuristic
def getTotalHeight(board):
    totalHeight = 0
    heights = []

    for i in range(BOARDWIDTH):
        colHeight = 0

        for j in range(BOARDHEIGHT):
            if board[i][j] != BLANK:
                colHeight = BOARDHEIGHT - j
                break

        heights.append(colHeight)
        totalHeight += colHeight

    return totalHeight, heights


# Calculates the total number of holes heuristic
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


# Calculates the height variance heuristic
def getHeightVar(heights):
    heightVar = 0

    for i in range(1, BOARDWIDTH):
        heightVar += abs(heights[i] - heights[i-1])

    return heightVar


#Calculates the number of complete lines heuristic
def getCompleteLines(board):
    numCompleteLines = 0

    for y in range(BOARDHEIGHT):
        if isCompleteLine(board, y):
            numCompleteLines += 1

    return numCompleteLines


def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()


def terminate():
	pygame.quit()
	sys.exit()


def checkForKeyPress():
	# Go through event queue looking for a KEYUP event.
	# Grab KEYDOWN events to remove them from the event queue.
	checkForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None


def showTextScreen(text):
	# This function displays large text in the
	# center of the screen until a key is pressed.
	# Draw the text drop shadow
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the text
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the additional "Press a key to play." text.
	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

	while checkForKeyPress() == None:
		pygame.display.update()

def checkForQuit():
	for event in pygame.event.get(QUIT): # get all the QUIT events
		terminate() # terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP): # get all the KEYUP events
		if event.key == K_ESCAPE:
			terminate() # terminate if the KEYUP event was for the Esc key
		pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
	# Based on the score, return the level the player is on and
	# how many seconds pass until a falling piece falls one space.
	level = int(score / 10) + 1
	fallFreq = 0.27 - (level * 0.02)
	return level, fallFreq


def getNewPiece():
	# return a random new piece in a random rotation and color
	shape = random.choice(list(PIECES.keys()))
	newPiece = {'shape': shape,
				'rotation': random.randint(0, len(PIECES[shape]) - 1),
				'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
				'y': -2, # start it above the board (i.e. less than 0)
				'color': random.randint(0, len(COLORS)-1)}
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
	t = time.time()
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				print 'a: ' + str(t-time.time())
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				print 'b: ' + str(t-time.time())
				return False
	print 'c: ' + str(t-time.time())
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
	for rot in range(numRotations):
		piece['rotation'] = (piece['rotation'] + 1) % len(PIECES[piece['shape']])

		xshift = 0
		while True:
			if not isInRange(piece, adjX = xshift) and xshift > 0:
				break
			currXShiftPiece = copy.deepcopy(piece)
			currXShiftPiece['x'] += xshift
			# t = time.time()
			# print 'Rot#' + str(rot) + ': ' + str(time.time()-t)
			if isValidPosition(board, currXShiftPiece):
				# print 'xshift#' + str(xshift) + ': ' + str(time.time()-t)
				dropPiece(board, currXShiftPiece)
				# print 'xshift#' + str(xshift) + ': ' + str(time.time()-t)
				currBoard = copy.deepcopy(board)
				# print 'xshift#' + str(xshift) + ': ' + str(time.time()-t)
				if addToBoard(currBoard, currXShiftPiece):
					# print 'xshift#' + str(xshift) + ': ' + str(time.time()-t)
					boardList.append(currBoard)
					# print 'xshift#' + str(xshift) + ': ' + str(time.time()-t)
			# left first
			# print 'Rot#' + str(rot) + ': ' + str(time.time()-t)
			if xshift <= 0:
				xshift -= 1
			else:
				xshift += 1

			if not isInRange(piece, adjX = xshift) and xshift <= 0:
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


def convertToPixelCoords(boxx, boxy):
	# Convert the given xy coordinates of the board to xy
	# coordinates of the location on the screen.
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	# draw a single box (each tetromino piece has four boxes)
	# at xy coordinates on the board. Or, if pixelx & pixely
	# are specified, draw to the pixel coordinates stored in
	# pixelx & pixely (this is used for the "Next" piece).
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
	# draw the border around the board
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

	# fill the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
	# draw the individual boxes on the board
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			drawBox(x, y, board[x][y])


def drawStatus(score, level):
	# draw the score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 150, 20)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

	# draw the level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOWWIDTH - 150, 50)
	DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
	shapeToDraw = PIECES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		# if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

	# draw each of the boxes that make up the piece
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[y][x] != BLANK:
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
	# draw the "next" text
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 120, 80)
	DISPLAYSURF.blit(nextSurf, nextRect)
	# draw the "next" piece
	drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
	main()
