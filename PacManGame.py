from cmu_112_graphics import * 
import random
import MazeGeneration
import AStarPathFinding
import ScoreSaver

'''
Work Cited:
Images:
- Characters: https://images.app.goo.gl/vkdwwDGDWUiz3mXu5
- Heart: https://images.app.goo.gl/ULeuUAD4bkxkgFW49
- Wall: https://images.app.goo.gl/vqHufK6qrPDwhpF9A
- Cherry: https://www.pixilart.com/art/pac-man-cherry-79e94a34e56adb2
- Background Image: https://vignette2.wikia.nocookie.net/kamenrider/images/1/14/Pac-Man_Game_Screen.png/revision/latest?cb=20170223170411'

'''

def appStarted(app):
    ## TitleScreen: ##
    #General:
    app.title_PlayButtonWidth = 100
    #loading images
    app.game_TitleBackground = app.loadImage('https://vignette2.wikia.nocookie.net/kamenrider/images/1/14/Pac-Man_Game_Screen.png/revision/latest?cb=20170223170411')
    app.game_TitleBackground = app.scaleImage(app.game_TitleBackground,8/10)
    app.findNextMove = 0


    #Map Creation#
    app.mapCreationSelected = []
    app.mapCreationSelectedPowerUp = []
    app.selection = "wall"

    ## GameMode ##

    #General:
    app.score = 0
    app.timerDelay = 100
    app.lives = 3
    app.PacmanEatten = False
    app.currentMove = "Right"
    app.nextMove = 'Right'
    app.dotsLeft = 0
    app.powerup = False
    app.powerupCounter = 0
    app.topScores = []
    app.topScoresName = []

    #board
    app.boardSize = 20
    app.board = [['Path'] * app.boardSize for i in range(app.boardSize)]
    app.border = 10
    app.squareLength = 40
    # app.squareLength = (app.width - (app.border*2))/app.boardSize
    app.mode = "titleScreen"

    #Loading Images:
    #Wall:
    app.wallImage = app.loadImage("/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/PacmanWall.png")
    imageWidthWall, imageHeightWall = app.wallImage.size
    app.wallImage = app.wallImage.crop((0,0,imageWidthWall/3.5,imageHeightWall))
    app.wallImage = app.scaleImage(app.wallImage,0.4) #Make it scaleable

    #PowerUP (https://www.pixilart.com/art/pac-man-cherry-79e94a34e56adb2)
    app.cherry = app.loadImage("/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/79e94a34e56adb2.png")
    app.cherry = app.scaleImage(app.cherry,0.04)

    #Pacman:
    app.spriteSheet = app.loadImage("/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/PacMan Sprite Sheet Full.png")
    app.spriteSheet = app.scaleImage(app.spriteSheet,1) #Make it scaleable
    app.sprites = dict()

    #Pacman Dead:
    app.PacmanDead = []

    #Ghosts:
    app.ghost1Sprites = dict()
    app.ghost2Sprites = dict()
    imageWidth, imageHeight = app.spriteSheet.size
    app.spriteWidth, app.spriteHeight = imageWidth/ 23, imageHeight/23

    #Hearts (https://www.vippng.com/png/full/154-1549032_heart-pixelart-game-retro-red-minecraft-life-pixel.png)
    app.heart = app.loadImage('/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/heart.jpeg')
    app.heart = app.scaleImage(app.heart,0.1)

    #Help Screen:
    app.ghostsImages = app.loadImage("/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/PacMan Sprite Sheet Full.png")
    app.imageWidthGhostsImages, app.imageHeightGhostsImages = app.ghostsImages.size
    app.ghostsImages = app.ghostsImages.crop((0,0,app.imageWidthGhostsImages/4,app.imageHeightGhostsImages/19))
    app.ghostsImages = app.scaleImage(app.ghostsImages,0.8) #Make it scaleable

    #Fix:
    app.pacmanStatic = app.loadImage("/Users/bhavikthati/Google Drive/Carnegie Mellon University/Freshman (21-22)/15-112/Term Project/PacMan Sprite Sheet Full.png")
    app.imageWidthPacManStaticImage, app.imageHeightPacManStaticImage = app.pacmanStatic.size
    app.pacmanStatic = app.pacmanStatic.crop((18*app.imageWidthPacManStaticImage/23,1*app.imageHeightPacManStaticImage,
                                             19*app.imageWidthPacManStaticImage/23, 2*app.imageHeightPacManStaticImage))
    app.pacmanStatic = app.scaleImage(app.pacmanStatic,0.8)

    '''Adapted from 15112 PIL TA Lecture:'''
    #PacMan Sprite
    for direction in ["Up9", "Down3", "Left6", "Right0"]:
        index = int(direction[-1:])
        newDir = direction[:-1]
        LeftX = 19 * imageWidth/ 23
        RightX = 20.1 * imageWidth / 23
        tempSprites = []
        for i in range(index,index+3):
            topLeftY = i * (imageHeight/20.8)
            botRightY = (i+1) * (imageHeight/20.8)
            sprite = app.spriteSheet.crop((LeftX,topLeftY,RightX,botRightY))
            tempSprites.append(sprite)
        app.sprites[newDir] = tempSprites

    #Pacman Dead:
    LeftX = 8 * imageWidth/ 23
    RightX = 9.2 * imageWidth / 23
    for i in range(11):
        topLeftY = i * (imageHeight/20.8)
        botRightY = (i+1) * (imageHeight/20.8)
        sprite = app.spriteSheet.crop((LeftX,topLeftY,RightX,botRightY))
        app.PacmanDead.append(sprite)

    #Ghost 1 Sprite:
    for direction in ["Up6", "Down2", "Left4", "Right0"]:
        index = int(direction[-1:])
        newDir = direction[:-1]
        LeftX = 0 * imageWidth/ 23
        RightX = 1 * imageWidth / 23
        tempSprites = []
        for i in range(index,index+2):
            topLeftY = i * (imageHeight/20.8)
            botRightY = (i+1) * (imageHeight/20.5)
            sprite = app.spriteSheet.crop((LeftX,topLeftY,RightX,botRightY))
            tempSprites.append(sprite)
        app.ghost1Sprites[newDir] = tempSprites

    #Ghost 2 Sprite:
    for direction in ["Up6", "Down2", "Left4", "Right0"]:
        index = int(direction[-1:])
        newDir = direction[:-1]
        LeftX = 1 * imageWidth/ 23
        RightX = 2.2 * imageWidth / 23
        tempSprites = []
        for i in range(index,index+2):
            topLeftY = i * (imageHeight/20.8)
            botRightY = (i+1) * (imageHeight/20.8)
            sprite = app.spriteSheet.crop((LeftX,topLeftY,RightX,botRightY))
            tempSprites.append(sprite)
        app.ghost2Sprites[newDir] = tempSprites

    #Ghost 1 Sprite Powerup:
    app.ghost1SpritesP = []
    LeftXP = 0 * imageWidth/ 23
    RightXP = 1 * imageWidth / 23
    for i in range(12,14):
        topLeftY = i * (imageHeight/20.2)
        botRightY = (i+1) * (imageHeight/20.3) #Fix
        sprite = app.spriteSheet.crop((LeftXP,topLeftY,RightXP,botRightY))
        app.ghost1SpritesP.append(sprite)


    #Pacman related:
    app.direction = 'Right'
    app.spriteCounter = 0
    app.PacmanX = 60
    app.PacmanY = 30

    #Ghost 1 Related:
    app.Ghost1Direction = "Right"
    app.spriteCounterGhost1 = 0
    app.Ghost1X = (len(app.board)//2)* app.squareLength + app.border
    app.Ghost1Y = (len(app.board)//2)* app.squareLength - app.border
    app.Ghost1Path = []
    app.Ghost1dx = 0
    app.Ghost1dy = 0
    app.Ghost1NextX = app.Ghost1X
    app.Ghost1NextY = app.Ghost1Y
    app.spriteCounterGhost1P = 0
    app.Ghost1DirectionP = "Right"

    #Ghost 2 Related:
    app.Ghost2Direction = "Right"
    app.spriteCounterGhost2 = 0
    app.Ghost2X = (len(app.board)//2)* app.squareLength + app.border
    app.Ghost2Y = (len(app.board)//2)* app.squareLength + app.border - 40

#### TITLE SCREEN ####
def titleScreen_mousePressed(app,event):
    #If playButton Clicked:
    if (event.x > app.width // 2 - app.title_PlayButtonWidth and event.x < app.width // 2 + app.title_PlayButtonWidth and
        event.y > app.height // 2 - app.title_PlayButtonWidth + 300 and event.y < app.height // 2 + app.title_PlayButtonWidth + 300 ):
            app.mode = 'gameMode'
            app.board = MazeGeneration.generateMap2(app.boardSize)
    if (event.x > app.width // 2 - app.title_PlayButtonWidth and event.x < app.width // 2 + app.title_PlayButtonWidth and
        event.y > app.height // 2 - app.title_PlayButtonWidth + 150 and event.y < app.height // 2 + app.title_PlayButtonWidth + 150):
            app.mode = 'helpScreen'
    
    #mapCreation Mode Button Clicked:
    if (event.x > 150 - app.title_PlayButtonWidth and event.x < 150 + app.title_PlayButtonWidth and
        event.y > 100 - app.title_PlayButtonWidth//2 and event.y < 100 + app.title_PlayButtonWidth//2):
            app.mode = 'mapCreation'

def titleScreen_redrawAll(app,canvas):
    #Insert Background
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.game_TitleBackground))
    canvas.create_text(app.width//2, 200,
                       text = "112", font = 'Arial 60', fill = 'yellow')

    #Draw Play Button
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 300 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 300 + app.title_PlayButtonWidth//2,
                            outline = "white", width = 3)
    canvas.create_text(app.width//2, app.height//2 + 300,
                       text = "Start", font = 'Arial 40', fill = 'white')

    #Draw Help Button
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 150 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 150 + app.title_PlayButtonWidth//2,
                            outline = "white", width = 3)
    canvas.create_text(app.width//2, app.height//2 + 150,
                       text = "Help", font = 'Arial 40', fill = 'white')
    
    #Draw mapCreation Mode
    canvas.create_rectangle(150 - app.title_PlayButtonWidth, 100 - app.title_PlayButtonWidth//2,
                            150 + app.title_PlayButtonWidth,100 + app.title_PlayButtonWidth//2,
                            outline = "white", width = 3)
    canvas.create_text(150, 100,
                       text = "Map Creation Mode", font = 'Arial 20', fill = 'white')

#### Map Creation ####

def mapCreation_mousePressed(app,event):
    if (event.x > app.width - app.title_PlayButtonWidth - 200 and event.x < app.width - 200 + app.title_PlayButtonWidth and
        event.y > app.height - 200 and event.y < app.height - 100):
            app.mode = 'gameMode'
    
    #If wall piece selection:
    if (event.x > app.width - 200 - 50 and event.x < app.width - 200 + 50 and
        event.y > 300 - 50 and event.y < 300 + 50):
            app.selection = "wall"

    #If cherry piece selection:
    if (event.x > app.width - 200 - 50 and event.x < app.width - 200 + 50 and
        event.y > 400 - 50 and event.y < 400 + 50):
            app.selection = "cherry"
    
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            if (event.x > row*app.squareLength + app.border and event.x < (row+1) *app.squareLength + app.border and
                event.y > col*app.squareLength + app.border and event.y < (col+1) * app.squareLength + app.border):
                cord = (row,col)
                if app.selection == "wall":
                    if app.board[row][col] != "Path":
                        try:
                            app.mapCreationSelected.remove(cord)
                            app.board[row][col] = "Path"
                        except:
                            pass
                    else:
                        app.board[row][col] = "Wall"
                        app.mapCreationSelected.append(cord)
                    break
                else:
                    if app.board[row][col]  != "Path":
                        try:
                            app.mapCreationSelectedPowerUp.remove(cord)
                            app.board[row][col]  = "Path"
                        except:
                            pass
                    else:
                        app.board[row][col] = "Powerup"
                        app.mapCreationSelectedPowerUp.append(cord)
                    break                 

def mapCreation_redrawAll(app,canvas):
    #Background:
    canvas.create_rectangle(0,0,app.width,app.height, fill = "black")
    
    #Text:
    canvas.create_text(app.width - 200, 100, text = "Make your own map!", fill = "white", font = "Arial 30")

    #Draw Play Button
    canvas.create_rectangle(app.width - app.title_PlayButtonWidth - 200, app.height - 200,
                            app.width - 200 + app.title_PlayButtonWidth, app.height - 100,
                            outline = "white", width = 2)
    canvas.create_text(app.width - 200, app.height - 150,
                       text = "Play Game", font = 'Arial 20', fill = 'white')

    #Piece Selection:
    canvas.create_text(app.width - 200, 200, text = "Choose your piece:", fill = "yellow", font = "Arial 30")


    #Wall:
    canvas.create_image(app.width - 200, 300, image = getCachedPhotoImage(app.wallImage))
    
    #Cherry:
    canvas.create_image(app.width - 200, 400, image = getCachedPhotoImage(app.cherry))

    #Draw Board
    drawGrid(app,canvas)
    drawWalls(app,canvas)
    drawSelectionRectangle(app,canvas)
    
def drawSelectionRectangle(app,canvas):
    if app.selection == "wall":
        canvas.create_rectangle(app.width - 200 - 50,300 - 50,app.width - 200 + 50, 300 + 50, 
                                width = 2, outline = "white")
    else:
        canvas.create_rectangle(app.width - 200 - 50,400 - 50,app.width - 200 + 50, 400 + 50, 
                                width = 2, outline = "white")

def drawGrid(app,canvas):
    for row in range(app.boardSize):
            for col in range(app.boardSize):
                x0 = row*app.squareLength + app.border
                x1 = (row+1) *app.squareLength + app.border
                y0 = col*app.squareLength + app.border
                y1 = (col+1) * app.squareLength + app.border
                canvas.create_rectangle(x0,y0,x1,y1,outline = "white", width = 1)

def drawWalls(app,canvas):
    for cord in app.mapCreationSelected:
        row = cord[0]
        col = cord[1]
        x0 = row*app.squareLength + app.border + app.squareLength // 2
        y0 = col*app.squareLength + app.border + app.squareLength // 2
        canvas.create_image(x0,y0,image=ImageTk.PhotoImage(app.wallImage))
    for cord in app.mapCreationSelectedPowerUp:
        row = cord[0]
        col = cord[1]
        x0 = row*app.squareLength + app.border + app.squareLength // 2
        y0 = col*app.squareLength + app.border + app.squareLength // 2
        cherryImage = app.cherry
        cherryImage = app.scaleImage(cherryImage,0.6)
        canvas.create_image(x0,y0,image=ImageTk.PhotoImage(cherryImage))

#### GAME MODE ####
## Control ##
def getMap(app):
    copyBoard = copy.deepcopy(app.board)
    return copyBoard

def gameMode_timerFired(app):
    app.spriteCounter = (app.spriteCounter + 1) % 3
    app.spriteCounterGhost1 = (app.spriteCounterGhost1+1) %2
    app.spriteCounterGhost1P = (app.spriteCounterGhost1P+1) %2
    app.findNextMove += 1

    PacmanRow = int((app.PacmanX-app.border)//app.squareLength)
    PacmanCol = int((app.PacmanY-app.border)/app.squareLength)
    if app.board[PacmanRow][PacmanCol] == "Path":
        app.board[PacmanRow][PacmanCol] = ""
        app.score += app.squareLength
    if app.board[PacmanRow][PacmanCol] == "Powerup":
        app.powerup = True
        app.board[PacmanRow][PacmanCol] = ""
        app.score += app.squareLength

    if app.powerup == True:
        app.powerupCounter += 1
        if app.powerupCounter == 50:
            app.powerup = False
            app.powerupCounter = 0

    #Move Ghost 1:
    if app.powerup == True:
        moveGhost1PowerUp(app)
    else:
        moveGhost1(app)

    # Move Ghost 2 Randomly:
    # moveGhost2(app)

    #isTouchingPacMan
    if isTouchingPacMan(app):
        if app.powerup == True:
            app.Ghost1X = (len(app.board)//2)* app.squareLength + app.border
            app.Ghost1Y = (len(app.board)//2)* app.squareLength + app.border
            app.powerup = False
            app.score += 100
        else:
            if app.lives > 0:
                # app.PacmanEatten = True
                app.PacmanX,app.PacmanY = app.border+10,app.border+10
            else:
                app.mode = "loseScreen"

    #Move 
    if app.nextMove != app.currentMove:
        if app.nextMove == 'Up' and isLegalMove(app,0,-10):
            app.direction = 'Up'
            app.currentMove = app.nextMove
            movePlayer(app,0,-10)
        if app.nextMove == 'Down' and isLegalMove(app,0,10):
            app.direction = 'Down'
            app.currentMove = app.nextMove
            movePlayer(app,0,10)
        if app.nextMove == 'Left' and isLegalMove(app,-10,0):
            app.direction = 'Left'
            app.currentMove = app.nextMove
            movePlayer(app,-10,0)
        if app.nextMove == 'Right' and isLegalMove(app,10,0):
            app.direction = 'Right'
            app.currentMove = app.nextMove
            movePlayer(app,10,0)
    else:
        if app.currentMove == 'Up':
            app.direction = 'Up'
            movePlayer(app,0,-10)
        if app.currentMove == 'Down':
            app.direction = 'Down'
            movePlayer(app,0,10)
        if app.currentMove == 'Left':
            app.direction = 'Left'
            movePlayer(app,-10,0)
        if app.currentMove == 'Right':
            app.direction = 'Right'
            movePlayer(app,10,0) 

    if isGameOver(app):
        app.mode = "gameOver"

def gameMode_keyPressed(app,event):
    if event.key == "Up":
        app.nextMove = event.key
    if event.key == "Down":
        app.nextMove = event.key
    if event.key == "Left":
        app.nextMove = event.key
    if event.key == "Right":
        app.nextMove = event.key
    if event.key == "p":
        app.mode = "gameOver"

def isLegalMove(app,dx,dy):
    PacManX = app.PacmanX + dx
    PacManY = app.PacmanY + dy
    if (app.border > app.PacmanX or app.PacmanX >= (len(app.board)*app.squareLength)- app.border or
        app.border > app.PacmanY or app.PacmanY >= (len(app.board)*app.squareLength)-app.border):
        return False
    return True

def movePlayer(app,dx,dy):
    app.PacmanX += dx
    app.PacmanY += dy
    if (app.border > app.PacmanX or app.PacmanX >= (len(app.board)*app.squareLength)- app.border or
        app.border > app.PacmanY or app.PacmanY >= (len(app.board)*app.squareLength)-app.border):
        app.PacmanX -= dx
        app.PacmanY -= dy
    if isTouchingWall(app):
        app.PacmanX -= dx
        app.PacmanY -= dy

def isTouchingWall(app):
    PacmanRow = int((app.PacmanX-app.border+10)//app.squareLength)
    PacmanCol = int((app.PacmanY-app.border+10)//app.squareLength)
    PacmanRow1 = int((app.PacmanX-app.border-10)//app.squareLength)
    PacmanCol1 = int((app.PacmanY-app.border-10)//app.squareLength)
    if (PacmanRow < len(app.board) and PacmanRow > 0 and PacmanCol < len(app.board) and PacmanCol > 0):
        if app.board[PacmanRow][PacmanCol] == "Wall" or app.board[PacmanRow1][PacmanCol1] == "Wall":
            return True
    return False

def isGhost1TouchingWall(app):
    GhostX = int((app.Ghost1X+app.border)//app.squareLength)
    GhostY = int((app.Ghost1Y+app.border)/app.squareLength)
    if app.board[GhostX][GhostY] == "Wall":
        return True
    return False

def isGhost2TouchingWall(app):
    GhostX = int((app.Ghost2X+app.border)//app.squareLength)
    GhostY = int((app.Ghost2Y+app.border)/app.squareLength)
    if app.board[GhostX][GhostY] == "Wall":
        return True
    return False

def isTouchingPacMan(app):
    PacmanRow = int((app.PacmanX-app.border)//app.squareLength)
    PacmanCol = int((app.PacmanY-app.border)/app.squareLength)
    Ghost1Row = int((app.Ghost1X-app.border)//app.squareLength)
    Ghost1Col = int((app.Ghost1Y-app.border)/app.squareLength)
    
    if PacmanRow == Ghost1Row and PacmanCol == Ghost1Col:
        if app.powerup == False:
            app.lives -= 1
        return True
    elif app.PacmanX == app.Ghost2X and app.PacmanY == app.Ghost2Y:
        app.lives -= 1
        return True  
    return False

def isGameOver(app):
    app.dotsLeft = 0
    for row in range(len(app.board[0])):
        for col in range(len(app.board)):
            if (app.board[col][row] == "Path") or (app.board[col][row] == "Open"):
                return False
    return True

def restartGame(app):
    app.board = MazeGeneration.generateMap2(app.boardSize)
    app.score = 0
    app.lives = 3
    app.PacmanEatten = False
    app.currentMove = "Right"
    app.nextMove = 'Right'
    app.PacmanX = 30
    app.PacmanY = 30
    app.Ghost1X = (len(app.board)//2)* app.squareLength + app.border
    app.Ghost1Y = (len(app.board)//2)* app.squareLength - app.border

def ghost1UpdatePath(app):
    Ghost1Row = int((app.Ghost1X-app.border)//app.squareLength)
    Ghost1Col = int((app.Ghost1Y-app.border)/app.squareLength)
    ghostStart = (Ghost1Row,Ghost1Col)
    PacmanRow = int((app.PacmanX-app.border)//app.squareLength)
    PacmanCol = int((app.PacmanY-app.border)/app.squareLength)
    PacmanEnd = (PacmanRow,PacmanCol)
    app.Ghost1Path = AStarPathFinding.astar(app.board, ghostStart, PacmanEnd)

def moveGhost1(app):
    #Every 5 seconds find path to Pacman:
    # if app.findNextMove % 5 == 0:
    ghost1UpdatePath(app)
    
    if app.Ghost1Path != None and len(app.Ghost1Path) >= 2:
        currentRow, currentCol = app.Ghost1Path[0]
        nextRow, nextCol = app.Ghost1Path[1]
        if nextRow == currentRow and nextCol == currentCol:
            app.Ghost1Path.pop(0)
        app.Ghost1dx = nextRow - currentRow
        app.Ghost1dy = nextCol - currentCol
        # print(f'Next Moves: {app.Ghost1Path}')
        # print(f'Pacman Cell: {app.Ghost1Path[-1]}')
        # # print(f'next Cell: {cord}')
        # print(f'next Cell Cord: {app.Ghost1NextX}, {app.Ghost1NextY}')
        # print(f'Ghost1 Cord: {app.Ghost1X},{app.Ghost1Y}')
        # print(f'dx: {app.Ghost1dx}, dy: {app.Ghost1dy}')
    else:
        app.Ghost1dx = app.Ghost1dy = 0

    app.Ghost1DirectionP = app.Ghost1Direction
    if app.Ghost1dx > 0:
        app.Ghost1Direction = "Right"
        app.Ghost1X += 10
    elif app.Ghost1dx < 0: 
        app.Ghost1Direction = "Left"
        app.Ghost1X -= 10
    else:
        app.Ghost1X += 0

    if app.Ghost1dy > 0: 
        app.Ghost1Direction = "Down"
        app.Ghost1Y += 10
    elif app.Ghost1dy < 0: 
        app.Ghost1Direction = "Up"
        app.Ghost1Y -= 10
    else:
        app.Ghost1Y += 0

    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Up":
        app.Ghost1Y -= 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Down":
        app.Ghost1Y += 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Right":
        app.Ghost1X += 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Left":
        app.Ghost1X -= 10

def ghost1UpdatePathPowerUp(app):
    Ghost1Row = int((app.Ghost1X-app.border)//app.squareLength)
    Ghost1Col = int((app.Ghost1Y-app.border)/app.squareLength)
    ghostStart = (Ghost1Row,Ghost1Col)
    PacmanRow = ((app.PacmanX-app.border)//app.squareLength)
    PacmanCol = ((app.PacmanY-app.border)/app.squareLength)
    endX = 0
    endY = 0
    if PacmanRow < len(app.board)//2:
        endX = len(app.board)-1
    else:
        endX = 0
    if PacmanCol < len(app.board)//2:
        endY = len(app.board)-1
    else:
        endY = 0

    while app.board[endX][endY] == "Wall":
        endX -= 1
        endY -= 1
    PacmanEnd = (endX,endY)
    app.Ghost1Path = AStarPathFinding.astar(app.board, ghostStart, PacmanEnd)

def moveGhost1PowerUp(app):
    #Every 5 seconds find path to Pacman:
    # if app.findNextMove % 5 == 0:
    ghost1UpdatePathPowerUp(app)

    
    if app.Ghost1Path != None and len(app.Ghost1Path) >= 2:
        currentRow, currentCol = app.Ghost1Path[0]
        nextRow, nextCol = app.Ghost1Path[1]
        if nextRow == currentRow and nextCol == currentCol:
            app.Ghost1Path.pop(0)
        app.Ghost1dx = nextRow - currentRow
        app.Ghost1dy = nextCol - currentCol
    else:
        app.Ghost1dx = app.Ghost1dy = 0
    
    app.Ghost1DirectionP = app.Ghost1Direction
    if app.Ghost1dx > 0:
        app.Ghost1Direction = "Right"
        app.Ghost1X += 10
    elif app.Ghost1dx < 0: 
        app.Ghost1Direction = "Left"
        app.Ghost1X -= 10
    else:
        app.Ghost1X += 0

    if app.Ghost1dy > 0: 
        app.Ghost1Direction = "Down"
        app.Ghost1Y += 10
    elif app.Ghost1dy < 0: 
        app.Ghost1Direction = "Up"
        app.Ghost1Y -= 10
    else:
        app.Ghost1Y += 0

    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Up":
        app.Ghost1Y -= 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Down":
        app.Ghost1Y += 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Right":
        app.Ghost1X += 10
    if app.Ghost1DirectionP != app.Ghost1Direction and app.Ghost1DirectionP == "Left":
        app.Ghost1X -= 10


def moveGhost2(app):
    randomMove2 = random.randint(0,4)
    if randomMove2 == 0:
        app.Ghost2Direction = "Right"
        app.Ghost2X += 10
        if isGhost2TouchingWall(app):
                app.Ghost2X -= 10
    elif randomMove2 == 1:
        app.Ghost2Direction = "Left"
        app.Ghost2X -= 10
        if isGhost2TouchingWall(app):
            app.Ghost2X += 10
    elif randomMove2 == 2:
        app.Ghost2Direction = "Down"
        app.Ghost2Y += 10
        if isGhost2TouchingWall(app):
            app.Ghost2Y -= 10
    elif randomMove2 == 3:
        app.Ghost2Direction = "Up"
        app.Ghost2Y -= 10
        if isGhost2TouchingWall(app) == False:
            app.Ghost2Y += 10

## Canvas ##
def drawPacmanDeadAnimation(app,canvas):
    for image in app.PacmanDead:
        canvas.create_image(app.PacmanX, app.PacmanY, image = getCachedPhotoImage(image))

def drawMap(app,canvas):
    for row in range(len(app.board[0])):
        for col in range(len(app.board)):
            if (app.board[col][row] == "Path") or (app.board[col][row] == "Open") :
                #Draw yellow dot
                drawDot(app,canvas,col,row)

            #Draw Walls
            if (app.board[col][row] == "Wall"):
                drawWall(app,canvas,col,row)
            
            #Draw PowerUp
            if (app.board[col][row] == "Powerup"):
                drawPowerUP(app,canvas,col,row)

def drawPowerUP(app,canvas,col,row):
    canvas.create_image(col * app.squareLength + app.border + app.squareLength // 2,
                        row * app.squareLength + app.border + app.squareLength //2,
                        image=ImageTk.PhotoImage(app.cherry))

def drawWall(app,canvas,col,row):
    canvas.create_image(col * app.squareLength + app.border + app.squareLength // 2,
                        row * app.squareLength + app.border + app.squareLength //2,
                        image=ImageTk.PhotoImage(app.wallImage))

def drawDot(app,canvas,col,row):
    radius = app.squareLength / 5
    canvas.create_oval(col * app.squareLength + app.border + app.squareLength // 2 - radius,
                        row * app.squareLength + app.border + app.squareLength //2 - radius,
                        col * app.squareLength + app.border + app.squareLength // 2 + radius,
                        row * app.squareLength + app.border + app.squareLength //2 + radius,
                        fill = "yellow2", outline = "white")        

def getCachedPhotoImage(image):
    if('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

def gameMode_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = "black")
    canvas.create_line((len(app.board)*app.squareLength) + 30,0,(len(app.board)*app.squareLength) + 30,app.height,
                       fill = "white", width = 3)
    drawMap(app,canvas)
    # canvas.create_text(app.width - 100, 100, text = f'{app.PacmanX}, {app.PacmanY}')

    #Draw Pacman:
    # if app.PacmanEatten == True:
    #     drawPacmanDeadAnimation(app,canvas)
    # else:
    spriteImage = app.sprites[app.direction][app.spriteCounter]
    print()
    print(f'PacMan Cord: {app.PacmanX}, {app.PacmanY}')
    canvas.create_image(app.PacmanX, app.PacmanY, image = getCachedPhotoImage(spriteImage))

    #Draw Ghost1:
    if app.powerup == False:
        ghost1Image = app.ghost1Sprites[app.Ghost1Direction][app.spriteCounterGhost1]
        canvas.create_image(app.Ghost1X, app.Ghost1Y, image = getCachedPhotoImage(ghost1Image))
    else:
        
        ghost1ImageP = app.ghost1SpritesP[app.spriteCounterGhost1P]
        canvas.create_image(app.Ghost1X, app.Ghost1Y, image = getCachedPhotoImage(ghost1ImageP))


    #Draw Ghost2:
    # ghost1Image = app.ghost2Sprites[app.Ghost2Direction][app.spriteCounterGhost2]
    # canvas.create_image(app.Ghost2X, app.Ghost2Y, image = getCachedPhotoImage(ghost1Image))

    #Draw Info Table:
    #Score
    canvas.create_rectangle(app.width-300, app.border, app.width-10, app.height-app.border, fill = "floral white")
    canvas.create_text(app.width - 150, 100, text = "SCORE:", font = "Arial 28")
    canvas.create_text(app.width - 150, 150, text = f'{app.score}', font = "Arial 28")
    
    #Lives:
    for lives in range(app.lives):
        canvas.create_image(app.width-200 + (lives*50), app.height - 100, image = getCachedPhotoImage(app.heart))

    # #Dots Remaining:
    # canvas.create_text(app.width - 150, 200, text = "Dots Remaining:", font = "Arial 28")
    # canvas.create_text(app.width - 150, 250, text = f'{app.dotsLeft}', font = "Arial 28")

#Help Screen:
def helpScreen_mousePressed(app,event):
    if (event.x > 75 and event.x < 75 + app.title_PlayButtonWidth and
        event.y > app.height - 100 and event.y < app.height - 50):
            app.mode = 'titleScreen'

def helpScreen_redrawAll(app,canvas):
    #Background:
    canvas.create_rectangle(0,0,app.width,app.height, fill = "black")
    #Help Title:
    canvas.create_rectangle(app.width//2 - app.title_PlayButtonWidth, 50,
                            app.width//2 + app.title_PlayButtonWidth, 100,
                            outline = "white", width = 3)
    canvas.create_text(app.width//2, 75,
                        text = 'HELP SCREEN', fill = 'white', font = 'Arial 24')
                                                    
    #Goal:
    canvas.create_text(app.width//2, app.border + 200,
                       text = '''Goal: The goal of the game is to move around the board and collect all the yellow dots on the map. 
                                But be careful, the ghosts will be chasing you! Don't get caught!''', font = 'Arial 24', fill = 'white')
    
    #Ghost:
    canvas.create_image(170, 500, image = getCachedPhotoImage(app.ghostsImages))
    canvas.create_text(app.border + 600, 500,
                       text = ''' --> These are the ghosts. Avoid them or lose a life :(''', font = 'Arial 24', fill = 'white') 
    
    #Pacman:
    spriteImage = app.sprites["Right"][1]
    canvas.create_image(170, 400, image = getCachedPhotoImage(spriteImage))
    # canvas.create_image(170, 400, image = getCachedPhotoImage(app.pacmanStatic))
    canvas.create_text(600, 400,
                       text = ''' --> This is you (Pacman). Move around the map using the arrow keys''', font = 'Arial 24', fill = 'white') 

    #Dot:
    radius = app.squareLength / 2
    canvas.create_oval(100 - radius,
                       600 - radius,
                       100 + radius,
                       600 + radius,
                        fill = "yellow2", outline = "white")     
    canvas.create_text(450 + radius + 100, 600,
                       text = ''' --> These are the dots. Make sure you collect these! They will increase your score.''', font = 'Arial 24', fill = 'white')  

    #Back Button:
    canvas.create_rectangle(75, app.height - 100,
                            75 + app.title_PlayButtonWidth, app.height - 50,
                            outline = "white", width = 3)
    canvas.create_text(125, app.height - 75,
                        text = 'Back', fill = 'white', font = 'Arial 24')
#Game Over:
def gameOver_mousePressed(app,event):
    if ((event.x > app.width//2 - app.title_PlayButtonWidth and event.x < app.width//2 + app.title_PlayButtonWidth) and
        (event.y > app.height//2 + 200 - app.title_PlayButtonWidth//2 and event.y < app.height//2 + 200 + app.title_PlayButtonWidth//2)):
            app.mode = 'titleScreen'
            restartGame(app)
    
    #Save Score:
    if ((event.x > app.width//2 - app.title_PlayButtonWidth and event.x < app.width//2 + app.title_PlayButtonWidth) and
    (event.y > app.height//2 + 300 - app.title_PlayButtonWidth//2 and event.y < app.height//2 + 300 + app.title_PlayButtonWidth//2)):
        #Adapated from 15-112 Function (https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#ioMethods)
        name = app.getUserInput('What is your name?')
        if (name == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You entered: ' + name)
            print('Your Score is: ' + str(app.score))
        ScoreSaver.saveScore(app.score,name)
    
    #Get Leaderboard:
    if ((event.x > app.width//2 - 575 and event.x < app.width//2 - 450) and
        (event.y > app.height//2 - 375 and event.y < app.height//2 - 325)):
        app.mode = 'topScores'
        scores = ScoreSaver.getScores()
        app.topScores = scores[0]
        app.topScoresName = scores[1]

def gameOver_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = "black")

    #You Win:
    canvas.create_text(app.width//2, app.height//2-200,
                       text = "YOU WIN!", font = 'Arial 60', fill = 'yellow')
    canvas.create_text(app.width//2, app.height//2,
                       text = f'Your Score: {app.score}', font = 'Arial 40', fill = 'white')

    #Play Again Button                        
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 200 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 200 + app.title_PlayButtonWidth//2,
                            outline = "white")
    canvas.create_text(app.width//2, app.height//2 + 200,
                       text = "Play Again", font = 'Arial 36', fill = 'white')

    #Save Score Button                        
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 300 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 300 + app.title_PlayButtonWidth//2,
                            outline = "white")
    canvas.create_text(app.width//2, app.height//2 + 300,
                       text = "Save Score", font = 'Arial 36', fill = 'white')
    
    #Leaderboard:                       
    canvas.create_rectangle(app.width//2 - 575, app.height//2 - 375,
                            app.width//2 - 450, app.height//2 - 325,
                            outline = "white")
    canvas.create_text(app.width//2 - 510, app.height//2 - 350,
                    text = "Top Scores", font = 'Arial 18', fill = 'white')
#loseScreen:
def loseScreen_mousePressed(app,event):
    if ((event.x > app.width//2 - app.title_PlayButtonWidth and event.x < app.width//2 + app.title_PlayButtonWidth) and
        (event.y > app.height//2 + 200 - app.title_PlayButtonWidth//2 and event.y < app.height//2 + 200 + app.title_PlayButtonWidth//2)):
            app.mode = 'titleScreen'
            restartGame(app)

    if ((event.x > app.width//2 - app.title_PlayButtonWidth and event.x < app.width//2 + app.title_PlayButtonWidth) and
    (event.y > app.height//2 + 300 - app.title_PlayButtonWidth//2 and event.y < app.height//2 + 300 + app.title_PlayButtonWidth//2)):
        name = app.getUserInput('What is your name?')
        if (name == None):
            app.message = 'You canceled!'
        else:
            app.showMessage('You entered: ' + name + '\nYour Score is: ' + str(app.score))
            app.message = f'Hi, {name}!'
        ScoreSaver.saveScore(app.score,name)

    if ((event.x > app.width//2 - 575 and event.x < app.width//2 - 450) and
        (event.y > app.height//2 - 375 and event.y < app.height//2 - 325)):
        app.mode = 'topScores'
        scores = ScoreSaver.getScores()
        app.topScores = scores[0]
        app.topScoresName = scores[1]

def loseScreen_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = "black")

    #You Win:
    canvas.create_text(app.width//2, app.height//2-200,
                       text = "You Lost", font = 'Arial 60', fill = 'yellow')
    canvas.create_text(app.width//2, app.height//2,
                       text = f'Your Score: {app.score}', font = 'Arial 40', fill = 'white')

    #Play Again Button                        
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 200 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 200 + app.title_PlayButtonWidth//2,
                            outline = "white")
    canvas.create_text(app.width//2, app.height//2 + 200,
                       text = "Play Again", font = 'Arial 36', fill = 'white')

    #Save Score Button                        
    canvas.create_rectangle(app.width//2- app.title_PlayButtonWidth, app.height//2 + 300 - app.title_PlayButtonWidth//2,
                            app.width//2 + app.title_PlayButtonWidth, app.height//2 + 300 + app.title_PlayButtonWidth//2,
                            outline = "white")
    canvas.create_text(app.width//2, app.height//2 + 300,
                       text = "Save Score", font = 'Arial 36', fill = 'white')

    #Leaderboard:                       
    canvas.create_rectangle(app.width//2 - 575, app.height//2 - 375,
                            app.width//2 - 450, app.height//2 - 325,
                            outline = "white")
    canvas.create_text(app.width//2 - 510, app.height//2 - 350,
                    text = "Top Scores", font = 'Arial 18', fill = 'white')

#TopScore:
def topScores_mousePressed(app,event):
    if (event.x > 75 and event.x < 75 + app.title_PlayButtonWidth and
        event.y > app.height - 100 and event.y < app.height - 50):
            app.mode = 'titleScreen'

def topScores_redrawAll(app,canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = "black")

    canvas.create_text(app.width//2, app.border + 200,
                        text = "Leaderboard", font = 'Arial 80', fill = 'Yellow')
    for i in range(3):
        canvas.create_text(app.width//2, app.border + 300 + i*100,
                        text = f'{i+1}. {app.topScoresName[i]} {app.topScores[i]}', font = 'Arial 40', fill = 'white')

    #Back Button:
    canvas.create_rectangle(75, app.height - 100,
                            75 + app.title_PlayButtonWidth, app.height - 50,
                            outline = "white", width = 3)
    canvas.create_text(125, app.height - 75,
                        text = 'Home', fill = 'white', font = 'Arial 24')
runApp(width = 1200, height = 1200)

