# part of SierpinskiTriangle
# SierpinskiTriangleExplorer.py
# 1/22/2017
#
# contains class definition for a sample App

# import statements for all of the graphics libraries
# there is a distinction between python 2 and python 3
# in terms of what they call the Tkinter library
try:
    import Tkinter as tk
    import ttk
except ImportError: #for python 3.3
    import tkinter as tk
    from tkinter import ttk

# (R)ushy (P)anchal modified Zelle's graphics library
# to support GraphWins within frames
from pkg.RP_graphics import *

# utilities as needed
from math import *
import random

# change the name of 'SierpinskiTriangleExplorerApp' as necessary
class SierpinskiTriangleExplorerApp:
    
    # constructor for App class, which implements an App to
    # explore equations of the form Y = MX + B
    def __init__(self, master):
        self.master = master

        #*************************************************************
        # LinearEquationExplorerApp INSTANCE FIELDS          
        
        #1. list of Points
        self.points = [Point(0,0), Point(0,0), Point(0,0)]

        #2. Number of iterations
        self.numIters = 1000
        self.numItersScaleVar = tk.DoubleVar() # Should be IntVal
        
        #3. default window settings for graph window &
        #   storage of current window settings
        self.defaultCoords = (-20, -20, 20, 20)
        self.minX = self.defaultCoords[0]
        self.minY = self.defaultCoords[1]
        self.maxX = self.defaultCoords[2]
        self.maxY = self.defaultCoords[3]

        #*************************************************************
        # the main frames for this program

        # 1. the outer, container frame of the entire thing
        self.frame = tk.Frame(self.master, background = 'black')

        # 2. the plot window will go inside of drawFrame
        self.drawFrame = tk.Frame(self.frame)
        self.drawFrame.grid(row = 1, column = 10, padx = 5, pady = 5)

        # 3. the frame to hold the controls (buttons, sliders, etc.)
        self.controlFrame = tk.Frame(self.frame, bg = 'black')
        self.controlFrame.grid(row = 1, column = 50, padx = 10, pady = [10,100], sticky = tk.N + tk.S)

        #*************************************************************
        # setting up graph window
        self.graph = GraphWin(self.drawFrame, 620, 620, autoflush = False)
        self.graph.grid(row = 1, column = 1)
        self.graph.setBackground('black')
        self.graph.setCoords(self.defaultCoords[0], self.defaultCoords[1], self.defaultCoords[2], self.defaultCoords[3])

        #*************************************************************
        # setting up controls in control frame
        #1. label
        self.controlLabel = tk.Label(self.controlFrame, text = "INPUTS FOR Myster Program", fg = 'white', bg = 'black')
        self.controlLabel.grid(row = 10, column = 1, columnspan = 1, padx = 5, pady = 15)

        #2. NUMITERS scroll
        self.numItersScroll = tk.Scale(self.controlFrame, from_ = 0, to = 10000, tickinterval = 5000)
        self.numItersScroll.configure(label = "Number of Iterations", orient = tk.HORIZONTAL)
        self.numItersScroll.configure(bg = 'black', fg = 'white', troughcolor = 'white', activebackground = 'black')
        self.numItersScroll.configure(variable = self.numItersScaleVar)
        self.numItersScroll.grid(row = 20, column = 1, columnspan = 1, padx = 5, pady = 5, sticky = tk.W + tk.E)
        
        #3. new frame for DRAW & CLEAR & ZOOM buttons
        self.drawclearFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.drawclearFrame.configure(text = "control buttons")
        self.drawclearFrame.grid(row = 70, column = 1, padx = 0, pady = 5, sticky = tk.N + tk.S)

        #3a. DRAW button
        self.drawLineButton = ttk.Button(self.drawclearFrame, text = "DRAW", command = lambda: self.acceptInputs())
        self.drawLineButton.grid(row = 1, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        #3b. CLEAR button
        self.clearButton = ttk.Button(self.drawclearFrame, text = "CLEAR", command = lambda: self.erase())
        self.clearButton.grid(row = 1, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        #4. INSTRUCTIONS label
        instructions = "In order to use this program,\nclick draw to start,\nthen click three points\nto generate a triangle."
        self.instructLabel = tk.Label(self.controlFrame, text = instructions, fg = 'white', bg = 'black')
        self.instructLabel.grid(row = 100, column = 1)

        # initialize scale widgets to corresponding initial parameter values
        self.numItersScroll.set(self.numIters)
        self.frame.pack()

    def acceptInputs(self):
        self.numIters = int(self.numItersScaleVar.get())
        self.erase()
        self.process(self.points, self.numIters, self.graph)

    def process(self, points, numIters, win):
        # Ask the user to plot three points
        print("Click to set Point A")
        points[0] = win.getMouse()
        win.plot(points[0].getX(), points[0].getY(), 'red')
        
        print("Click to set Point B")
        points[1] = win.getMouse()
        win.plot(points[1].getX(), points[1].getY(), 'red')
        
        print("Click to set Point C")
        points[2] = win.getMouse()
        win.plot(points[2].getX(), points[2].getY(), 'red')

        # Select a random Point Z
        Z = Point(random.uniform(-20,20), random.uniform(-20,20))

        # For the number of iterations...
        for i in range(numIters):
            # Select randomly one of the three points
            ranPoint = points[random.randint(0,2)]

            # Calculate the halfway point between Z and the selected Point
            deltaX = abs(Z.getX() - ranPoint.getX()) / 2
            deltaY = abs(Z.getY() - ranPoint.getY()) / 2

            if(Z.getX() > ranPoint.getX()):
                coordX = Z.getX() - deltaX
            else:
                coordX = Z.getX() + deltaX

            if(Z.getY() > ranPoint.getY()):
                coordY = Z.getY() - deltaY
            else:
                coordY = Z.getY() + deltaY

            # Plot the new point and set it as Point Z
            win.plot(coordX, coordY, 'green')
            Z = Point(coordX, coordY)

    def erase(self):
        self.graph.clear()

    def shutDown(self):
        self.root.quit()



