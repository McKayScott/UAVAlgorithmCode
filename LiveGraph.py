
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import queue
from matplotlib.animation import FuncAnimation
from GridDeveloper import *
from NodeClass import *
import math
import time
import random

#plt.style.use('fivethirtyeight') 
#Live update Data
#https://www.youtube.com/watch?v=sRYI5egdWLo

ax = plt.axes(projection='3d')

namafile = 'Grid.csv'
header1 = "x_value"
header2 = "y_value"
header3 = "z_value"

index = count()

G = GridDeveloper()
matrixPoints = 20
Grid, NodeGrid = G.developGrid(matrixPoints)

#Plot stagnant grid
def plotGrid():
    color = 0
    for plane in Grid:
            for line in plane:
                x = []
                y = []
                z = []
                for point in line:
                    x.append(point[0])
                    y.append(point[1])
                    z.append(point[2])
                if color == 0:
                    ax.plot3D(x, y, z, 'red')
                elif color == 1:
                    ax.plot3D(x, y, z, 'blue')
                elif color == 2:
                    ax.plot3D(x, y, z, 'green')
                elif color == 3:
                    ax.plot3D(x, y, z, 'black')
            color += 1

def findDistance(node1, node2):
    distance = math.sqrt(((node1.x_val - node2.x_val)**2) + ((node1.y_val - node2.y_val)**2) + ((node1.z_val - node2.z_val)**2))
    return distance

def getPath(sourcex, sourcey, sourcez, goalx, goaly, goalz, occupied_unique_idents):
    Grid, NodeGrid = G.developGrid(matrixPoints)
    sourceNode = NodeGrid[sourcex][sourcey][sourcez]
    sourceNode.score = 0
    #goalNode = NodeGrid[0][matrixPoints - 1][matrixPoints - 1]
    goalNode = NodeGrid[goalx][goaly][goalz]
    #Find the best Route
    currentNode = sourceNode
    q = queue.PriorityQueue()
    distance = findDistance(sourceNode, goalNode)
    q.put((distance, -1 ,currentNode))
    justVisited = None
    pathFound = 0
    i = 0
    shortestPath = math.inf
    while(not q.empty()):
        tup = q.get()
        currentNode = tup[2]
        for nNode in currentNode.neighborNodes :
            if(nNode.uniqueIdentifier not in currentNode.prevNodes and nNode.uniqueIdentifier not in occupied_unique_idents):
                pathLength = currentNode.score + findDistance(currentNode, nNode)
                if(pathLength < shortestPath):
                    distanceToGoal = findDistance(goalNode, nNode)
                    if distanceToGoal == 0:
                        pathFound += 1
                        nNode.setParent(currentNode)
                        nNode.prevNodes = currentNode.prevNodes
                        nNode.addPrevNode(currentNode.uniqueIdentifier)
                        nNode.score = pathLength
                        shortestPath = pathLength
                    elif nNode.score == -1:
                        nNode.setParent(currentNode)
                        fullDist = distanceToGoal + pathLength
                        nNode.score = pathLength
                        nNode.prevNodes = currentNode.prevNodes
                        nNode.addPrevNode(currentNode.uniqueIdentifier)
                        q.put((fullDist, i , nNode))
                    else :
                        if(pathLength < nNode.score):
                            nNode.setParent(currentNode)
                            nNode.score = pathLength
                            fullDist = distanceToGoal + pathLength
                            q.put((fullDist, i , nNode))
                            nNode.prevNodes = currentNode.prevNodes
                            nNode.addPrevNode(currentNode.uniqueIdentifier)
            i += 1
        justVisited = currentNode
    currentNode = goalNode
    x = []
    y = []
    z = []
    x.append(goalNode.x_val)
    y.append(goalNode.y_val)
    z.append(goalNode.z_val)
    #print('source node:' + sourceNode.uniqueIdentifier)
    while(currentNode.uniqueIdentifier != sourceNode.uniqueIdentifier):
        occupied_unique_idents.append(currentNode.uniqueIdentifier)
        currentNode = currentNode.getParent()
        x.append(currentNode.x_val)
        y.append(currentNode.y_val)
        z.append(currentNode.z_val)
        #print(currentNode.uniqueIdentifier)
    return x, y, z, occupied_unique_idents

def animate(i):
    #data = pd.read_csv('Grid.csv')
    #x = data[header1]
    #y = data[header2]
    #z = data[header3]
    plt.cla()
    plotGrid()
    occupied = []
    start_time = time.time()
    x, y, z, occupied = getPath(0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), 0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), occupied)
    ax.plot3D(x, y, z, 'purple')
    q, w, e, occupied = getPath(0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), 0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), occupied)
    ax.plot3D(q,w,e,'orange')
    a, s, d, occupied = getPath(0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), 0, random.randint(0, matrixPoints - 1), random.randint(0, matrixPoints - 1), occupied)
    ax.plot3D(a,s,d,'yellow')
    end_time = time.time()
    time_Elapsed = end_time - start_time
    print(time_Elapsed)
    #plt.legend(loc='upper left')
    #plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=5000)

plt.tight_layout()
plt.show()

def findDistance(node1, node2):
    distance = math.sqrt(((node1.x_val - node2.x_val)**2) + ((node1.y_val - node2.y_val)**2) + ((node1.z_val - node2.z_val)**2))
    return distance
