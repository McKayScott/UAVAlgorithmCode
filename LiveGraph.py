
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

class graphing_grids: 
    def __init__(self):
    
        self.ax = plt.axes(projection='3d')

        self.namafile = 'Grid.csv'
        self.header1 = "x_value"
        self.header2 = "y_value"
        self.header3 = "z_value"

        self.index = count()

        self.G = GridDeveloper()
        self.matrixPoints = 20
        self.Grid, self.NodeGrid = self.G.developGrid(self.matrixPoints)

    #Plot stagnant grid
    def plotGrid(self):
        color = 0
        for plane in self.Grid:
                for line in plane:
                    x = []
                    y = []
                    z = []
                    for point in line:
                        x.append(point[0])
                        y.append(point[1])
                        z.append(point[2])
                    if color == 0:
                        self.ax.plot3D(x, y, z, 'red')
                    elif color == 1:
                        self.ax.plot3D(x, y, z, 'blue')
                    elif color == 2:
                        self.ax.plot3D(x, y, z, 'green')
                    elif color == 3:
                        self.ax.plot3D(x, y, z, 'black')
                color += 1

    def findDistance(self, node1, node2):
        distance = math.sqrt(((node1.x_val - node2.x_val)**2) + ((node1.y_val - node2.y_val)**2) + ((node1.z_val - node2.z_val)**2))
        return distance

    def getPath(self, sourcex, sourcey, sourcez, goalx, goaly, goalz, occupied_unique_idents):
        Grid, NodeGrid = self.G.developGrid(self.matrixPoints)
        sourceNode = NodeGrid[sourcex][sourcey][sourcez]
        sourceNode.score = 0
        #goalNode = NodeGrid[0][matrixPoints - 1][matrixPoints - 1]
        goalNode = NodeGrid[goalx][goaly][goalz]
        #Find the best Route
        currentNode = sourceNode
        q = queue.PriorityQueue()
        distance = self.findDistance(sourceNode, goalNode)
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
                    pathLength = currentNode.score + self.findDistance(currentNode, nNode)
                    if(pathLength < shortestPath):
                        distanceToGoal = self.findDistance(goalNode, nNode)
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

    def animate(self, i):
        #data = pd.read_csv('Grid.csv')
        #x = data[header1]
        #y = data[header2]
        #z = data[header3]
        plt.cla()
        self.plotGrid()
        occupied = []
        start_time = time.time()
        x, y, z, occupied = self.getPath(0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), 0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), occupied)
        self.ax.plot3D(x, y, z, 'purple')
        q, w, e, occupied = self.getPath(0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), 0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), occupied)
        self.ax.plot3D(q,w,e,'orange')
        a, s, d, occupied = self.getPath(0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), 0, random.randint(0, self.matrixPoints - 1), random.randint(0, self.matrixPoints - 1), occupied)
        self.ax.plot3D(a,s,d,'yellow')
        end_time = time.time()
        time_Elapsed = end_time - start_time
        print(time_Elapsed)
        #plt.legend(loc='upper left')
        #plt.tight_layout()

if __name__ == "__main__":
    grid_developer = graphing_grids()
    ani = FuncAnimation(plt.gcf(), grid_developer.animate, interval=5000)

    plt.tight_layout()
    plt.show()

    
