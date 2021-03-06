# Python includes
import numpy
import random

# ROS includes
import roslib
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Vector3, Polygon
from tf import transformations # rotation_matrix(), concatenate_matrices()

from rviz_tools_for_me import *
from visualization_msgs.msg import Marker, MarkerArray

# Initialize the ROS Node
class ros_marker_organizer:
    def __init__(self):
        #rospy.init_node('test', anonymous=False, log_level=rospy.INFO, disable_signals=False)
        self.pub_rviz_marker = rospy.Publisher("visualization_marker", Marker, queue_size=10)
        self.pub_rviz_marker_array = rospy.Publisher("visualization_marker_array", MarkerArray, queue_size=10)

    def publish_drone(self, x_val, y_val, z_val):
        sphere_marker = Marker()
        sphere_marker.header.frame_id = "base_frame"
        sphere_marker.ns = "Sphere" # unique ID
        sphere_marker.type = Marker().SPHERE
        sphere_marker.action = Marker().ADD
        sphere_marker.lifetime = rospy.Duration(0.0)
        sphere_marker.pose.position.x = x_val
        sphere_marker.pose.position.y = y_val
        sphere_marker.pose.position.z = z_val
        sphere_marker.scale.x = 1.0
        sphere_marker.scale.y = 1.0
        sphere_marker.scale.z = 1.0
        sphere_marker.pose.orientation.x = 0.0
        sphere_marker.pose.orientation.y = 0.0
        sphere_marker.pose.orientation.z = 0.0
        sphere_marker.pose.orientation.w = 1.0
        sphere_marker.color.a = 1.0
        sphere_marker.color.r = 0.0
        sphere_marker.color.g = 1.0
        sphere_marker.color.b = 0.0
        self.pub_rviz_marker.publish(sphere_marker)

    def publish_path(self, x_vals, y_vals, z_vals):
        marker_array = MarkerArray()
        for i in range(len(x_vals)):
            other_sphere_marker = Marker()
            other_sphere_marker.header.frame_id = "base_frame"
            other_sphere_marker.ns = "Sphere" + str(i) # unique ID
            other_sphere_marker.type = Marker().SPHERE
            other_sphere_marker.action = Marker().ADD
            other_sphere_marker.lifetime = rospy.Duration(0.0)
            other_sphere_marker.scale.x = 0.5
            other_sphere_marker.scale.y = 0.5
            other_sphere_marker.scale.z = 0.5
            other_sphere_marker.pose.position.x = x_vals[i]
            other_sphere_marker.pose.position.y = y_vals[i]
            other_sphere_marker.pose.position.z = z_vals[i]
            other_sphere_marker.pose.orientation.x = 0.0
            other_sphere_marker.pose.orientation.y = 0.0
            other_sphere_marker.pose.orientation.z = 0.0
            other_sphere_marker.pose.orientation.w = 1.0
            other_sphere_marker.color.a = 1.0
            other_sphere_marker.color.r = 1.0
            other_sphere_marker.color.g = 1.0
            other_sphere_marker.color.b = 0.0
            marker_array.markers.append(other_sphere_marker)
        self.pub_rviz_marker_array.publish(marker_array)

if __name__ == "__main__":
    new_pubber = ros_marker_organizer()
    i = 0
    xvals = []
    yvals = []
    zvals = []
    while(i<100):
        #print("running")
        new_pubber.publish_drone(i-50,0,0)
        xvals.append(i-50)
        yvals.append(0)
        zvals.append(0)
        new_pubber.publish_path(xvals,yvals,zvals)
        rospy.sleep(0.5)
        i += 1

    

# markers = RvizMarkers('/map', 'visualization_marker')

# # Define exit handler
# def cleanup_node():
#     print("Shutting down node")
#     markers.deleteAllMarkers()

# rospy.on_shutdown(cleanup_node)


# while not rospy.is_shutdown():

#     # Axis:

#     # Publish an axis using a numpy transform matrix
#     T = transformations.translation_matrix((1,0,0))
#     axis_length = 0.4
#     axis_radius = 0.05
#     markers.publishAxis(T, axis_length, axis_radius, 5.0) # pose, axis length, radius, lifetime

