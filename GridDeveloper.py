#Generates random data
#TO RUN, OPEN ONE FILE IN THE NORMAL TERMINAL AND ONE IN DEBUG
import csv
import random
import time
from NodeClass import *
class GridDeveloper:
    def developGrid(self, mp) :
        namafile = 'Grid.csv'
        header1 = "x_value"
        header2 = "y_value"
        header3 = "z_value"
        #North-South, x_value, North Positive
        #East-West, y_value, West Positive
        #Altitude, z_value, Up Positive


        fieldnames = [header1, header2, header3]

        #第零 3 DIMENSIONAL ARRAY                               CUBE
        #第一 First layer, planes of different altitudes        PLANE
        #第二 Second layer, individual channels on each plane   LINE 
        #第三 third layer, points in that channel               POINT

        CUBE = []
        NODES = []

        with open(namafile, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()



        with open(namafile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            MATRIX_POINTS = mp
            POINTS_DIFFERENCE = 5
            ALTITUDE_START = 20
            ALTITUDE_DIFFERENCE = 10
            X_START = 0
            Y_START = 0

            x_value = 0
            y_value = 0
            z_value = ALTITUDE_START

            
            info = {
                header1: x_value,
                header2: y_value,
                header3: z_value
            }

            #Layer 1, North-South, altitude 20
            PLANE = []
            PLANE_N = []
            for i in range(MATRIX_POINTS):
                x_value = X_START
                LINE = []
                LINE_N = []
                firstNode = True
                prevNode = None
                for j in range(MATRIX_POINTS):
                    info = {
                        header1: x_value,
                        header2: y_value,
                        header3: z_value
                    }
                    csv_writer.writerow(info)
                    #print(x_value, y_value, z_value)
                    POINT = [x_value, y_value, z_value]
                    curNode = gridNode(x_value, y_value, z_value, ('A_'+str(i)+'_'+str(j)))
                    if(not firstNode):
                        curNode.addNeighbor(prevNode)
                        prevNode.addNeighbor(curNode)
                    LINE.append(POINT)
                    LINE_N.append(curNode)
                    firstNode = False
                    prevNode = curNode
                    x_value += POINTS_DIFFERENCE
                y_value += POINTS_DIFFERENCE
                PLANE.append(LINE)
                PLANE_N.append(LINE_N)
            CUBE.append(PLANE)
            NODES.append(PLANE_N)

            #Layer 2, NorthEast-SouthWest, altitude 30
            z_value += ALTITUDE_DIFFERENCE
            PLANE = []
            PLANE_N = []
            y_value = Y_START
            x_base = X_START
            i = 0
            firstNode = True
            while(x_base <= 2*(POINTS_DIFFERENCE * (MATRIX_POINTS-1))) :
                x_value = x_base
                y_value = Y_START
                LINE = []
                LINE_N = []
                j = 0
                while(x_value >= (X_START)):
                    if((x_value <= (POINTS_DIFFERENCE * (MATRIX_POINTS-1))) and (y_value <= (POINTS_DIFFERENCE * (MATRIX_POINTS-1)))):
                        info = {
                            header1: x_value,
                            header2: y_value,
                            header3: z_value
                        }
                        csv_writer.writerow(info)
                        #print(x_value, y_value, z_value)
                        POINT = [x_value, y_value, z_value]
                        curNode = gridNode(x_value, y_value, z_value, ('B_'+str(i)+'_'+str(j)))
                        if(not firstNode):
                            curNode.addNeighbor(prevNode)
                            prevNode.addNeighbor(curNode)
                        LINE.append(POINT)
                        LINE_N.append(curNode)
                        firstNode = False
                        prevNode = curNode
                    y_value += POINTS_DIFFERENCE
                    x_value -= POINTS_DIFFERENCE
                    j += 1
                x_base += POINTS_DIFFERENCE
                PLANE.append(LINE)
                PLANE_N.append(LINE_N)
                i += 1
            CUBE.append(PLANE)
            NODES.append(PLANE_N)  

            #Layer 3, West-East, altitude 40
            z_value += ALTITUDE_DIFFERENCE
            x_value = X_START
            y_value = Y_START
            PLANE = []
            PLANE_N = []
            firstNode = True
            for i in range(MATRIX_POINTS):
                y_value = Y_START
                LINE = []
                LINE_N = []
                for j in range(MATRIX_POINTS):
                    info = {
                        header1: x_value,
                        header2: y_value,
                        header3: z_value
                    }
                    csv_writer.writerow(info)
                    #print(x_value, y_value, z_value)
                    POINT = [x_value, y_value, z_value]
                    curNode = gridNode(x_value, y_value, z_value, ('C_'+str(i)+'_'+str(j)))
                    if(not firstNode):
                        curNode.addNeighbor(prevNode)
                        prevNode.addNeighbor(curNode)
                    LINE.append(POINT)
                    LINE_N.append(curNode)
                    firstNode = False
                    prevNode = curNode
                    y_value += POINTS_DIFFERENCE
                x_value += POINTS_DIFFERENCE
                PLANE.append(LINE)
                PLANE_N.append(LINE_N)
            CUBE.append(PLANE)
            NODES.append(PLANE_N)

            #Layer 4, NorthWest-SouthEast, altitude 50
            z_value += ALTITUDE_DIFFERENCE
            x_base = (POINTS_DIFFERENCE * (MATRIX_POINTS-1))
            y_base = Y_START
            PLANE = []
            PLANE_N = []
            i = 0
            firstNode = True
            while(x_base >= -(POINTS_DIFFERENCE * (MATRIX_POINTS-1))) :
                x_value = x_base
                y_value = Y_START
                LINE = []
                LINE_N = []
                j = 0
                while(y_value <= (POINTS_DIFFERENCE * (MATRIX_POINTS-1))):
                    if((x_value <= (POINTS_DIFFERENCE * (MATRIX_POINTS-1))) and (y_value <= (POINTS_DIFFERENCE * (MATRIX_POINTS-1))) and (x_value >= X_START)):
                        info = {
                            header1: x_value,
                            header2: y_value,
                            header3: z_value
                        }
                        csv_writer.writerow(info)
                        #print(x_value, y_value, z_value)
                        POINT = [x_value, y_value, z_value]
                        curNode = gridNode(x_value, y_value, z_value, ('D_'+str(i)+'_'+str(j)))
                        if(not firstNode):
                            curNode.addNeighbor(prevNode)
                            prevNode.addNeighbor(curNode)
                        LINE.append(POINT)
                        LINE_N.append(curNode)
                        firstNode = False
                        prevNode = curNode
                    x_value += POINTS_DIFFERENCE
                    y_value += POINTS_DIFFERENCE
                    j += 1
                x_base -= POINTS_DIFFERENCE
                PLANE.append(LINE)
                PLANE_N.append(LINE_N)
                i += 1
            CUBE.append(PLANE)
            NODES.append(PLANE_N)

            newNODES = self.addVerticalNeighbors(NODES)

        return CUBE, newNODES

    def addVerticalNeighbors(self, nodeMatrix):
        planeNo = 1
        while(planeNo < len(nodeMatrix)):
            current_Plane = nodeMatrix[planeNo]
            for current_Line in current_Plane :
                for current_Point in current_Line:
                    found = False
                    bottom_Plane = nodeMatrix[planeNo - 1]
                    for bottom_Line in bottom_Plane:
                        if(not found):
                            for bottom_Point in bottom_Line:
                                if(bottom_Point.x_val == current_Point.x_val) :
                                    if (bottom_Point.y_val == current_Point.y_val):
                                        found = True
                                        bottom_Point.addNeighbor(current_Point)
                                        current_Point.addNeighbor(bottom_Point)
            planeNo += 1
        return nodeMatrix

                        
