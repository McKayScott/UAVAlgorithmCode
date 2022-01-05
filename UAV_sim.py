import time
import math
import socket
import numpy as np
import struct

class UAV_sim:
    def __init__(self, path_x, path_y, path_z, velocity, port, ip = '127.0.0.1'):
        self.x = path_x
        self.y = path_y
        self.z = path_z
        self.vel = velocity                        #UNITS/Second
        self.current_location = (None, None, None) #X, Y, Z Location
        self.port = port
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def follow_path(self):
        tenth_of_vel = self.vel/10
        print("new drone")
        for i in range(len(self.x)-1):
            self.current_location = (self.x[i], self.y[i], self.z[i])
            x_diff = np.abs(self.x[i]-self.x[i+1])
            y_diff = np.abs(self.y[i]-self.y[i+1])
            z_diff = np.abs(self.z[i]-self.z[i+1])
            num_steps = 0
            if x_diff / tenth_of_vel > num_steps:
                num_steps = x_diff / tenth_of_vel
            if y_diff / tenth_of_vel > num_steps:
                num_steps = y_diff / tenth_of_vel
            if z_diff / tenth_of_vel > num_steps:
                num_steps = z_diff / tenth_of_vel
            x_step_array = np.linspace(self.x[i], self.x[i+1], math.floor(num_steps))
            y_step_array = np.linspace(self.y[i], self.y[i+1], math.floor(num_steps))
            z_step_array = np.linspace(self.z[i], self.z[i+1], math.floor(num_steps))
            for j in range(len(x_step_array)):
                self.current_location = (x_step_array[j], y_step_array[j], z_step_array[j])
                #print(self.current_location)
                #Return the current location here
                message = struct.pack('<3f',*self.current_location)
                #print(message)
                self.sock.sendto(message, 0, (self.ip, self.port))
                time.sleep(.1)

if __name__ == "__main__":
    x_path = [70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 600]
    y_path = [85, 85, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 30]            
    z_path = [20, 30, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20]
    my_drone = UAV_sim(x_path, y_path, z_path, 5, 7131).follow_path()

