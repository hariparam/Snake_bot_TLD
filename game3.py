#the UI was built of the code on top of the code from Mr. David Kosbie with minor modifications
#http://www.kosbie.net/cmu/fall-10/15-110/handouts/snake/snake.html
#Version1
#The code uses a basic BFS to find out if there's a direct path P1 to food from the head.
#If such path is present, the snake moves in the same calculated path.
#But the such path is a> always not optimal b> the code stops working if there is no direct path

import random
from Tkinter import *
import Queue

#stores the moves in order that needs to be executed
movesList = Queue.Queue()
# Parameters
delay = 25  # milliseconds; denotes the rate at which the time is refreshed.
length = 10 #denotes the number of rows in the grid
width = 20  #denotes the number of coloumns in the grid


#the method defines the keyboard options to play the game
def keyPressed(event):
    canvas = event.widget.canvas
    # first process keys that work even if the game is over
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        init(canvas)
    elif (event.char == "d"):
        canvas.data["inDebugMode"] = not canvas.data["inDebugMode"]
    # now process keys that only work if the game is not over
    if (canvas.data["isGameOver"] == False):
        if (event.keysym == "Up"):
            # moveSnake(canvas, -1, 0)
            movesList.put((-1, 0))
        elif (event.keysym == "Down"):
            # moveSnake(canvas, +1, 0)
            movesList.put((1, 0))
        elif (event.keysym == "Left"):
            # moveSnake(canvas, 0,-1)
            movesList.put((0, -1))
        elif (event.keysym == "Right"):
            # moveSnake(canvas, 0,+1)
            movesList.put((0, 1))
    redrawAll(canvas)

# move the snake one step forward in the given direction.
def moveSnake(canvas, drow, dcol):
    canvas.data["snakeDrow"] = drow  # store direction for next timer event
    canvas.data["snakeDcol"] = dcol
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = canvas.data["headRow"]
    headCol = canvas.data["headCol"]
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if ((newHeadRow < 0) or (newHeadRow >= rows) or
            (newHeadCol < 0) or (newHeadCol >= cols)):
        # snake ran off the board
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] > 0):
        # snake ran into itself!
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] < 0):
        # eating food!  Yum!
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
        canvas.data["headRow"] = newHeadRow
        canvas.data["headCol"] = newHeadCol
        placeFood(canvas)
    else:
        # normal move forward (not eating food)
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
        canvas.data["headRow"] = newHeadRow
        canvas.data["headCol"] = newHeadCol
        removeTail(canvas)

#removes the tail from the last scene as soon as the new scene is rendered
def removeTail(canvas):
    # find every snake cell and subtract 1 from it.  When we're done,
    # the old tail (which was 1) will become 0, so will not be part of the snake.
    # So the snake shrinks by 1 value, the tail.
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > 0):
                snakeBoard[row][col] -= 1


def gameOver(canvas):
    canvas.data["isGameOver"] = True

#everytime once in 'delay ms' the canvas is rerendered the next move is fetched from the queue and is executed.
def timerFired(canvas):
    drow = 0
    dcol = -1
    if (canvas.data["isGameOver"] == False):
        # only process timerFired if game is not over
        if (movesList.empty() == False):
            #make a move only if there is a move to be made
            (drow, dcol) = movesList.get()
        moveSnake(canvas, drow, dcol)
        redrawAll(canvas)
    # whether or not game is over, call next timerFired
    # (or we'll never call timerFired again!)
    canvas.after(delay, timerFired, canvas)  # pause, then call timerFired again

#on press of R the game begins a new
def redrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    if (canvas.data["isGameOver"] == True):
        cx = canvas.data["canvasWidth"] / 2
        cy = canvas.data["canvasHeight"] / 2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))


def drawSnakeBoard(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)


def drawSnakeCell(canvas, snakeBoard, row, col):
    margin = canvas.data["margin"]
    cellSize = canvas.data["cellSize"]
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (snakeBoard[row][col] > 0):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    elif (snakeBoard[row][col] < 0):
        # draw food
        canvas.create_oval(left, top, right, bottom, fill="green")
    # for debugging, draw the number in the cell
    if (canvas.data["inDebugMode"] == True):
        canvas.create_text(left + cellSize / 2, top + cellSize / 2,
                           text=str(snakeBoard[row][col]), font=("Helvatica", 30, "bold"))


def loadSnakeBoard(canvas):
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    snakeBoard = []
    for row in range(rows): snakeBoard += [[0] * cols]
    snakeBoard[rows / 2][cols / 2] = 1
    canvas.data["snakeBoard"] = snakeBoard
    findSnakeHead(canvas)
    placeFood(canvas)


