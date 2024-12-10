# also has checking to ensure that our data doesn't look stupid when we move startX and startY around

import math

def mapToIndex(points, startX, startY):
    out = []
    for i in points:
        if i[0] < startX or i[0] > startX + 19 or i[1] > startY or i[1] < startY - 19: # big thing to check whether our wanted points are inside of our graph
            continue
        point = abs(startX - i[0]) # handles location on X axis
        point += (startY - i[1]) * 20 # handles location on Y axis
        if point not in out:
            out.append(math.floor(point))
    out.sort()
    return out

def setupAxis(graph, startX, startY):
    centerPoint = mapToIndex([(0, 0)], startX, startY) # creates an index for the center "+" to be placed at
    if len(centerPoint) == 0: # if we don't have a centerpoint, leave "centerPoint" null
        centerPoint = None
    else:
        centerPoint = centerPoint[0] # if we do have a centerpoint, give centerPoint an int value to look for in an index
    xLineS = startY * 20
    xLineE = (startY * 20) + 19
    graph = list(graph)
    for index, i in enumerate(graph): # check through whole graph because we can add it all in one loop for easier readibility
        if index == centerPoint: # add centerpointx
            graph[index] = "+"
        elif index >= xLineS and index <= xLineE: # add x axis
            graph[index] = "-"
        elif index % 20 == -startX: # add y axis
            graph[index] = "|"
    "".join(graph)
    return graph

def addToGraph(graph, points, symbol):
    graphOut = graph
    graphOut = list(graphOut)
    for i in points:
        graphOut[i] = symbol
    "".join(graphOut)
    return graphOut

def printGraph(graph):
    graph = list(graph)
    for index, i in enumerate(graph):
        if index % 20 == 19:
            print(i)
        else:
            print(i, end = " ")

if __name__ == "__main__":
    startX = -8
    startY = 15
    graph = "·"*400

    points = [(-8,77), (-7,60), (-6,45), (-5,32), (-4,21), (-3,12), (-2,5), (-1,0), (0,-3), (1,-4), (2,-3), (3,0), (4,5), (5,12), (6,21), (7,32), (8,45), (9,60), (10,77), (11,96)]
    points2 = [(-8,2), (-7,2), (-6,3), (-5,3), (-4,4), (-3,4), (-2,5), (-1,5), (0,6), (1,6), (2,7), (3,7), (4,8), (5,8), (6,9), (7,9), (8,10), (9,10), (10,11), (11,11)]
    
    points = mapToIndex(points, startX, startY)
    points2 = mapToIndex(points2, startX, startY)

    graph = setupAxis(graph, startX, startY)

    graphEnd = graph
    graphEnd = addToGraph(graphEnd, points2, "@")
    graphEnd = addToGraph(graphEnd, points, "#")

    printGraph(graphEnd)
