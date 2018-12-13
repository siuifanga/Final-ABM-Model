# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:18:19 2018

@author: Siu Pouvalu, 201205928
"""
########################################################################
               ########### Create agent class  ##########
########################################################################
             
import random 

#Create an agent class which is basically the blueprint for the agents and
#their behaviour
class Agent(): 
#Create a function that can be called from the objects or agents
   
    def __init__(self, environment, agents,y,x): #this gives each agent access                                        
        self.environment = environment;         ##to the env and other agents
        self.agents = agents                     #defines the agents
        self.x = x                               #random.randint (0,100)
        self.y = y                               #random.randint (0,100)
        self.store = 0                     #each agent starts with 0 or nothing
        pass                                     ##keyword that only compiles 
                                                 #the clauses above                                  
     
###########################################################################
    ########### Define functions and agent behaviour ##########
###########################################################################       
    
#Define functions or agent behaviour i.e. eat, move and share with other
                                                 #agents
                                                 
    def eat(self): 
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
            
#
    def share_with_neighbours(self, neighbourhood):
        for agent in self.agents:
            dist = self.distance_between(agent) 
        if dist <= neighbourhood:
            total = self.store + agent.store
            ave = total /2
            self.store = ave
            agent.store = ave
            #print("sharing " + str(dist) + " " + str(ave))
            
#Calculate the distance between agents
    def distance_between(self, agent):
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
        
            
        
  

 