def placeFood(canvas):
    # place food (-1) in a random location on the snakeBoard, but
    # keep picking random locations until we find one that is not
    # part of the snake!
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    while True:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if (snakeBoard[row][col] == 0):
            break
    snakeBoard[row][col] = -1
    #print snakeBoard
    movesList.queue.clear()
    #everytime the food is placed the route is computed
    get_moves(snakeBoard)


def findSnakeHead(canvas):
    # find where snakeBoard[row][col] is largest, and
    # store this location in headRow, headCol
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = 0
    headCol = 0
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                headRow = row
                headCol = col
    canvas.data["headRow"] = headRow
    canvas.data["headCol"] = headCol


def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))


def max_2d(myList):
    mx = max(myList[0])
    for i, x in enumerate(myList):
        if mx < max(myList[i]):
            mx = max(myList[i]);
    return mx

#finds the list of moves using a BFS and pushes it into the queue
def get_moves(board):
    (foodx, foody) = index_2d(board, -1)
    (headx, heady) = index_2d(board, max_2d(board))
    # Lets do a BFS
    scene = convert_to_scene(board)
    # for i in scene:
    #     print i
    # print scene[headx][heady]
    scene[headx][heady] = False
    # print scene[headx][heady]
    # for i in scene:
    #     print i
    moves_made = find_path((headx, heady), (foodx, foody), scene)
    #print (headx, heady), (foodx, foody),moves_made
    if moves_made!=None:
        for i in moves_made[1:]:
            #print i
            if i=='up':
                movesList.put((-1,0))
            if i=='down':
                movesList.put((1,0))
            if i=='right':
                movesList.put((0,1))
            if i=='left':
                movesList.put((0,-1))

# finds the shortest path from cell A to cell B in a grid the entire body of the snake is considered to be an obstacle
# and the code tries to estimate a direct path; if no such path exist return None
############################################################

def find_path(start, goal, scene):
    rows = len(scene)
    cols = len(scene[0])
    array = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if scene[i][j]:
                row.append(-1)
            else:
                row.append(0)
        array.append(row)
    if array[start[0]][start[1]] == -1 | array[goal[0]][goal[1]] == -1 | array[start[0]][start[1]] == array[goal[0]][
        goal[1]]:
        return None
    else:
        currentnode = start
        q = Queue.PriorityQueue()
        dist = getecdist(currentnode, goal)
        moves = ['up']
        q.put((dist, (currentnode, moves)))
        while currentnode != goal and (q.qsize() != 0):
            successor_nodes = []
            successor_moves = []
            moves_made = []
            node = ()
            x = q.get()
            (node, moves_made) = x[1]
            if node == goal:
                return moves_made
            successor_moves = get_successors(node, array)
            currentnode = node
            if len(successor_moves) > 0:
                for m in range(len(successor_moves)):
                    newmoves = moves_made[:]
                    if successor_moves[m] == 'up':
                        newnode = (currentnode[0] - 1, currentnode[1])
                        ecdist = getecdist(newnode, goal)
                        if array[newnode[0]][newnode[1]] > (ecdist + len(moves_made) + 1) or array[newnode[0]][
                            newnode[1]] == 0:
                            array[newnode[0]][newnode[1]] = ecdist + len(moves_made) + 1
                            newmoves.append('up')
                            q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                    if successor_moves[m] == 'down':
                        newnode = (currentnode[0] + 1, currentnode[1])
                        ecdist = getecdist(newnode, goal)
                        if array[newnode[0]][newnode[1]] > (ecdist + len(moves_made) + 1) or array[newnode[0]][
                            newnode[1]] == 0:
                            array[newnode[0]][newnode[1]] = ecdist + len(moves_made) + 1
                            newmoves.append('down')
                            q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                    if successor_moves[m] == 'left':
                        newnode = (currentnode[0], currentnode[1] - 1)
                        ecdist = getecdist(newnode, goal)
                        if array[newnode[0]][newnode[1]] > (ecdist + len(moves_made) + 1) or array[newnode[0]][
                            newnode[1]] == 0:
                            array[newnode[0]][newnode[1]] = ecdist + len(moves_made) + 1
                            newmoves.append('left')
                            q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                    if successor_moves[m] == 'right':
                        newnode = (currentnode[0], currentnode[1] + 1)
                        ecdist = getecdist(newnode, goal)
                        if array[newnode[0]][newnode[1]] > (ecdist + len(moves_made) + 1) or array[newnode[0]][
                            newnode[1]] == 0:
                            array[newnode[0]][newnode[1]] = ecdist + len(moves_made) + 1
                            newmoves.append('right')
                            q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                            # if successor_moves[m]=='upleft':
                            #     newnode=(currentnode[0]-1,currentnode[1]-1)
                            #     ecdist=getecdist(newnode,goal)
                            #     if array[newnode[0]][newnode[1]]>(ecdist+len(moves_made)+1) or array[newnode[0]][newnode[1]]==0:
                            #         array[newnode[0]][newnode[1]]=ecdist+len(moves_made)+1
                            #         newmoves.append(newnode)
                            #         q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                            # if successor_moves[m] == 'upright':
                            #     newnode = (currentnode[0]-1, currentnode[1] + 1)
                            #     ecdist = getecdist(newnode, goal)
                            #     if array[newnode[0]][newnode[1]] > (ecdist + len(moves_made) + 1) or array[newnode[0]][
                            #         newnode[1]] == 0:
                            #         array[newnode[0]][newnode[1]] = ecdist + len(moves_made) + 1
                            #         newmoves.append(newnode)
                            #         q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                            # if successor_moves[m]=='downright':
                            #     newnode=(currentnode[0]+1,currentnode[1]+1)
                            #     ecdist=getecdist(newnode,goal)
                            #     if array[newnode[0]][newnode[1]]>(ecdist+len(moves_made)+1) or array[newnode[0]][newnode[1]]==0:
                            #         array[newnode[0]][newnode[1]]=ecdist+len(moves_made)+1
                            #         newmoves.append(newnode)
                            #         q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
                            # if successor_moves[m]=='downleft':
                            #     newnode=(currentnode[0]+1,currentnode[1]-1)
                            #     ecdist=getecdist(newnode,goal)
                            #     if array[newnode[0]][newnode[1]]>(ecdist+len(moves_made)+1) or array[newnode[0]][newnode[1]]==0:
                            #         array[newnode[0]][newnode[1]]=ecdist+len(moves_made)+1
                            #         newmoves.append(newnode)
                            #         q.put(((ecdist + len(moves_made) + 1), (newnode, newmoves)))
    if len(moves_made) == 1 or q.qsize() == 0:
        return None
    return moves_made