#     # Publish an axis using a ROS Pose Msg
#     P = Pose(Point(2,0,0),Quaternion(0,0,0,1))
#     axis_length = 0.4
#     axis_radius = 0.05
#     markers.publishAxis(P, axis_length, axis_radius, 5.0) # pose, axis length, radius, lifetime


#     # Line:

#     # Publish a line between two ROS Point Msgs
#     point1 = Point(-2,1,0)
#     point2 = Point(2,1,0) 
#     width = 0.05
#     markers.publishLine(point1, point2, 'green', width, 5.0) # point1, point2, color, width, lifetime

#     # Publish a line between two ROS Poses
#     P1 = Pose(Point(-2,1.1,0),Quaternion(0,0,0,1))
#     P2 = Pose(Point(2,1.1,0),Quaternion(0,0,0,1))
#     width = 0.02
#     markers.publishLine(P1, P2, 'red', width, 5.0) # point1, point2, color, width, lifetime

#     # Publish a line between two numpy transform matrices
#     T1 = transformations.translation_matrix((-2,1.2,0))
#     T2 = transformations.translation_matrix((2,1.2,0))
#     width = 0.02
#     markers.publishLine(T1, T2, 'blue', width, 5.0) # point1, point2, color, width, lifetime


#     # Path:

#     # Publish a path using a list of ROS Point Msgs
#     path = []
#     path.append( Point(0,-0.5,0) )
#     path.append( Point(1,-0.5,0) )
#     path.append( Point(1.5,-0.2,0) )
#     path.append( Point(2,-0.5,0) )
#     path.append( Point(2.5,-0.2,0) )
#     path.append( Point(3,-0.5,0) )
#     path.append( Point(4,-0.5,0) )
#     width = 0.02
#     markers.publishPath(path, 'orange', width, 5.0) # path, color, width, lifetime


#     # Plane / Rectangle:

#     # Publish a rectangle between two points (thin, planar surface)
#     # If the z-values are different, this will produce a cuboid
#     point1 = Point(-1,0,0)
#     point2 = Point(-2,-1,0) 
#     markers.publishRectangle(point1, point2, 'blue', 5.0)

#     # Publish a rotated plane using a numpy transform matrix
#     R_y = transformations.rotation_matrix(0.3, (0,1,0)) # Rotate around y-axis by 0.3 radians
#     T0 = transformations.translation_matrix((-3,-1.5,0))
#     T = transformations.concatenate_matrices(T0, R_y)
#     depth = 1.1
#     width = 1.5
#     markers.publishPlane(T, depth, width, 'purple', 5.0) # pose, depth, width, color, lifetime

#     # Publish a plane using a ROS Pose Msg
#     P = Pose(Point(-3,0,0),Quaternion(0,0,0,1))
#     depth = 1.3
#     width = 1.3
#     markers.publishPlane(P, depth, width, 'brown', 5.0) # pose, depth, width, color, lifetime


#     # Polygon:

#     # Publish a polygon using a ROS Polygon Msg
#     polygon = Polygon()
#     polygon.points.append( Point(0.0,-1.0,0.0) )
#     polygon.points.append( Point(0.0,-2.0,0.0) )
#     polygon.points.append( Point(-1.0,-2.0,0.0) )
#     polygon.points.append( Point(-1.0,-1.0,0.0) )
#     markers.publishPolygon(polygon, 'red', 0.02, 5.0) # path, color, width, lifetime


#     # Text:

#     # Publish some text using a ROS Pose Msg
#     P = Pose(Point(3,-1,0),Quaternion(0,0,0,1))
#     scale = Vector3(0.2,0.2,0.2)
#     markers.publishText(P, 'This is some text', 'white', scale, 5.0) # pose, text, color, scale, lifetime


#     # Arrow:

#     # Publish an arrow using a numpy transform matrix
#     T = transformations.translation_matrix((1,-2,0))
#     scale = Vector3(1.0,0.2,0.2) # x=length, y=height, z=height
#     markers.publishArrow(T, 'blue', scale, 5.0) # pose, color, scale, lifetime

