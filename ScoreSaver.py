import os
import datetime
import ast

def saveScore(score,name,path = os.path.abspath(os.getcwd())):
    if os.path.isdir(path):
        files = listFiles(path)
        if "PacmanScoreSheet.txt" in files:
            previousScores = ast.literal_eval(readFile(path))
            addScoreText = (datetime.datetime.now(), name, score)
            textPath = path + '/' + "PacmanScoreSheet.txt"
            addScoreText = previousScores + addScoreText
            writeFile(textPath,addScoreText)
        else:
            date = str(datetime.datetime.now())
            addScoreText = (f'\nDate: {date}, Name: {name}, Score: {score}')
            textPath = path + '/' + "PacmanScoreSheet.txt"
            writeFile(textPath, addScoreText)

def getScores(path = os.path.abspath(os.getcwd()) + '/' + "PacmanScoreSheet.txt"):
    topScores = [0,0,0]
    topScoreNames = ['','','']

    scoreFile = open(path,'r')
    scoresList = scoreFile.readlines()
    scoresLine = []
    for score in scoresList:
            line = score.split(' ')
            scoresLine.append(line)
    print(scoresLine)
    scores = getScores2helper(topScores,topScoreNames,scoresLine)
    print(f'insideScore: {score}')
    return scores

#Uses Recursion to get top scores:
def getScores2helper(topScores,topScoreNames,scoresLine):
    if scoresLine == []:
        print(f'returing: {topScores, topScoreNames}')
        return topScores, topScoreNames
    else:
        line = scoresLine[0]
        playerScore = int(line[-1])
        for index in range(len(topScores)):
            if isinstance(playerScore,int) and int(playerScore) > topScores[index]:
                topScores[index] = playerScore
                topScoreNames[index] = line[-3]
                break
        return getScores2helper(topScores,topScoreNames,scoresLine[1:])

#Adapted from 112 (https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#listFiles):
def listFiles(path):
    if os.path.isfile(path):
        # Base Case: return a list of just this file
        return [ path ]
    else:
        # Recursive Case: create a list of all the recursive results from
        # all the folders and files in this folder
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + '/' + filename)
        return files

#Basic File IO Functions:
def writeFile(path, contents):
    with open(path, "a") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

