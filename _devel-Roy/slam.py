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
    
            
        #* update the constraint matrix/vector to account for all *measurements*
        #* this should be a series of additions that take into account the measurement noise
        nweight = 1 / meas_noise
        
        for m in measurements:
            landmark = m[0]
            x = m[1]
            y=  m[2]
            
            #*for x value
            omega[2*i, 2*i] += nweight    #x,y
            
            omega[2*i, 2*N + 2*landmark] += -nweight   # x, y+landmark
        
            omega[2*N + 2*landmark, 2*i] += -nweight    #x+ landmark,y
        
            omega[2*N + 2*landmark, 2*N + 2*landmark] += nweight  # x+landmark,y+landmark

            xi[2*i, 0] += -x *nweight  #vector update 1
        
            xi[2*N + 2*landmark, 0] += x *nweight  #vector update 2

            # for y value
            omega[2*i+1, 2*i+1] += nweight  #x,y
        
            omega[2*i+1, 2*N + 2*landmark+1] += -nweight # x, y+landmark
        
            omega[2*N+2*landmark+1, 2*i+1] += -nweight #x+landmark, y
        
            omega[2*N+2*landmark+1, 2*N+2*landmark+1] += nweight  # x+landmark, y+landmark  

            xi[2*i + 1, 0] += -y *nweight  #vector update 1
        
            xi[2*N + 2*landmark + 1, 0] += y *nweight   #vector update 2   
        
     ## TODO: update the constraint matrix/vector to account for all *motion* and motion noise       
        dx = motion[0]             
        dy = motion[1]
        mweight = 1 / motion_noise
        
     #now for dx value  
    
        omega[2*i, 2*i] +=  mweight
        
        omega[2*i, 2*i+2] += - mweight
        omega[2*i+2, 2*i] += - mweight
        
        omega[2*i+2, 2*i+2] +=  mweight
        
        xi[2*i, 0] += -dx  *mweight     #vector update 1
        
        xi[2* +2, 0] += dx * mweight  #vector update 2 
        
 # for dy value  

        omega[2*i+1, 2*i+1] +=  mweight
        
        omega[2*i+1, 2*i+3] += - mweight
        
        omega[2*i+3, 2*i+1] += - mweight
        
        omega[2*i+3, 2*i+3] +=  mweight 
        

        xi[2*i+1, 0] += -dy * mweight    #vector update 1
        xi[2*i+3, 0] += dy * mweight    #vector update 2 
    
       
    #* After iterating through all the data
    #* Compute the best estimate of poses and landmark positions
    omega_inv = np.linalg.inv(np.matrix(omega))
    mu = omega_inv*xi
    
    
    with open('omega.txt', 'w') as f:
        for item in omega:
            f.write("%s\n" % item)
    
    return mu 