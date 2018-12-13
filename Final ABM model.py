# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:18:19 2018

@author: Siu Pouvalu, 201205928 
"""
#The following is a set of code for agent based modelling, where an environment
#and agents are created. This model is used to animate the rate of how the 
#invasive crazy yellow ants (agents) move around randomly eating and altering 
#a new ecosystem (environment) they find until the conditions are unfavourable
#and they die (stopping condition).
#The last bit of code, produces a graphic user interface.


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

#The following code creates an environment for the agents (ants) to 
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
#commented out here because in the GUI code, we plot using canvas.show(). So
#it's better to comment it out unless you just want to see whether the above 
#code creates the environment. Once the GUI code is entered you can comment
#it out or delete it but its good to have it here to see whether your code
#is working.
                                    
#matplotlib.pyplot.imshow(environment)
#matplotlib.pyplot.show() 

 
##############################################################################
                        ####### Create agents(Crazy yellow ants) #######
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
                            #agents you can use this code to define the number
                            #of agents. However, we will use the next line
                            #to specify that we will model all of the agents
                            #in the dataset.
num_of_agents = len(td_ys)  #This calls all (length) of the agents in the 
                            #dataset. It could be len(td_ys) or len(td_xs)
                            #because they both have the same length of data
num_of_iterations = 10  #number of times the agents repeat execution of task
neighbourhood = 10      #number of times agents search for other agents and
                        #share resources with them

#print(td_ys)           #These three lines are commented out, not necessary
#print(td_xs)           #to have once you have a complete code but you can
#print (len (td_ys))    #use it to run the code above and see how many agents

fig = matplotlib.pyplot.figure(figsize=(7, 7)) 
ax = fig.add_axes([0, 0, 1, 1])

#agent initialisation loop, connecting agents with environment and y,x data
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework1.Agent(environment, agents, y, x)) 

#specifies how the model will be looped            
carry_on = True                    
             
def update(frame_number):
    global carry_on
    fig.clear()
    
#Create the axes in which the agents will be plotted in. This specifies
#the starting point and end point inwhich agents will move around in.
#The axes is from 0-100 
    
    matplotlib.pyplot.xlim(0, 100) #extent of environment x axes
    matplotlib.pyplot.ylim(0, 100) #extent of environment y axes
   
    
#define the condition in which the agents will stop
    if random.random() <0.003:     #If temperature increases in the environment
        carry_on = False           #by a certain amount, the ants will die
        print("stopping condition") #and the model stops runing.
    
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
#in their location. Agents will also search for nearby agents to share
#their resources.
                    
#Specify agent behaviour, so they move, eat and share in the environment
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)

#Plot the agents in the x,y axes   
     
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)  
 

########################################################################
######## Animating the agents ###############
########################################################################

#The line below can be used to see an animation of the model, with the
#model to check the above codes work.
        
#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1,
                             #repeat=False, frames=num_of_iterations)
                             
def gen_function(b = [0]): #generator function specifying the model to start 
    a = 0                  #running from 0 and carry on if the repeat number 
    global carry_on        #is below 100. It will not go beyond 100.
    while (a < 100) & (carry_on == True) :
        print(a)
        sys.stdout.flush()
        yield a			  #Returns control and waits next call.
        a = a + 1

#The following line allows the animation to run and stops according to
#the specifications of the gen_function specified above. 
        
animation = matplotlib.animation.FuncAnimation(fig, update, 
interval=1, repeat=False, frames=gen_function)


###########################################################################
######### Creating a Graphic User Interface (GUI) #########
###########################################################################
 
#The following code creates a new interface and a menu which can allows a 
#user to click on a menu and run the model 

#define the animation that will run in the new interface.

def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, 
                    frames=gen_function, repeat=False)
    canvas.show() 
     
root = tkinter.Tk() 
root.wm_title("Crazy Yellow Ant invasion")    #model title
menu_bar = tkinter.Menu(root)                 
root.config(menu=menu_bar)                    #menu bar configuration
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
tkinter.mainloop() 

###########################################################################
















