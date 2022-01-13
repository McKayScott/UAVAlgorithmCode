import time
import math
import socket
import numpy as np
import struct
#import rospy
#from vizualizer import *

# STATE TREE
# 1: On startup, reaches out to server to register and request a path
# 2: On receiving the path, acknowledges and requests permission to takeoff
# 3: Drone starts to follow path, transmitting live data and communicating which nodes are checked off
# 4: Upon finishing the path, communicates to the server that the path is finished.

class UAV_sim:
    def __init__(self, velocity, origin_x, origin_y, goal_x, goal_y, server_port= 20001, server_ip = '127.0.0.1'):
        self.vel = velocity                        #UNITS/Second
        self.current_location = (None, None, None) #X, Y, Z Location
        self.port = server_port
        self.ip = server_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.org_x = origin_x
        self.org_y = origin_y
        self.goal_x = goal_x
        self.goal_y = goal_y
        message = struct.pack('iffffs',1,self.org_x,self.org_y,self.goal_x,self.goal_y,'a'.encode('utf-8'))
        self.sock.sendto(message, 0, (server_ip, server_port))
        self.x = []
        self.y = []
        self.z = []
        self.path_nodes = []

    def UAV_listen_for_path(self):
        # RECEIVING KEY - 0 IS PATH IMPOSSIBLE; WAIT 10 SECONDS, 1 IS SUCCESSFUL PATH PASSED, 2 PATH FINISHED, 3 IS TAKEOFF CERTIFIED
        byte_input, address = self.sock.recvfrom(1024)
        input = struct.unpack('ifffsii',byte_input)
        print(input)
        if input[0] == 0:
            time.sleep(10)
            self.UAV_listen_for_path()
        else: 
            while input[0] == 1:
                self.x.append(input[1]) #TODO FINISH THE APPENDING. CHECK TO SEE IF IT IS LOSSY.
                self.y.append(input[2])
                self.z.append(input[3])
                self.path_nodes.append(self.input_to_nodeID(input[4], input[5], input[6]))
                byte_input, address = self.sock.recvfrom(1024)
                input = struct.unpack('ifffsii',byte_input)
            print(self.x)
            print(self.y)
            print(self.z)
            print(self.path_nodes)
            request = struct.pack('iffffs',2,0,0,0,0,'a'.encode('utf-8'))
            self.sock.sendto(request, 0, (self.ip, self.port))
            print("Requesting Permission to Takeoff")
            self.receive_takeoff_permission()
        
    def input_to_nodeID(self, char, index1, index2):
        return char.decode('utf-8') + '_' + str(index1) + '_' + str(index2)

    def receive_takeoff_permission(self): # 1 is go, 0 is wait
        byte_input, address = self.sock.recvfrom(1024)
        input = struct.unpack('i',byte_input)
        if input[0] == 1:
            self.follow_path()
        else: print("PERMISSION NOT GRANTED")
    
    def follow_path(self):
        tWenth_of_vel = self.vel/20
        print("new drone")
        for i in range(len(self.x)-1):
            self.current_location = (self.x[i], self.y[i], self.z[i])
            x_diff = np.abs(self.x[i]-self.x[i+1])
            y_diff = np.abs(self.y[i]-self.y[i+1])
            z_diff = np.abs(self.z[i]-self.z[i+1])
            num_steps = 0
            if x_diff / tWenth_of_vel > num_steps:
                num_steps = x_diff / tWenth_of_vel
            if y_diff / tWenth_of_vel > num_steps:
                num_steps = y_diff / tWenth_of_vel
            if z_diff / tWenth_of_vel > num_steps:
                num_steps = z_diff / tWenth_of_vel
            x_step_array = np.linspace(self.x[i], self.x[i+1], math.floor(num_steps))
            y_step_array = np.linspace(self.y[i], self.y[i+1], math.floor(num_steps))
            z_step_array = np.linspace(self.z[i], self.z[i+1], math.floor(num_steps))
            for j in range(len(x_step_array)):
                self.current_location = (x_step_array[j], y_step_array[j], z_step_array[j])
                print(self.current_location)
                #Return the current location here
                message = struct.pack('iffffs',3,self.current_location[0],self.current_location[1],self.current_location[2],0,'a'.encode('utf-8'))
                #print(message)
                self.sock.sendto(message, 0, (self.ip, self.port))
                #rospy.init_node("test"+str(self.port), anonymous=False, log_level=rospy.INFO, disable_signals=False)
                #self.ros_pubs = ros_marker_organizer(self.port)

                #self.ros_pubs.publish_drone(self.current_location[0],self.current_location[1],self.current_location[2])
                time.sleep(.05)
            layer, int1, int2 = self.id_to_parts(self.path_nodes[i])
            message = struct.pack('iffffs',4,int1,int2,0,0,layer.encode('utf-8'))
            self.sock.sendto(message, 0, (self.ip, self.port))
        layer, int1, int2 = self.id_to_parts(self.path_nodes[len(self.x)-1])
        message = struct.pack('iffffs',5,int1,int2,0,0,layer.encode('utf-8'))
        self.sock.sendto(message, 0, (self.ip, self.port))       

    def id_to_parts(self, id):#TODO IF MATRIX POINTS ARE THREE DIGITS THIS NEEDS TO BE REVAMPED
        layer = id[0]
        int1 = id[2]
        int2 = ''
        if id[3] == '_':
            int2 = int2 + id[4]
            if len(id) == 6:
                int2 = int2 + id[5]
        else: 
            int1 = int1 + id[3]
            int2 = int2 + id[5]
            if len(id) == 7:
                int2 = int2 + id[6]
        return layer, int(int1), int(int2)

if __name__ == "__main__":
    # x_path = [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 60]
    # y_path = [85, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 30]            
    # z_path = [20, 30, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20]
    my_drone = UAV_sim(np.random.randint(0,10), np.random.randint(0,20), np.random.randint(0,20), np.random.randint(0,20), np.random.randint(0,20)).UAV_listen_for_path()