#     # Publish an arrow using a ROS Pose Msg
#     P = Pose(Point(1,-3,0),Quaternion(0,0,0,1))
#     arrow_length = 2.0 # single value for length (height is relative)
#     markers.publishArrow(P, 'pink', arrow_length, 5.0) # pose, color, arrow_length, lifetime


#     # Cube / Cuboid:

#     # Publish a cube using a numpy transform matrix
#     T = transformations.translation_matrix((-3,2.2,0))
#     cube_width = 0.5 # cube is 0.5x0.5x0.5
#     markers.publishCube(T, 'green', cube_width, 5.0) # pose, color, cube_width, lifetime

#     # Publish a cube using a ROS Pose Msg
#     P = Pose(Point(-2,2.2,0),Quaternion(0,0,0,1))
#     cube_width = 0.6
#     markers.publishCube(P, 'blue', cube_width, 5.0) # pose, color, cube_width, lifetime

#     # Publish a cube using wrapper function publishBlock()
#     P = Pose(Point(-1,2.2,0),Quaternion(0,0,0,1))
#     cube_width = 0.7
#     markers.publishBlock(P, 'orange', cube_width, 5.0) # pose, color, cube_width, lifetime

#     # Publish a cuboid using a numpy transform matrix
#     T = transformations.translation_matrix((0.6,2.2,0))
#     scale = Vector3(1.5,0.2,0.2)
#     markers.publishCube(T, 'yellow', scale, 5.0) # pose, color, scale, lifetime

#     # Publish a cuboid using a ROS Pose Msg
#     P = Pose(Point(2.2,2.2,0),Quaternion(0,0,0,1))
#     scale = Vector3(1.1,0.2,0.8)
#     markers.publishCube(P, 'brown', scale, 5.0) # pose, color, scale, lifetime


#     # List of cubes:

#     # Publish a set of cubes using a list of ROS Point Msgs
#     points = []
#     z_height = 0.1
#     points.append(Point(3.5+0*0.2, 0.5, z_height)) # row 1
#     points.append(Point(3.5+1*0.2, 0.5, z_height))
#     points.append(Point(3.5+2*0.2, 0.5, z_height))
#     points.append(Point(3.5+0*0.2, 0.5+1*0.2, z_height)) # row 2
#     points.append(Point(3.5+1*0.2, 0.5+1*0.2, z_height))
#     points.append(Point(3.5+2*0.2, 0.5+1*0.2, z_height))
#     points.append(Point(3.5+0*0.2, 0.5+2*0.2, z_height)) # row 3
#     points.append(Point(3.5+1*0.2, 0.5+2*0.2, z_height))
#     points.append(Point(3.5+2*0.2, 0.5+2*0.2, z_height))
#     points.append(Point(3.5+0*0.2, 0.5+2*0.2, z_height+0.2)) # 2nd layer
#     diameter = 0.2-0.005
#     markers.publishCubes(points, 'red', diameter, 5.0) # path, color, diameter, lifetime


#     # Sphere:

#     # Publish a sphere using a numpy transform matrix
#     T = transformations.translation_matrix((-3,3.2,0))
#     scale = Vector3(0.5,0.5,0.5) # diameter
#     color = [0,1,0] # list of RGB values (green)
#     markers.publishSphere(T, color, scale, 5.0) # pose, color, scale, lifetime

#     # Publish a sphere using a ROS Pose
#     P = Pose(Point(-2,3.2,0),Quaternion(0,0,0,1))
#     scale = Vector3(0.6,0.6,0.6) # diameter
#     color = (0,0,1) # tuple of RGB values (blue)
#     markers.publishSphere(P, color, scale, 5.0) # pose, color, scale, lifetime

#     # Publish a sphere using a ROS Point
#     point = Point(-1,3.2,0)
#     scale = Vector3(0.7,0.7,0.7) # diameter
#     color = 'orange'
#     markers.publishSphere(point, color, scale, 5.0) # pose, color, scale, lifetime

#     # Publish a sphere by passing diameter as a float
#     point = Point(0,3.2,0)
#     diameter = 0.8
#     markers.publishSphere(point, 'yellow', diameter, 5.0) # pose, color, diameter, lifetime

