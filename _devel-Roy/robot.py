"""
Author:      Roy Wu
Description: creates a mobile robot for SLAM
"""
import numpy as np
import random

#* the Robot class
class Robot:
    #*-------- 
    #*   creates a robot with the specified parameters and initializes 
    #*   the location (self.x, self.y) to the center of the world
    #*-------- 
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        self.world_size = world_size
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.meas_noise = measurement_noise
        self.meas_range = measurement_range
        self.landmarks = []
        self.num_LDMK = 0
    
    #*--------     
    #*   returns a positive, random float
    #*-------- 
    def rand(self):
        value = random.random() * 2.0 - 1.0      
        # value =(random.random()*2.0-1.0)*0.1  
        return value   
    
    #*-------- 
    #*   Attempts to move robot by dx, dy. 
    #*   If outside world boundary, then do nothing and returns failure
    #*-------- 
    def move(self, dx, dy):
        # print ('\nmove is called.....')
        print('x is move() is', self.x)
        noise = self.rand() * self.motion_noise
        # noise=0
        # print ('\n noise in Movee function is.....', noise)
        x = self.x + dx + noise
        y = self.y + dy + noise
        # print('x is move() is', x)
        
        # print ('\nmotion noise is...', self.motion_noise)
        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True
 
       
    #*-------- 
    #*   Sense the environment (landmarks)
    #*   (take no argument)
    #*--------     
    def sense(self): 
        measurements = []
        noise = self.rand() * self.meas_noise
        # noise = 0
        for index, landmark in enumerate(self.landmarks):
            # dx = self.x - landmark[0] + noise
            # dy = self.y - landmark[1] + noise
            dx = landmark[0] - self.x  + noise
            dy = landmark[1] - self.y  + noise
            if (self.meas_range==-1) or ( (abs(dx)<=self.meas_range)and(abs(dy)<=self.meas_range) ):
                measurements.append([index, dx, dy])
        # print ('\nmeasurement noise is...', self.meas_noise)        
        return measurements
    

    
    #*-------- 
    #     make random landmarks located in the world
    #*-------- 
    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
            # ldmkCoor = []
            # ldmkCoor.append([round(random.random() * self.world_size),
            #                  round(random.random() * self.world_size)])
        self.num_LDMK = num_landmarks
        
        
        with open('LDMKcoordinate.txt', 'w') as f:
            for item in self.landmarks:
                f.write("%s\n" % item)
      
        # return ldmkCoor

    
    #*-------- 
    #    called when print(robot) is called; prints the robot's location
    #*-------- 
    def __repr__(self):
        return 'Robot loation [x=%.5f y=%.5f]'  % (self.x, self.y)    
    
    
    