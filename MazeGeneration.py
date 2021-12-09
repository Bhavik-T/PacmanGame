### MAZE GENERATION ###
import random

def generateMap2(rows):

    #Maze Pieces:
    squarePiece = [
        ['Wall','Wall'],
        ['Wall','Wall'],
    ]

    TPiece = [
        ['Wall','Wall','Wall'],
        ['Path','Wall','Path'],
    ]

    TPieceLeft = [
        ['Wall','Path','Path'],
        ['Wall','Wall','Wall'],
        ['Wall','Path','Path'],
    ]

    LPiece = [
        ['Wall','Path','Path'],
        ['Wall','Path','Path'],
        ['Wall','Wall','Wall'],
    ]

    LPieceInv = [
        ['Path','Path','Wall'],
        ['Path','Path','Wall'],
        ['Wall','Wall','Wall'],
    ]

    mapWalls = [squarePiece,TPiece,TPieceLeft,LPiece,LPieceInv]

    #Start with an empty grid
    map = [['Open']*rows for i in range(rows)]

    for row in range(1,len(map)//2):
        for col in range(1,len(map[0])//2):
            if map[col][row] == "Open":
                randomIndex = random.randint(0, (len(mapWalls) - 1))
                newWall = mapWalls[randomIndex]
                addWallToMap(map,row,col,newWall)

    GhostSpawnPiece = [
        ['Wall','Ghos','Ghos','Wall'],
        ['Wall','Ghos','Ghos','Wall'],
        ['Wall','Wall','Wall','Wall'],
    ]

    mirrorMap(map)
    mirrorMapX(map)

    middleX = (len(map)//2)-2
    middelY = (len(map)//2)-2
    addWallToMap(map,middleX,middelY,GhostSpawnPiece)

    #add powerup randomly:
    for count in range(5):
        x = random.randint(1,len(map)-1)
        y = random.randint(1,len(map)-1)
        while map[y][x] != 'Path':
            x = random.randint(0,len(map)-1)
            y = random.randint(0,len(map)-1)
        map[y][x] = "Powerup"
    return map

def addWallToMap(map,startRow,startCol,piece):
    for row in range(-1,len(piece)+1):
        for col in range(-1, len(piece[0])+1):
            if row == -1 or col == -1 or row == len(piece) or col == len(piece[0]):
                map[startCol+col][startRow+row] = "Path"
            else:
                map[startCol+col][startRow+row] = piece[row][col]

def mirrorMap(map):
    maplength = len(map)
    for y in range((maplength//2)):
        for x in range((maplength//2)):
            map[(maplength-1)-x][y] = map[x][y]

def mirrorMapX(map):
    maplength = len(map)
    for y in range((maplength//2)):
        for x in range((maplength)):
            map[x][(maplength-1)-y] = map[x][y]

def printMap(map):
    for row in map:
        print(row)
