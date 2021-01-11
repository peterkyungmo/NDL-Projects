# FractalTree.py
# v 1.4
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

# change the name of 'FractalTreeApp' as necessary
class FractalTreeApp:
    
    # constructor for App class, which implements an App to
    # explore equations of the form Y = MX + B
    def __init__(self, master):
        self.master = master

        #*************************************************************
        # FractalTreeApp INSTANCE FIELDS

        # a. other
        global lines
        self.lines = list()

        global mode
        self.mode = 0
        self.modeVar = tk.IntVar()

        global roots
        self.roots = list()

        # 2a. Branch Angle
        self.branchAngle = 30
        self.baScaleVar = tk.DoubleVar()

        # 2b. Scale Factor
        self.scaleFactor = 0.5
        self.sfScaleVar = tk.DoubleVar()

        # 2c. Level
        self.level = 4
        self.lvlScaleVar = tk.IntVar() # Make sure it gets outputed as an int later in the selection

        # 2d. Angle Variation
        self.angleVariation = 0
        self.avScaleVar = tk.DoubleVar()

        # 2e. Forest Density
        self.forestDensity = 10
        self.fdScaleVar = tk.IntVar()

        # 3. default window settings for graph window &
        #    storage of current window settings
        global defaultCoords
        global minX
        global minY
        global maxX
        global maxY
        
        self.defaultCoords = (-20, -20, 20, 20)
        self.minX = self.defaultCoords[0]
        self.minY = self.defaultCoords[1]
        self.maxX = self.defaultCoords[2]
        self.maxY = self.defaultCoords[3]

        # 5. default color settings
        bg_color = 'black'
        fg_color = 'white'

        #*************************************************************
        # the main frames for this program

        # 1. the outer, countainer frame of the entire thing
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

        # 1. label
        self.controlLabel = tk.Label(self.controlFrame, text = "INPUTS FOR Fractal Tree Generator", fg = 'white', bg = 'black')
        self.controlLabel.grid(row = 10, column = 1, columnspan = 1, padx = 5, pady = 15)

        # 2a. BRANCH ANGLE scroll
        self.baScroll = tk.Scale(self.controlFrame, from_ = 0, to = 90, tickinterval = 15, resolution = 1)
        self.baScroll.configure(label = "Branching Angle", orient = tk.HORIZONTAL)
        self.baScroll.configure(bg = 'black', fg = 'white', troughcolor = 'white', activebackground = 'white')
        self.baScroll.configure(variable = self.baScaleVar)
        self.baScroll.grid(row = 20, column = 1, columnspan = 1, padx = 5, pady = (10,0), sticky = tk.W + tk.E)

        # 2b. SCALE FACTOR scroll
        self.sfScroll = tk.Scale(self.controlFrame, from_ = 0, to = 1, tickinterval = 0.2, resolution = 0.05)
        self.sfScroll.configure(label = "Scale Factor", orient = tk.HORIZONTAL)
        self.sfScroll.configure(bg = 'black', fg = 'white', troughcolor = 'white', activebackground = 'white')
        self.sfScroll.configure(variable = self.sfScaleVar)
        self.sfScroll.grid(row = 30, column = 1, columnspan = 1, padx = 0, pady = (10,0), sticky = tk.W + tk.E)

        # 2c. ANGLE VARIATION scroll
        self.avScroll = tk.Scale(self.controlFrame, from_ = 0, to = 90, tickinterval = 15, resolution = 1)
        self.avScroll.configure(label = "Angle Variation", orient = tk.HORIZONTAL)
        self.avScroll.configure(bg = 'black', fg = 'white', troughcolor = 'white', activebackground = 'white')
        self.avScroll.configure(variable = self.avScaleVar)
        self.avScroll.grid(row = 40, column = 1, columnspan = 1, padx = 0, pady = (10,0), sticky = tk.W + tk.E)

        # 3a. new frame for radiobuttons
        self.radioFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.radioFrame.configure(text = "Lab Mode")
        self.radioFrame.grid(row = 50, column = 1, padx = 0, pady = (10, 0), sticky = tk.W + tk.E)

        # 3b. Styling for radiobuttons
        s = ttk.Style()
        s.configure('color.TRadiobutton', background = 'black', foreground = 'white')

        # 3b. SINGLE TREE radiobutton
        self.singleTreeMode = ttk.Radiobutton(self.radioFrame, text = "Single Tree", variable = self.modeVar, value = 0, command = lambda: self.selSingleTree(0))
        self.singleTreeMode.configure(style = 'color.TRadiobutton')
        self.singleTreeMode.grid(row = 1, column = 1, padx = (10,1), pady = 0, sticky = tk.W + tk.E)

        # 3c. TREE PLANTER radiobutton
        self.treePlanterMode = ttk.Radiobutton(self.radioFrame, text = "Tree Planter", variable = self.modeVar, value = 1, command = lambda: self.selPlantTree(1))
        self.treePlanterMode.configure(style = 'color.TRadiobutton')
        self.treePlanterMode.grid(row = 2, column = 1, padx = (10,1), pady = 0, sticky = tk.W + tk.E)

        # 3d. WAlK SIMULATOR radiobutton
        self.walkSimulationMod = ttk.Radiobutton(self.radioFrame, text = "Walk Simulation", variable = self.modeVar, value = 2, command = lambda: self.selWalkSim(2))
        self.walkSimulationMod.configure(style = 'color.TRadiobutton')
        self.walkSimulationMod.grid(row = 3, column = 1, padx = (10,1), pady = 0, sticky = tk.W + tk.E)

        # 3. LEVEL entry
        self.lvlEntry = ttk.Entry(self.controlFrame)
        self.lvlEntry.configure(textvariable = self.lvlScaleVar) # **Might have to change lvlScaleVar to a string**
        self.lvlEntry.grid(row= 60, column = 1, columnspan = 1, padx = 0, pady = (10,0), sticky = tk.W + tk.E)

        # 4. new frame for DRAW & CLEAR & ZOOM buttons
        self.drawClearFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.drawClearFrame.configure(text = "control buttons")
        self.drawClearFrame.grid(row = 70, column = 1, padx = 0, pady = 5, sticky = tk.N + tk.S)

        # 5a. DRAW button
        self.drawLineButton = ttk.Button(self.drawClearFrame, text = "DRAW", command = lambda: self.acceptInputs())
        self.drawLineButton.grid(row = 1, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        # 5b. CLEAR button
        self.clearButton = ttk.Button(self.drawClearFrame, text = "CLEAR", command = lambda: self.secondaryInputs())
        self.clearButton.grid(row = 1, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        # INSTRUCTIONS label
        global instructions
        instructions = "Single Tree Mode:,\nChange the inputs\nto see the tree change,\n\n"
        self.instructLabel = tk.Label(self.controlFrame, text = instructions, fg = 'white', bg = 'black')
        self.instructLabel.grid(row = 100, column = 1)

        # initialize scale widgets to corresponding initial parameter values
        self.baScroll.set(self.branchAngle)
        self.sfScroll.set(self.scaleFactor)
        self.lvlScaleVar.set(self.level)
        self.fdScaleVar.set(self.forestDensity)
        self.frame.pack()

    #*************************************************************
    # Radiobutton Selection Functions

    def selSingleTree(self, mod):
        # Clear Trees
        self.clearTrees()
        self.mode = mod # temp fix

        # Set Buttons
        self.drawLineButton.configure(text = "DRAW")
        self.clearButton.configure(text = "CLEAR")

        # Configure Angle Variation Scale
        self.avScroll.configure(to = 90, tickinterval = 15, resolution = 1)
        self.avScroll.configure(label = "Angle Variation")
        self.avScroll.configure(variable = self.avScaleVar)

        # Change instructions label
        instructions = "Single Tree Mode:,\nChange the inputs\nto see the tree change,\n\n"
        self.instructLabel.configure(text = instructions)

    def selPlantTree(self, mod):
        # Clear Trees
        self.clearTrees()
        self.mode = mod # temp fix

        # Set Buttons
        self.drawLineButton.configure(text = "PLANT")
        self.clearButton.configure(text = "CLEAR")

        # Configure Angle Variation Scale
        self.avScroll.configure(to = 90, tickinterval = 15, resolution = 1)
        self.avScroll.configure(label = "Angle Variation")
        self.avScroll.configure(variable = self.avScaleVar)

        # Change instructions label
        instructions = "Plant Tree Mode:,\nChange the inputs,\nthen click on the window\nto plant your trees.\n"
        self.instructLabel.configure(text = instructions)

    def selWalkSim(self, mod):
        # Clear Trees
        self.clearTrees()

        # Clear Roots
        del self.roots[:]

        # Set Buttons
        self.drawLineButton.configure(text = "SET TREES")
        self.clearButton.configure(text = "STEP")

        # Configure Forest Density Scale
        self.forestDensity = int(self.fdScaleVar.get())
        self.avScroll.configure(to = 20, tickinterval = 4, resolution = 1)
        self.avScroll.configure(label = "Forest Density")
        self.avScroll.configure(variable = self.fdScaleVar)

        # Change instructions label
        instructions = "Walking Simulator:,\nClick set trees to\nset tree qualities.\nClick step to step forward.\n *angle variation disabled"
        self.instructLabel.configure(text = instructions)
        
        # Get random roots
        for i in range(self.forestDensity):
            newRoot = Point(random.uniform(-15, 15), random.uniform(-15, 15))
            self.roots.append(newRoot)

        # Sort order of trees from furthest to closest
        self.quickSortY(self.roots)
        
        # Draw trees
        for root in self.roots:
            distance = self.maxY - root.getY()
            root_length = (1 - self.scaleFactor) * distance
            
            # Check if the distance is less than 20
            if(distance < 20):
                oFactor = distance / 20
                ln_color = color_rgb(int(oFactor * 255), int(oFactor * 255), int(oFactor * 255))

            else:
                ln_color = 'white'
            self.generator(self.graph, root, 90, self.branchAngle, self.scaleFactor, root_length, self.level, 0, 10, 0.5, ln_color)

        # Set Mode
        self.mode = mod # temp fix

    #*************************************************************
    # Button Input Functions

    def acceptInputs(self):
        # Initialize inputs
        self.branchAngle = int(self.baScaleVar.get())
        self.scaleFactor = self.sfScaleVar.get()
        self.level = int(self.lvlScaleVar.get())
        self.angleVariation = int(self.avScaleVar.get())
        self.forestDensity = int(self.fdScaleVar.get())

        # Single Tree Mode
        if(self.mode == 0):
            
            # Default Tree Settings
            root_point = Point(0, - 15)
            distance = self.maxY - root_point.getY()
            root_length = (0.98 - self.scaleFactor) * distance

            # Clear Trees
            if(len(self.lines) > 0):
                self.clearTrees()

            # Generate Single Tree
            self.generator(self.graph, root_point, 90, self.branchAngle, self.scaleFactor, root_length, self.level, self.angleVariation, 10, 0.5, 'white')

        # Tree Plant Mode
        if(self.mode == 1):

            # Change instructions label
            instructions = "Click on the window to plant a tree.\n\n\n\n"
            self.instructLabel.configure(text = instructions)

            # Set root settings depending on user click
            root_point = self.graph.getMouse()
            distance = self.maxY - root_point.getY()
            root_length = (0.98 - self.scaleFactor) * distance
            root_width = (1 - 0.5) * distance

            # Generate Tree
            self.generator(self.graph, root_point, 90, self.branchAngle, self.scaleFactor, root_length, self.level, self.angleVariation, root_width, 0.5, 'white')

            # Change instructions label back
            instructions = "Plant Tree Mode:,\nChange the inputs,\nthen click on the window\nto plant your trees.\n"
            self.instructLabel.configure(text = instructions)

        # Walk Simulation Mode
        if(self.mode == 2):

            # Clear Trees
            self.clearTrees()

            # Clear Roots
            del self.roots[:]

            # Draw Random Trees
            numTrees = self.forestDensity
        
            for i in range(numTrees):
                newRoot = Point(random.uniform(-15, 15), random.uniform(-15, 15))
                self.roots.append(newRoot)

            for root in self.roots:
                distance = self.maxY - root.getY()
                root_length = (1 - self.scaleFactor) * distance

                # Check if the distance is less than 20
                if(distance < 20):
                    oFactor = distance / 20
                    ln_color = color_rgb(int(oFactor * 255), int(oFactor * 255), int(oFactor * 255))

                else:
                    ln_color = 'white'
                self.generator(self.graph, root, 90, self.branchAngle, self.scaleFactor, root_length, self.level, 0, 10, 0.5, ln_color)
            

    def secondaryInputs(self):
        # Single Tree and Tree Plant Mode
        if(self.mode == 0 or self.mode == 1):

            # Clear Trees
            self.clearTrees()

        if(self.mode == 2):

            # Take a step
            self.step(self.graph)

    #*************************************************************
    # Main Functions

    def generator(self, win, pt_init, main_angle, theta, sf, length, lvl, maxV, width, t_sf, color):
        levelCount = 0
        # if the level count reaches lvl
        if(lvl > 0):
            # Draw the main branch
            self.drawLine(win, pt_init, main_angle, length, width, color)

            # Set the end point as the new point
            pt_current = self.endPoint(pt_init, main_angle, length)
            
            # Start a new branch towards the right
            self.generator(win, pt_current, main_angle + theta + random.uniform(-maxV, maxV), theta, sf, length * sf, lvl - 1, maxV, width * t_sf, t_sf, color) # Random Angles

            # Start a new branch towards the left
            self.generator(win, pt_current, main_angle - theta + random.uniform(-maxV, maxV), theta, sf, length * sf, lvl - 1, maxV, width * t_sf, t_sf, color) # Random Angles

        # Base Case
        else:
            # Draw the end branch
            self.drawLine(win, pt_init, main_angle, length, width, color)

    def step(self, win):
        # Modify every root point
        for i in range(len(self.roots)):

            # Calculate deltaX and deltaY based on the root position
            currentX = self.roots[i].getX()
            currentY = self.roots[i].getY()
            distance = self.minY - currentY
            scaleFactorX = ((distance / 40) ** 3)
            deltaX = (currentX / scaleFactorX) / 500
            deltaY = 2
            
            if(currentX > 0):
                newRoot = Point(currentX - deltaX, currentY - deltaY)
            else:
                newRoot = Point(currentX - deltaX, currentY - deltaY)
            
            self.roots[i] = newRoot

        # Check if any of the roots are past the window's fov
        for i in range(len(self.roots)):
            currentX = self.roots[i].getX()
            currentY = self.roots[i].getY()
            if(currentX > 30 or currentX < -30):
                # Change the root so that it moves the tree back to the top at a random location
                newX = random.uniform(-20, 20)
                newY = random.uniform(15, 20)
                newRoot = Point(newX, newY)
                self.roots[i] = newRoot

        # Clear the trees
        self.clearTrees()

        # Sort the roots from furthest to closest
        self.quickSortY(self.roots)

        # Draw new trees at every root
        for root in self.roots:
            distance = self.maxY - root.getY()
            root_length = (1 - self.scaleFactor) * distance

            # Check if the distance is less than 20
            if(distance < 20):
                oFactor = distance / 20
                ln_color = color_rgb(int(oFactor * 255), int(oFactor * 255), int(oFactor * 255))

            else:
                ln_color = 'white'
            self.generator(self.graph, root, 90, self.branchAngle, self.scaleFactor, root_length, self.level, 0, 10, 0.5, ln_color)

            

    def endPoint(self, pt_init, angle, length):
        angle = angle * (pi/180)
        finalX = (pt_init.getX() + (length * cos(angle)))
        finalY = (pt_init.getY() + (length * sin(angle)))
        return Point(finalX, finalY)

    def drawLine(self, win, pt_init, angle, length, width, color):
        # Conversion from degrees to radians
        angle = angle * (pi/180)
        
        # Store initial x and y coordinates
        init_x = pt_init.getX()
        init_y = pt_init.getY()
        
        # Get the x and y displacement using the angle and length
        delta_x = length * cos(angle)
        delta_y = length * sin(angle)

        # Make a final point by adding the displacements to the corresponding points
        pt_final = Point(init_x + delta_x, init_y + delta_y)

        # Set the width and draw the line
        newLine = Line(pt_init, pt_final)
        newLine.setOutline(color)
        newLine.setWidth(width)
        newLine.draw(win)

        # Add the drawn line to the database of lines
        self.lines.append(newLine)

    def clearTrees(self):
        for idx, val in enumerate(self.lines):
            val.undraw()
        del self.lines[:]

    def quickSortY(self, items):
        # Implementation of quick sort
        if(len(items) > 1):
            pivot_index = int(len(items) / 2)
            smaller_items = []
            larger_items = []

            for i, val in enumerate(items):
                if i != pivot_index:
                    if val.getY() < items[pivot_index].getY():
                        smaller_items.append(val)
                    else:
                        larger_items.append(val)

            self.quickSortY(smaller_items)
            self.quickSortY(larger_items)
            items[:] = larger_items + [items[pivot_index]] + smaller_items

                
