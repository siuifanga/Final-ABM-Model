# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:18:19 2018

@author: Siu Pouvalu, 201205928
"""

#import random
import random 

 
  

#define the agent class
class Agent(): 
#defining the function 
    #def __init__(self):
    def __init__(self, environment, agents,y,x): #this gives each agent access                                        
        self.environment = environment;         #to the env and other agents
        self.agents = agents #this defines the agents
        self.x = x #random.randint (0,299)
        self.y = y #random.randint (0,299)
        self.store = 0 #what each agent starts off with, nothing.
        pass 
     
#######################################################################
        
    
#Create a method to move agents
    def eat(self): # can you make it eat what is left?
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        
    def move (self):
        if random.random() < 0.5:
            self.x = (self.x + 1) % 300
        else:
            self.x = (self.x - 1) % 300

        if random.random() < 0.5:
            self.y = (self.y + 1) % 300
        else:
            self.y = (self.y - 1) % 300
            

    def share_with_neighbours(self, neighbourhood):
        for agent in self.agents:
            dist = self.distance_between(agent) 
        if dist <= neighbourhood:
            total = self.store + agent.store
            ave = total /2
            self.store = ave
            agent.store = ave
            #print("sharing " + str(dist) + " " + str(ave))

    def distance_between(self, agent):
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
        
            
        


 