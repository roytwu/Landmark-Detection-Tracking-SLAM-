"""
Author:   Roy Wu
Description: main program for graphSLAM
"""
#* custom library
# import robot
import slam
import helpers 

#*----- ----- -----
#*   Define parameters
#*----- ----- -----
world_size         = 50.0 #* size of world (square)
measurement_range  = 25.0 #* range at which we can sense landmarks
motion_noise       = 1.3  #* noise in robot motion
measurement_noise  = 1.3  #* noise in the measurements
N                  = 5
distance           = 3.0
num_landmarks      = 3    #* purple x in the grid world
#*----- ----- -----
#*   Visualize The World
#*----- ----- -----
# plt.rcParams["figure.figsize"] = (100, 100)  #*define figure size


#*----- ----- -----
#*   SLAM
#*----- ----- -----

#* create simulation data
data = helpers.make_data(N, num_landmarks, world_size, measurement_range, 
                         motion_noise, measurement_noise, distance)

#* perform slam
mu = slam.slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)


#*----- ----- -----
#*   print out the resulting landmarks and poses
#*----- ----- -----
if(mu is not None):
    #* print out the lists of poses and landmarks
    poses, landmarks = helpers.get_poses_landmarks(mu, N, num_landmarks)
    helpers.print_all(poses, landmarks)

# print(mu)
# print(mu.size)