"""
Author:      Roy Wu
Description: SLAM
"""
import numpy   as np


#*----- ----- -----
#*    This function takes in a number of time steps N, number of landmarks, 
#*    and a world_size, it returns initialized constraint matrices, omega and xi
#*----- ----- -----
def initialize_constraints(N, num_ldmk, world_size):
    #* Define and store the size (rows/cols) 
    rows = 2* (N + num_ldmk)
    cols = 2* (N + num_ldmk)
    #print(rows)
    #print(cols)
    
    #* Define the constraint matrix, Omega, with two initial "strength" values
    omega = np.zeros((rows, cols))
    #* initial x, y location of our robot
    omega[0][0] = 1. 
    omega[1][1] = 1.
    
    #* Define the constraint *vector*, xi
    #* Assume the robot starts out in the middle of the world with 100% confidence
    
    #xi = [ rows, 1]
    xi = np.zeros((rows, 1))
    xi[0][0] = world_size / 2.
    xi[1][0] = world_size / 2.
    
    return omega, xi


#*----- ----- -----
##    slam takes in 6 arguments and returns mu, 
#*----- ----- -----
def slam(data, N, num_ldmk, world_size, motion_noise, meas_noise):
    
    
    omega, xi = initialize_constraints(N, num_ldmk, world_size)
    
    #* Iterate through each time step in the data
    #* get all the motion and measurement data as you iterate
    p= len(data)
    for i in range(p):
        measurements = data[i][0]
        motion = data[i][1]
        dx = motion[0]
        dy = motion[1]
        mweight = 1.0 / motion_noise
        nweight = 1.0 / meas_noise
        # print('\nmweight is...', mweight)
        # print('nweight is...', nweight)
    
        #* even number colus of Omega corresponds to x values
        x0 = 2*i    #* 0, 2, 4, 6, ...
        x1 = 2*i+2  #* 2, 4, 6, 8,...
        
        #* odd number colus of Omega corresponds to y values
        y0 = 2*i +1  #* 1, 3, 5, 7, ...
        y1 = 2*i +3  #* 3, 5, 7, 9,...        
        
        for m in measurements:
            landmark = m[0]  #*landmark ID
            dxM = m[1]
            dyM=  m[2]
            
            x0L = (2*N) +(landmark*2) #* even-numbered columns have x values of landmarks
            y0L = x0L+1               #* odd-numbered columns have y values of landmarks
            
            #*for x value
            omega[x0,  x0]  += nweight   #x,y
            omega[x0,  x0L] += -nweight  # x, y+landmark
            omega[x0L, x0]  += -nweight  #x+ landmark,y
            omega[x0L, x0L] += nweight   # x+landmark,y+landmark

            # for y value
            omega[y0,  y0]  += nweight  # x,y
            omega[y0,  y0L] += -nweight # x, y+landmark
            omega[y0L, y0]  += -nweight # x+landmark, y
            omega[y0L, y0L] += nweight  # x+landmark, y+landmark  
            
            xi[x0,  0] += -dxM *nweight  #vector update 1
            xi[x0L, 0] += dxM *nweight   #vector update 2
            xi[y0,  0] += -dyM *nweight  #vector update 1
            xi[y0L, 0] += dyM *nweight   #vector update 2   

        
     ## TODO: update the constraint matrix/vector to account for all *motion* and motion noise       
     #now for dx value  
        omega[x0, x0] +=  mweight
        omega[x0, x1] += - mweight
        omega[x1, x0] += - mweight
        omega[x1, x1] +=  mweight
        
     # for dy value  
        omega[y0, y0] +=  mweight
        omega[y0, y1] += - mweight
        omega[y1, y0] += - mweight
        omega[y1, y1] +=  mweight 
        
        xi[x0, 0] += -dx * mweight #vector update 1
        xi[x1, 0] += dx * mweight  #vector update 2 
        xi[y0, 0] += -dy * mweight    #vector update 1
        xi[y1, 0] += dy * mweight    #vector update 2 

    
       
    #* After iterating through all the data
    #* Compute the best estimate of poses and landmark positions
    omega_inv = np.linalg.inv(omega)
    mu=np.matmul(omega_inv, xi)
    
    
    with open('omega.txt', 'w') as f:
        for item in omega:
            f.write("%s\n" % item)
    
    return mu 