import matplotlib.pyplot as plt
import numpy             as np

#* custom library
# import robot
import slam
import helpers 

#*----- ----- -----
#*   Define The World
#*----- ----- -----
world_size         = 50.0       # size of world (square)
measurement_range  = 25.0        # range at which we can sense landmarks
motion_noise       = 1.3  # noise in robot motion
measurement_noise  = 1.3  # noise in the measurements

#*----- ----- -----
#*   Visualize The World
#*----- ----- -----
# plt.rcParams["figure.figsize"] = (100, 100)  #*define figure size

#*----- ----- -----
#*   Create Landmark
#*----- ----- -----
#* create any number of landmarks 
#* Each landmark is displayed as a purple x in the grid world
num_landmarks = 3
# r.make_landmarks(num_landmarks)


N=5
distance = 3.0
data = helpers.make_data(N, num_landmarks, world_size, measurement_range, 
                         motion_noise, measurement_noise, distance)

mu = slam.slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)

# print out the resulting landmarks and poses
if(mu is not None):
    # get the lists of poses and landmarks
    # and print them out
    poses, landmarks = helpers.get_poses_landmarks(mu, N, num_landmarks)
    helpers.print_all(poses, landmarks)

# print(mu)
# print(mu.size)