#     # Publish a sphere with higher render quality (this is one sphere in a SPHERE_LIST)
#     point = Point(1,3.2,0)
#     diameter = 0.9
#     markers.publishSphere2(point, 'brown', diameter, 5.0) # pose, color, scale, lifetime


#     # List of spheres:

#     # Publish a set of spheres using a list of ROS Point Msgs
#     points = []
#     points.append( Point(-3,4,0) )
#     points.append( Point(-2,4,0) )
#     points.append( Point(-1,4,0) )
#     points.append( Point(0,4,0) )
#     diameter = 0.3
#     markers.publishSpheres(points, 'white', diameter, 5.0) # path, color, diameter, lifetime
    
#     # Publish a set of spheres using a list of ROS Pose Msgs
#     poses = []
#     poses.append( Pose(Point(1,4,0),Quaternion(0,0,0,1)) )
#     poses.append( Pose(Point(2,4,0),Quaternion(0,0,0,1)) )
#     poses.append( Pose(Point(3,4,0),Quaternion(0,0,0,1)) )
#     scale = Vector3(0.5,0.5,0.5) # diameter
#     markers.publishSpheres(poses, 'blue', scale, 5.0) # path, color, scale, lifetime

#     # Publish a set of spheres using a list of numpy transform matrices
#     poses = []
#     poses.append( Pose(Point(4,4,0),Quaternion(0,0,0,1)) )
#     poses.append( Pose(Point(5,4,0),Quaternion(0,0,0,1)) )
#     diameter = 0.6
#     markers.publishSpheres(poses, 'green', diameter, 5.0) # path, color, scale, lifetime


#     # Cylinder:

#     # Publish a cylinder using a numpy transform matrix
#     T = transformations.translation_matrix((-3,5,0))
#     markers.publishCylinder(T, 'green', 1.0, 0.5, 5.0) # pose, color, height, radius, lifetime

#     # Publish a cylinder using a ROS Pose
#     P = Pose(Point(-2,5,0),Quaternion(0,0,0,1))
#     markers.publishCylinder(P, 'blue', 1.0, 0.5, 5.0) # pose, color, height, radius, lifetime


#     # Publish a cylinder of a random color (method #1)
#     P = Pose(Point(-1,5,0),Quaternion(0,0,0,1))
#     markers.publishCylinder(P, markers.getRandomColor(), 1.0, 0.5, 5.0) # pose, color, height, radius, lifetime

#     # Publish a cylinder of a random color (method #2)
#     P = Pose(Point(0,5,0),Quaternion(0,0,0,1))
#     markers.publishCylinder(P, 'random', 1.0, 0.5, 5.0) # pose, color, height, radius, lifetime


#     # # Model mesh:

#     # # Publish STL mesh of box, colored green
#     # T = transformations.translation_matrix((3,1,0))
#     # scale = Vector3(1.5,1.5,1.5)
#     # mesh_file1 = "package://rviz_tools_py/meshes/box_mesh.stl"
#     # markers.publishMesh(T, mesh_file1, 'lime_green', scale, 5.0) # pose, mesh_file_name, color, mesh_scale, lifetime

#     # # Display STL mesh of bottle, re-scaled to smaller size
#     # P = Pose(Point(4,1,0),Quaternion(0,0,0,1))
#     # scale = Vector3(0.6,0.6,0.6)
#     # mesh_file2 = "package://rviz_tools_py/meshes/fuze_bottle_collision.stl"
#     # markers.publishMesh(P, mesh_file2, 'blue', scale, 5.0) # pose, mesh_file_name, color, mesh_scale, lifetime

#     # # Display collada model with original texture (no coloring)
#     # P = Pose(Point(5,1,0),Quaternion(0,0,0,1))
#     # mesh_file3 = "package://rviz_tools_py/meshes/fuze_bottle_visual.dae"
#     # mesh_scale = 4.0
#     # markers.publishMesh(P, mesh_file3, None, mesh_scale, 5.0) # pose, mesh_file_name, color, mesh_scale, lifetime


#     rospy.Rate(1).sleep() #1 Hz