'''
Used Pusedo Code from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2    
'''
class Vertex(object):
    def __init__(self, parent = None, position= None):
        self.parent = parent
        self.position = position
        self.cost = 0           # F
        self.currToStart = 0    # g
        self.currToTarget = 0   # h
    
    def __eq__(self, other):
        return self.position == other.position

def astar(map, start, end):

    # Initialize both open and closed list
    openList = []
    closedList = []

    # Add the start node, put the startNode on the openList (leave it's f at zero)
    startingPostion = Vertex(None, start)
    openList.append(startingPostion)

    targetPosition = Vertex(None, end)

    # Loop until you find the end while the openList is not empty
    iterations = 0
    while len(openList) > 0:
        if iterations > 5000: break
        iterations += 1

        # Get the current node
        # let the currentNode equal the node with the least f value
        currentNode = openList[0]
        currentIndex = 0
        for i in range(len(openList)):
            node = openList[i]
            if node.cost < currentNode.cost:
                currentNode = node
                currentIndex = i

        # remove the currentNode from the openList
        #  add the currentNode to the closedList
        openList.pop(currentIndex)
        closedList.append(currentNode)

        # Found the goal
        if currentNode == targetPosition:   # if currentNode is the goal
            shortestpath = []
            while currentNode is not None:
                shortestpath.append(currentNode.position)
                currentNode = currentNode.parent
            return shortestpath[::-1]   

        # Generate children
        # let the children of the currentNode equal the adjacent nodes
        children = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                if abs(dx) != abs(dy):
                    childX = currentNode.position[0] + dx
                    childY = currentNode.position[1] + dy
                    #If out of bounds:
                    if (childX >= len(map) or childX < 0 or 
                        childY < 0 or childY >= len(map)):
                        continue
                    #If cell is a wall:
                    if map[childX][childY] == "Wall":
                        continue
                    children.append(Vertex(currentNode,(childX,childY)))

        for child in children:
            
            # if child is in the closedList
            # continue to beginning of for loop
            if child in closedList:
                continue

            # Create the f, g, and h values
            child.currToStart = currentNode.currToStart + 1
            child.currToTarget = (((child.position[0] - targetPosition.position[0])**2) +
                                  ((child.position[1] - targetPosition.position[1])**2))
            child.cost = child.currToStart + child.currToTarget

            # if child.position is in the openList's nodes positions
            # if the child.g is higher than the openList node's g
            #     continue to beginning of for loop
            for openNode in openList:
                if child == openNode and child.currToStart > openNode.currToStart:
                    continue

            # Add the child to the openList
            openList.append(child)