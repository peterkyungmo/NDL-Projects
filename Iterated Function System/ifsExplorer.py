# ifsExplorer.py
# v 1.0
# Peter Kang
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

class ifsExplorerApp:

    # constructor for App class, which implements an App to
    # explore equations of the form Y = MX + B
    def __init__(self, master):
        self.master = master

        #*************************************************************
        # ifsExplorerApp INSTANCE FIELDS

        #1. Parameters
        self.T_list = []
        self.currentTrans = '0.5, 0.5, 0, 0, 0, 0'
        self.trans_string = tk.StringVar()

        #2. starting point
        self.x = random.uniform(0, 1)
        self.y = random.uniform(0, 1)
        self.currentPoint = Point(self.x, self.y)

        #3. number of transformations
        self.numTrans = 10000
        self.numTransScaleVar = tk.IntVar() # Make sure it gets outputed as an int later in the selection

        #3. color list
        self.colors = ['red', 'blue', 'green', 'yellow', 'white', 'navy', 'pink', 'brown', 'gray', 'cyan',
                      'magenta', 'gold', 'tan', 'orange']

        #4. default window settings for graph window &
        #   storage of current window settings
        self.defaultCoords = (-1, -1, 1, 1)
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
        self.controlLabel = tk.Label(self.controlFrame, text = "INPUTS FOR ifsExplorer", fg = 'white', bg = 'black')
        self.controlLabel.grid(row = 10, column = 1, columnspan = 1, padx = 5, pady = 15)

        #2. numTrans Scroll
        self.numTransScroll = tk.Scale(self.controlFrame, from_ = 10000, to = 100000, tickinterval = 90000, resolution = 10000)
        self.numTransScroll.configure(label = "Number of Iterations", orient = tk.HORIZONTAL)
        self.numTransScroll.configure(bg = 'black', fg = 'white', troughcolor = 'white', activebackground = 'white')
        self.numTransScroll.configure(variable = self.numTransScaleVar)
        self.numTransScroll.grid(row = 20, column = 1, columnspan = 1, padx = 0, pady = (5,0), sticky = tk.W + tk.E)

        #3. transformations listbox
        self.lb = tk.Listbox(self.controlFrame, height = 8)
        self.lb.grid(row = 30, column = 1, columnspan = 1, padx = 0, pady = (2,0), sticky = tk.W + tk.E)

        #3b. listbox label
        self.lbLabel = tk.Label(self.controlFrame, text = "Transformation Selection", fg = 'white', bg = 'black')
        self.lbLabel.grid(row = 25, column = 1, columnspan = 1, padx = 0, pady = 0)

        #4. Transformation Input
        self.transEntry = ttk.Entry(self.controlFrame)
        self.transEntry.configure(textvariable = self.trans_string)
        self.transEntry.grid(row = 60, column = 1, columnspan = 1, padx = 0, pady = (2,0), sticky = tk.W + tk.E)

        #4b. Input label
        self.lbLabel = tk.Label(self.controlFrame, text = "T-Input (comma deliminated\nEX. '0.5,0.5,0,0,0,0'", fg = 'white', bg = 'black')
        self.lbLabel.grid(row = 55, column = 1, columnspan = 1, padx = 0, pady = 0)
        
        #4. new frame for ADD & EDIT & REMOVE & DISPLAY & CLEAR buttons
        self.buttonFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.buttonFrame.configure(text = "control buttons")
        self.buttonFrame.grid(row = 70, column = 1, padx = 0, pady = 5, sticky = tk.N + tk.S)

        #5a. ADD button
        self.addButton = ttk.Button(self.buttonFrame, text = "ADD", command = lambda: self.addTrans(self.lb))
        self.addButton.grid(row = 1, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)
        
        #5b. EDIT button
        self.editButton = ttk.Button(self.buttonFrame, text = "EDIT", command = lambda: self.editTrans(self.lb))
        self.editButton.grid(row = 1, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        #5c. REMOVE button
        self.removeButton = ttk.Button(self.buttonFrame, text = "REMOVE", command = lambda: self.removeTrans(self.lb))
        self.removeButton.grid(row = 2, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        #5d. DISPLAY button
        self.editButton = ttk.Button(self.buttonFrame, text = "DISPLAY", command = lambda: self.iterate())
        self.editButton.grid(row = 2, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        #5e. CLEAR button
        self.clearButton = ttk.Button(self.buttonFrame, text = "CLEAR", command = lambda: self.graph.clear())
        self.clearButton.grid(row = 3, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        #6. INSTRUCTIONS label
        instructions = "You can type a transformation in the form,\n(r, s, theta, phi, e, f).\n You can also manipulate the list of\ntransformations by selecting the\ntransformations in the selection box."
        self.instructionLabel = tk.Label(self.controlFrame, text = instructions, fg = 'white', bg = 'black')
        self.instructionLabel.grid(row = 100, column = 1)
        
        # Initilaize widgets
        self.frame.pack()

    #*************************************************************
    # Button Functions
    def addTrans(self, lb):
        # Transformation String conversion to a list
        trans = self.trans_string.get().split(',')
        trans_value = []
        for value in trans:
            trans_value.append(float(value))
        
        # Append the list to T_list
        self.T_list.append(trans_value)

        # Add transformation to the listbox
        lb.insert(len(self.T_list) - 1, self.trans_string.get())

    def editTrans(self, lb):
        # get the index of the listbox item
        index = lb.index('active')

        # get the current transformation from the entry
        trans = self.trans_string.get().split(',')
        trans_value = []
        for value in trans:
            trans_value.append(float(value))

        # Change the transformation value at that index
        self.T_list[index] = trans_value

        # Change the transformation in the listbox
        lb.delete(index)
        lb.insert(index, self.trans_string.get())

        print(self.T_list)  #Debug

    def removeTrans(self, lb):
        # get the index of the listbox item
        index = lb.index('active')

        # remove the transformation from T_list and the listbox
        del self.T_list[index]
        lb.delete(index)

        print(self.T_list) #Debug
        
    #*************************************************************
    # IFS Functions
    def iterate(self):
        """ Iterates a point using randomly selected transformations in a list of transformations """

        numIters = int(self.numTransScaleVar.get())
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        point = Point(x, y)
        
        # iterate 'numIters' times...
        for i in range(numIters):
            
            # Pick a random transformation
            c = random.randint(0, len(self.T_list) - 1)

            # Transform point using selected transformation
            newPoint = self.T(point, self.T_list[c])

            # Plot the new point
            self.graph.plot(newPoint.getX(), newPoint.getY(), self.colors[c])

            # set current point to newPoint
            point = newPoint

    def T(self, point, trans):
        """ Takes Point object 'point' and transforms it using 'trans' """
        
        # Get transformation values
        r = trans[0]
        s = trans[1]
        theta = trans[2] * 0.01745329251
        phi = trans[3] * 0.01745329251
        e = trans[4]
        f = trans[5]

        # Transform points using transformation values
        x0 = point.getX()
        y0 = point.getY()
        x = (r * cos(theta) * x0) - (s * sin(phi) * y0) + e
        y = (r * sin(theta) * x0) + (s * cos(phi) * y0) + f
        
        # Return transformed point
        return Point(x, y)
    
        

    
        








        
