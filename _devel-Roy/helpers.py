"""
Author:      Roy Wu
Description: host several helper programs
"""
from robot import Robot
from math import *
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#*--------
#*    Displays the world that a robot is in
#*    Assume the world is a square grid of some given size
#*    landmarks is a list of landmark positions (optional argument)
#*--------
def display_world(world_size, position, landmarks=None):
    
    # using seaborn, set background grid to gray
    sns.set_style("dark")

    # Plot grid of values
    world_grid = np.zeros((world_size+1, world_size+1))

    # Set minor axes in between the labels
    ax=plt.gca()
    cols = world_size+1
    rows = world_size+1

    ax.set_xticks([x for x in range(1,cols)],minor=True )
    ax.set_yticks([y for y in range(1,rows)],minor=True)
    
    #* Plot grid on minor axes in gray (width = 1)
    plt.grid(which='minor',ls='-',lw=1, color='white')
    
    #* Plot grid on major axes in larger width
    plt.grid(which='major',ls='-',lw=2, color='white')
    
    #* Create an 'o' character that represents the robot
    # ha = horizontal alignment, va = vertical
    ax.text(position[0], position[1], 'o', ha='center', va='center', color='r', fontsize=30)
    
    #* Draw landmarks if they exists
    if(landmarks is not None):
        #* loop through all path indices and draw a dot (unless it's at the car's location)
        for pos in landmarks:
            if(pos != position):
                ax.text(pos[0], pos[1], 'x', ha='center', va='center', color='purple', fontsize=20)
    
    #* Display final result
    plt.show()

#*--------
#* check data
#*--------
def check_for_data(num_LDMK, world_size, meas_range, motion_noise, meas_noise):
    # make robot and landmarks
    r = Robot(world_size, meas_range, motion_noise, meas_noise)
    r.make_landmarks(num_LDMK)
    
    
    # check that sense has been implemented/data has been made
    test_Z = r.sense()
    if(test_Z is None):
        raise ValueError
    
    
#*--------
#*    this routine makes the robot data
#*    the data is a list of measurements and movements: [measurements, [dx, dy]]
#*    collected over a specified number of time steps, N
#*--------
def make_data(N, num_LDMK, world_size, meas_range, motion_noise, meas_noise, distance):

    #* check that data has been made
    try:
        check_for_data(num_LDMK, world_size, meas_range, motion_noise, meas_noise)
    except ValueError:
        print('Error: You must implement the sense function in robot_class.py.')
        return []
    
    complete = False
    
    r = Robot(world_size, meas_range, motion_noise, meas_noise)
    r.make_landmarks(num_LDMK)
    
    #* display the world including these landmarks
    display_world(int(world_size), [r.x, r.y], r.landmarks)

    while not complete:
        data = []
        seen = [False for row in range(num_LDMK)]
    
        #* guess an initial motion
        orientation = random.random() * 2.0 * np.pi
        dx = np.cos(orientation) * distance
        dy = np.sin(orientation) * distance
            
        for k in range(N-1):
            #* collect sensor measurements in a list, Z
            Z = r.sense()

            # check off all landmarks that were observed 
            for i in range(len(Z)):
                seen[Z[i][0]] = True
                
            #* move
            while not r.move(dx, dy):
                #* if we'd be leaving the robot world, pick instead a new direction
                # print ('\n while not is called.....')
                orientation = random.random() * 2.0 * np.pi
                dx = np.cos(orientation) * distance
                dy = np.sin(orientation) * distance

            #* collect/memorize all sensor and motion data
            data.append([Z, [dx, dy]])
            
            # #* display the world including these landmarks
            # display_world(int(world_size), [r.x, r.y], r.landmarks)

        #* we are done when all landmarks were observed; otherwise re-run
        complete = (sum(seen) == num_LDMK)

    print(' ')
    print('Landmark locations ', r.landmarks)
    print(r)


    return data


#*--------
#*    Creates a list of poses and of landmarks for ease of printing
#*    this only works for the suggested constraint architecture of interlaced x,y poses
#*--------
def get_poses_landmarks(mu, N, numLDMK):
    # create a list of poses
    poses = []
    for i in range(N):
        poses.append((mu[2*i].item(), mu[2*i+1].item()))

    # create a list of landmarks
    landmarks = []
    for i in range(numLDMK):
        landmarks.append((mu[2*(N+i)].item(), mu[2*(N+i)+1].item()))

    # return completed lists
    return poses, landmarks

#*--------
#*    print data
#*--------
def print_all(poses, landmarks):
    print('\n')
    print('Estimated Poses:')
    for i in range(len(poses)):
        print('['+', '.join('%.3f'%p for p in poses[i])+']')
    print('\n')
    print('Estimated Landmarks:')
    for i in range(len(landmarks)):
        print('['+', '.join('%.3f'%l for l in landmarks[i])+']')