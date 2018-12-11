# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:18:19 2018

@author: Siu Pouvalu, 201205928 
"""
#The following is a set of code for agent based modelling, where an environment
#and agents are created. This could be used to animate how individuals (agents) 
#move around randomly picking fruits and sharing with one another within a 
#field (environment) until their baskets are full (stopping
#condition). The last bit of code, produces a graphic user interface.


##############################################################################
      ####### Import all necessary operators at the top ########
##############################################################################
#Before you can run this model, the following operators and agent framework 
#must be imported at the top of the model. This makes it easier to locate the
#operators and also for Python to know what operators this code uses.

import sys
import csv 
import agentframework1
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation 
import matplotlib.pyplot
import tkinter
import matplotlib.backends.backend_tkagg 
import requests
import bs4
 

##############################################################################
                     ####### Create environment ########
##############################################################################

#The following code creates an environment for the agents (fruit pickers) to 
#interact in. 

environment = [] #empty list to hold data for the 2D environment created below

# "in.text" is a csv file of raster data containing pixel values, each row 
#contains values increasing in the y direction and values that follow
#also increases in the x direction. *Note that this file needs to be saved in 
#the same directory as the framework and model, otherwise code will not run.

f= open("in.txt", newline='')       #command to open text document
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC) #read text file
for row in reader:				     
    rowlist = []                    #Create empty list called 'rowlist' to
    for value in row:				#be filled with values from rows in csv
        #print(value) 				
        rowlist.append(value)       #Adds values in the rows to rowlist
    environment.append(rowlist)     #Adds rowlist to environment, creating a 
                                    #new list for every row and every row
                                    #containing a set of values
                                    
#the lines below will show the environment in a new window, you can remove 
#the # key to run the model and see the full of extent of environment. It is
#commented out here because, in the GUI code, we plot using canvas.show(). So
#it's better to comment it out unless you just want to see whether the above 
#code creates the environment.
                                    
#matplotlib.pyplot.imshow(environment)
#matplotlib.pyplot.show() 

 
##############################################################################
                        ####### Create agents(fruitpickers) #######
##############################################################################
                        
#Create the agents and connect them to the environment that they will 
#interact in. 
                        
agents = []             #an empty list to populate with agent data

#Code to scrape web data containing y, x data to initialise code. 
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

#num_of_agents = 10         #If you only want to use a specific number of 
                            #you can use this code to define the number
                            #of agents. However, we will use the next line
                            #to specify that we will model all of the agents
                            #in the dataset.
num_of_agents = len(td_ys) #This calls all (length) of the agents in the 
                            #dataset. It could be len(td_ys) or len(td_xs)
                            #because they both have the same length of data
num_of_iterations = 10  #number of times the agents repeat execution of task
neighbourhood = 10      #number of times agents search for other agents and
                        #share resources with them

print(td_ys)
print(td_xs)
#print (len (td_ys)) 

fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#agent initialisation loop, connecting agents with environment and y,x data
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework1.Agent(environment, agents, y, x)) 
                  
carry_on = True
#specify how you want your model to be animated                   
def update(frame_number):
    global carry_on
    fig.clear()
    
#Create the axes in which the agents will be plotted in. This specifies
#the starting point and end point inwhich agents will move around in.
#The axes is from 0-299 and the other 0-100. Obviously, one environment,
#is bigger than the other
    
    matplotlib.pyplot.xlim(0, 100) #extent of environment x axes
    matplotlib.pyplot.ylim(0, 100) #extent of environment y axes
   
    
#define the condition in which the agents will stop
    if random.random() <0.003:
        carry_on = False
        print("stopping condition") 
    
#######################################################################
####### Plotting the agents #########
#######################################################################
#The agents are plotted in the environment
        
    matplotlib.pyplot.imshow(environment)
    #for i in range(num_of_agents):
        #matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
 
#######################################################################
####### Agent communication ###########
#######################################################################
#The following commands the agents to move and eat at the same time
#in their location. Agents will also search or know the location of 
#nearby agents to share
                    
#Specify agent behaviour, so they move, eat and share in the environment
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].pickfruits()
        agents[i].share_with_neighbours(neighbourhood)

#Plot the agents in the x,y axes   
     
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)  
 

########################################################################
######## Animating the agents ###############
########################################################################

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1,
                             #repeat=False, frames=num_of_iterations)
                             
def gen_function(b = [0]): #generator function specifying stop condition
    a = 0                  # i.e. 100 times
    global carry_on 
    while (a < 100) & (carry_on == True) :
        print(a)
        sys.stdout.flush()
        yield a			# Returns control and waits next call.
        a = a + 1


#The next command animates the model but will stop when condition is met
#according to the set number of specified frames. Note that you should not run 
#it together with the second line of animation below it. Use one or the other.
                             
#animation = matplotlib.animation.FuncAnimation(fig, update, 
#interval=1, repeat=False, frames=10)

#The following line allows the animation to run and stops according to
#the specifications of the gen_function specified above. Use this line
#because the gen_function will be called in the GUI code. 
        
animation = matplotlib.animation.FuncAnimation(fig, update, 
interval=1, repeat=False, frames=gen_function)

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1)
 
#matplotlib.pyplot.show() ##commented out because it is not used in the GUI

###########################################################################
######### Creating a Graphic User Interface (GUI) #########
###########################################################################
 
#The following code creates a new interface and a menu which can allows a 
#user to click on a menu and run the model 

def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, 
                    frames=gen_function, repeat=False)
    canvas.show() 
     
root = tkinter.Tk() 
root.wm_title("Fruitpicking Model")
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
tkinter.mainloop() 

###########################################################################
















