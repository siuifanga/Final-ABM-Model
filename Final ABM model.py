
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:18:19 2018

@author: Siu Pouvalu, 201205928 
"""
#The following is a set of code for agent based modelling, where agents and
#an environment are created. The agents interact within the environment
#where they move and eat until a certain condition is met.


#######################################################################
####### Import all necessary functions at the top #########
#######################################################################
import sys
import csv
import agentframework1
import random
import operator
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation 
import matplotlib.pyplot
import tkinter
import matplotlib.backends.backend_tkagg 
import requests
import bs4
 

#Create the environment, and fill it with a list 
#containing values using the calculations that follow

#######################################################################
####### Create environment #########
#######################################################################
environment = []
f= open("in.txt", newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:				# A list of rows
    rowlist = []  
    for value in row:				# A list of value
        #print(value) 				# Floats
        rowlist.append(value)
    environment.append(rowlist) 
#f.close() 	# Don't close until you are done with the reader;
		# the data is read on request.
      
        ##the lines that follow shows the environment in a new window      
#matplotlib.pyplot.imshow(environment)
#matplotlib.pyplot.show()


#######################################################################
####### Make agents #########
#######################################################################
#Make the agents and connect them to the environment
agents = []
num_of_agents = 10
num_of_iterations = 10
neighbourhood = 20

r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys)
print(td_xs)

fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework1.Agent(environment, agents, y, x)) 
                    #this line commands a connection between 
                    #the agents with the environment
carry_on = True
#specify how you want your model to be animated                   
def update(frame_number):
    global carry_on
    fig.clear()
    
#create the axes in which the agents will be plotted in. This specifies
    #the starting point and end point inwhich agents will move around in.
    matplotlib.pyplot.xlim(0, 299)
    matplotlib.pyplot.ylim(299, 0)
    
#define the condition inwhich the animation will stop
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
                    #in their location. Agents will also search or
                    #know the location of nearby agents to share
                    
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
#######################################################################

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1,
                             #repeat=False, frames=num_of_iterations)
                             
def gen_function(b = [0]):
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < 100) & (carry_on == True) :
        print(a)
        sys.stdout.flush()
        yield a			# Returns control and waits next call.
        a = a + 1


#The next command animates the model but will stop when condition is met
        #according to the set number of specified frames. Note that you 
        #should not run it together with the second line of animation below it.
        # Use one or the other.
                             
#animation = matplotlib.animation.FuncAnimation(fig, update, 
#interval=1, repeat=False, frames=10)

##The following line allows the animation to run and stops according to
        ##the specifications of the gen_function specified above. It will
        ##never run above 100
        
animation = matplotlib.animation.FuncAnimation(fig, update, 
interval=1, repeat=False, frames=gen_function)

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1)

#matplotlib.pyplot.show() 
 
###########################################################################

 
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
root.wm_title("ABM Model")
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
tkinter.mainloop() 


#############################################################################
