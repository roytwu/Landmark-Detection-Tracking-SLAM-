"""
Author:      Roy Wu
Description: Define a small 10x10 square world, a measurement range that is 
             half that of the world and small values for motion and measurement noise
"""
import matplotlib.pyplot as plt
import numpy             as np

#* custom library
import robot
import slam
import helpers 
from helpers import display_world  

#*----- ----- -----
#*   Define The World And A Robot
#*----- ----- -----
world_size         = 10.0       # size of world (square)
measurement_range  = 5.0        # range at which we can sense landmarks
motion_noise       = 0.0000001  # noise in robot motion
measurement_noise  = 0.0000001  # noise in the measurements

#*instantiate a robot, r
r = robot.Robot(world_size, measurement_range, motion_noise, measurement_noise)
print(r)  #* print out the location of r


#*----- ----- -----
#*   Visualize The World
#*----- ----- -----
plt.rcParams["figure.figsize"] = (10, 10)  #*define figure size

#* move
dx = 1
dy = 2
r.move(dx, dy)

#* call display_world and display the robot in it's grid world
display_world(int(world_size), [r.x, r.y])


#*----- ----- -----
#*   Create Landmark
#*----- ----- -----
#* create any number of landmarks 
#* Each landmark is displayed as a purple x in the grid world
num_landmarks = 3
# r.make_landmarks(num_landmarks)

#* display the world including these landmarks
display_world(int(world_size), [r.x, r.y], r.landmarks)

# measurements = r.sense()
# data = []

# #* after a robot first senses, then moves (one time step)
# #* that data is appended like so:
# data.append([measurements, [dx, dy]])

# #* for our example movement and measurement
# print(data)

# time_step = 0
# print('Motion: ', data[time_step][1])
N=6
distance = 1
data = helpers.make_data(N, num_landmarks, world_size, measurement_range, 
                         motion_noise, measurement_noise, distance)

mu = slam.slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)

print(mu)
print(mu.size)




