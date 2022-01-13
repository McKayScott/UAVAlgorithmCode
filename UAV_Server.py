import socket
import struct

from numpy import byte
from LiveGraph import *
from UAV_sim import *

class UAV_server: 
    def __init__(self):
        self.localIP     = "127.0.0.1"
        self.localPort   = 20001
        self.bufferSize  = 1024
        self.UAVServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UAVServerSocket.bind((self.localIP, self.localPort))
        # Maybe Someday...........
        # self.listening_dict = {
        #     1: self.register_new_drone,
        #     2: self.acknowledge_and_give_takeoff_permission,
        #     3: self.update_drone_position
        # }
        self.live_grapher = graphing_grids()
        self.occupied_unique_idents = []
        self.active_UAVs = []
        print("UAV server up and listening")

    def UAV_listening_tree(self):
        byte_data, address = self.UAVServerSocket.recvfrom(self.bufferSize)
        message = struct.unpack('iffffs',byte_data)

        #RECEIVING KEY - 1 IS REGISTER, 2 IS ACCEPT & REQUEST TAKEOFF, 3 IS LIVE POSITION UPDATE, 4 IS FREE VISITED NODE, 5 IS SIGN OFF)
        # struct.pack('ifff',1,3.1,3.1,0)
        # b'\x01\x00\x00\x00ffF@ffF@\x00\x00\x00\x00'
        # struct.unpack('ifff',b'\x01\x00\x00\x00ffF@ffF@\x00\x00\x00\x00')
        # (1, 3.0999999046325684, 3.0999999046325684, 0.0)

        if message[0] == 1:
            self.register_new_drone(message[1], message[2], message[3], message[4], address)
        elif message[0] == 2:
            self.acknowledge_and_give_takeoff_permission(address)
        elif message[0] == 3:
            self.update_drone_position(message[1], message[2], message[3], address)
        elif message[0] == 4:
            self.free_visited_node(message[1], message[2], message[5].decode('utf-8'), address)
        elif message[0] == 5:
            self.sign_off_drone(message[1], message[2], message[5].decode('utf-8'), address)

    def register_new_drone(self, origin_x, origin_y, goal_x, goal_y, new_drone_address):
        import copy
        new_pathx, new_pathy, new_pathz, new_occ = self.live_grapher.getPath(int(origin_x), int(origin_y), 0, int(goal_x), int(goal_y), 0, copy.deepcopy(self.occupied_unique_idents))
        #print(new_pathx)
        #print(new_pathy)
        #print(new_pathz)
        #print(new_occupied_unique_idents)
        #TODO FIGURE OUT BEST WAY TO SEND PATH BACK
        if new_occ == []:
            #NO PATH FOUND
            mess = struct.pack('ifffsii',0,0,0,0,'a'.encode('utf-8'),0,0)
            self.UAVServerSocket.sendto(mess,new_drone_address)
        else:
            for index in range(len(new_pathx)):
                self.occupied_unique_idents.append(new_occ[index])
                print(new_pathx[index],new_pathy[index],new_pathz[index],new_occ[index])
                layer, int1, int2 = self.id_to_parts(new_occ[index])
                mess = struct.pack('ifffsii',1,new_pathx[index],new_pathy[index],new_pathz[index],layer.encode('utf-8'),int1,int2) #TODO NUMBERS ARE OFFSET DUE TO DOUBLE DIGITS
                self.UAVServerSocket.sendto(mess,new_drone_address)
            mess = struct.pack('ifffsii',2,0,0,0,'a'.encode('utf-8'),0,0) #TODO, MAYBE SECOND INDEX HERE CONTAINS THE LENGTH OF THE PATH, AND CAN BE USED TO CHECK ON THE DRONE SIDE?
            self.UAVServerSocket.sendto(mess,new_drone_address)

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

    def acknowledge_and_give_takeoff_permission(self, address): #Don't need any other parameters, right? Just need to know that it is now active?
        self.active_UAVs.append(address)
        mess = struct.pack('i',1)
        self.UAVServerSocket.sendto(mess,address)

    def update_drone_position(self, x_pos, y_pos, z_pos, address):    #TODO SOME SORT OF UNIQUE TRIP ID FOR EACH DRONE
        print("Updating drone " + str(address) + "'s position to "+ str(x_pos) + " " + str(y_pos) + " " + str(z_pos))

    def free_visited_node(self, node_x, node_y, layer, address):   #TODO FIND BEST WAY TO IDENTIFY NODES THAT NEED TO BE FREED. COULD WE PASS THE NODE ID'S? OR IDENTIFY BY LOCATION?
        cc_string = layer + "_" + str(int(node_x)) + "_" + str(int(node_y))
        self.occupied_unique_idents.remove(cc_string)
        print("Freed " + cc_string)

    def sign_off_drone(self, node_x, node_y, layer, address):
        cc_string = layer + "_" + str(int(node_x)) + "_" + str(int(node_y))
        self.occupied_unique_idents.remove(cc_string)
        self.active_UAVs.remove(address)
        print(str(address) + " successfully finished")
    
if __name__ == "__main__":
    new_server = UAV_server()
    while(True):
        new_server.UAV_listening_tree()



