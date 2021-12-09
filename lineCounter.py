import os

path = os.path.abspath(os.getcwd())

def findFiles(path):
    files = []
    if os.path.isdir(path):
        for elem in os.listdir(path):
            if os.path.isfile(path + '/' + elem):
                if elem[-3:] == '.py':
                    files.append(path + '/' + elem)
            elif os.path.isdir(path + '/' + elem):
                for e in findFiles(path + '/' + elem):
                    if e[-3:] == '.py':
                        files.append(e)
    return files

def lineCounter(filepath, key = 1):
    f = open(filepath, "r")
    lines = f.readlines()
    counter = 0
    for line in lines:
        if line != '\n':
            if len(line.strip()) != 0:
                if line.strip()[0] != "#":
                    if key == 0: print(line[:-1])
                    counter += 1

    return counter

counter  = 0
for file in findFiles(path):
    if file.find('constants.py') < 0 and file.find('cmu_112_graphics.py') < 0 and file.find('lineCounter.py') < 0:
        counter+=lineCounter(file)

print(counter)