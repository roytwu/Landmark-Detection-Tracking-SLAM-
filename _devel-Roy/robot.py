"""
Author:      Roy Wu
Description: creates a robot with the specified parameters and initializes 
             the location (self.x, self.y) to the center of the world
"""
import numpy as np
import random
#matplotlib inline


#* the Robot class
class Robot:
    #*-------- 
    #*   creates a robot with the specified parameters and initializes 
    #*   the location (self.x, self.y) to the center of the world
    #*-------- 
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        self.meas_noise = 0.0
        self.world_size = world_size
        self.meas_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.meas_noise = measurement_noise
        self.landmarks = []
        self.num_LDMK = 0
    
    #*--------     
    #*   returns a positive, random float
    #*-------- 
    def rand(self):
        return random.random() * 2.0 - 1.0        

    
    #*-------- 
    #*   attempts to move robot by dx, dy. If outside world boundary,
    #*   then the move does nothing and instead returns failure
    #*-------- 
    def move(self, dx, dy):

        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True
 
       
    #*-------- 
    #*   Sense the environment (landmarks)
    #*  
    #*--------     
    def sense(self): 
        measurements = []
        
        for index, landmark in enumerate(self.landmarks):
            dx = self.x - landmark[0] + self.rand()*self.meas_noise
            dy = self.y - landmark[1] + self.rand()*self.meas_noise
            if (self.meas_range==-1) or ( (abs(dx)<=self.meas_range)and(abs(dy)<=self.meas_range) ):
                measurements.append([index, dx, dy])
        return measurements
    

    
    #*-------- 
    #     make random landmarks located in the world
    #*-------- 
    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_LDMK = num_landmarks
    

    
    #*-------- 
    #    called when print(robot) is called; prints the robot's location
    #*-------- 
    def __repr__(self):
        return 'Robot: [x=%.5f y=%.5f]'  % (self.x, self.y)    
    
    
    