def getecdist(a, b):
    dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return dist


def get_successors(currentnode, array):
    moves = []
    rows = len(array)
    cols = len(array[0])
    if (currentnode[1] - 1 >= 0):
        if array[currentnode[0]][currentnode[1] - 1] != -1:
            moves.append('left')
    if (currentnode[1] + 1) < cols:
        if array[currentnode[0]][currentnode[1] + 1] != -1:
            moves.append('right')
    if (currentnode[0] - 1) >= 0:
        if array[currentnode[0] - 1][currentnode[1]] != -1:
            moves.append('up')
    if (currentnode[0] + 1) < rows:
        if array[currentnode[0] + 1][currentnode[1]] != -1:
            moves.append('down')
    # if (currentnode[0] - 1) >=0 and (currentnode[1]-1>=0):
    #     if array[currentnode[0] - 1][currentnode[1]-1] != -1:
    #         moves.append('upleft')
    # if (currentnode[0] - 1) >=0 and (currentnode[1]+1)<cols:
    #     if array[currentnode[0] - 1][currentnode[1]+1] != -1:
    #         moves.append('upright')
    # if (currentnode[0]+1)<rows and (currentnode[1]-1>=0):
    #     if array[currentnode[0]+1][currentnode[1]-1] != -1:
    #         moves.append('downleft')
    # if (currentnode[0] + 1) < rows and (currentnode[1]+1)<cols:
    #     if array[currentnode[0]+1][currentnode[1]+1] != -1:
    #         moves.append('downright')
    return moves


############################################################

#converts the snakeBoard from 0's 1:n's and -1 to True and False, a True denotes an empty cell where the head can move
#if its a false it means the snake body is there and the snake head cannot move theree
#this method is not required if the above section is modified. I wanted to reuse my the code I already had for path
# finding.
def convert_to_scene(board):
    scene = [[]]
    for i in board:
        for j in i:
            if j > 0:
                scene[-1].append(True)
            else:
                scene[-1].append(False)
        scene.append([])
    return scene[:-1]


def printInstructions():
    print "Snake!"
    print "Use the arrow keys to move the snake."
    print "Eat food to grow."
    print "Stay on the board!"
    print "And don't crash into yourself!"
    print "Press 'd' for debug mode."
    print "Press 'r' to restart."


def init(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data["inDebugMode"] = False
    canvas.data["isGameOver"] = False
    #    canvas.data["snakeDrow"] = 0
    #    canvas.data["snakeDcol"] = -1 # start moving left
    redrawAll(canvas)


########### copy-paste below here ###########

# takes in the board size and creates the board and begins the game
def run(rows, cols):
    # create the root and the canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2 * margin + cols * cellSize
    canvasHeight = 2 * margin + rows * cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = {}
    canvas.data["margin"] = margin
    canvas.data["cellSize"] = cellSize
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["rows"] = rows
    canvas.data["cols"] = cols
    init(canvas)
    # set up events
    #    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)


run(length, width)
