"""
Author:      Roy Wu
Description: Define a small 10x10 square world, a measurement range that is 
             half that of the world and small values for motion and measurement noise
"""

import matplotlib.pyplot as plt
import robot                       #* custom library
from helpers import display_world  #* custom library

#*----- ----- -----
#*   Define The World And A Robot
#*----- ----- -----
world_size         = 10.0    # size of world (square)
measurement_range  = 5.0     # range at which we can sense landmarks
motion_noise       = 0.2     # noise in robot motion
measurement_noise  = 0.2     # noise in the measurements

#*instantiate a robot, r
r = robot.Robot(world_size, measurement_range, motion_noise, measurement_noise)

#*print out the location of r
print(r)


#*----- ----- -----
#*   Visualize The World
#*----- ----- -----


plt.rcParams["figure.figsize"] = (5,5)  #*define figure size

#* call display_world and display the robot in it's grid world
print(r)
display_world(int(world_size), [r.x, r.y])