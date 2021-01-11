# 2D Cellular Automata Tkinter GUI
# Peter, Oliver, Manny
# The GUI Design for our 2D Cellular Automata Program
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
from time import sleep

class CellularAutomata2D:

    # Constructor for CA class, which implements an App to
    # explore the 2D Celullar Automata
    def __init__(self, master):
        self.master = master

        #*************************************************************
        #MAIN FRAMES
        
        
        #1. the outer, container frame of the entire thing
        self.frame = tk.Frame(self.master, background = 'black')

        #2. the plot window will go inside of drawFrame
        self.drawFrame = tk.Frame(self.frame)
        self.drawFrame.grid(row = 1, column = 10, padx = 5, pady = 5)
        

        #3. the frame to hold the controls (buttons, sliders, etc.)
        self.controlFrame = tk.Frame(self.frame, bg = 'black')
        self.controlFrame.grid(row = 1, column = 50, padx = 10, pady = [10,100], sticky = tk.N + tk.S)

        #*************************************************************
        #GRAPH WINDOW

        #1. default window settings for graph window &
        #   storage of current window settings
        self.defaultCoords = [0, 0, 50, 50]
        self.DCminX = self.defaultCoords[0]
        self.DCminY = self.defaultCoords[1]
        self.DCmaxX = self.defaultCoords[2]
        self.DCmaxY = self.defaultCoords[3]

        #2. Set graph window
        self.win = GraphWin(self.drawFrame, 600, 600, autoflush = True)
        self.win.grid(row = 1, column = 1)
        self.win.setBackground('white')
        self.win.setCoords(self.DCminX, self.DCminY, self.DCmaxX, self.DCmaxY)

        #3. Draw the grid lines
        for i in range(self.DCmaxX + 1):
            Line(Point(i,0), Point(i,self.DCmaxX)).draw(self.win)
        for i in range(self.DCmaxY + 1):
            Line(Point(0,i), Point(self.DCmaxY,i)).draw(self.win)

        #4. RULE ELEMENT ENTRY settings and graph that allows users to represent rules
        #   storage of current window settings
        self.entryCoords = [0, 0, 3, 3]
        self.RCminX = self.entryCoords[0]
        self.RCminY = self.entryCoords[1]
        self.RCmaxX = self.entryCoords[2]
        self.RCmaxY = self.entryCoords[3]

        #   set entry window
        self.entryWin = GraphWin(self.controlFrame, 90, 90, autoflush = False)
        self.entryWin.grid(row = 30, column = 1, padx = 0, pady = 15)
        self.entryWin.setBackground('white')
        self.entryWin.setCoords(self.RCminX, self.RCminY, self.RCmaxX, self.RCmaxY)
        
        #   draw grid lines
        for i in range(self.DCmaxX + 1):
            Line(Point(i,0), Point(i,self.RCmaxX)).draw(self.entryWin)
        for i in range(self.DCmaxY + 1):
            Line(Point(0,i), Point(self.RCmaxY,i)).draw(self.entryWin)
                
        #*************************************************************
        #INSTANCE FIELDS

        #1. list of SQUARES to be drawn
        self.squares = []

        #1a. list of ENTRY SQUARES to be drawn
        self.entrySquares = []

        #2. 2D matrix of active and unactive GRID SQUARES
        self.grid = [[0 for x in range(self.DCmaxX)] for y in range(self.DCmaxY)]

        #2a. 2D matrix of active and unactive ENTRY GRID SQUARES
        self.entryGrid = [[0 for x in range(self.RCmaxX)] for y in range(self.RCmaxY)]

        #3. mode selection boolean
        self.mode = 0
        self.modeVar = tk.IntVar()

        #4. list containing the RULE
        self.rule = []

        #5. STOP variable
        self.stop = False

        #*************************************************************
        #CONTROL FRAME
        
        #1. MAIN LABEL that indicates the control frame
        self.controlLabel = tk.Label(self.controlFrame, text = "RULE SETTINGS for 2D Cellular Automata", fg = 'white', bg = 'black')
        self.controlLabel.grid(row = 10, column = 1, columnspan = 1, padx = 5, pady = 5)
        
        #2. RULE LIST BOX that shows the currently selected rules
        self.ruleListbox = tk.Listbox(self.controlFrame, height = 15)
        self.ruleListbox.grid(row = 20, column = 1, columnspan = 1, padx = 0, pady = 0)

        #4. MODE SELECTION RADIO BUTTON
        #   new frame for radiobuttons
        self.radioFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.radioFrame.configure(text = "Lab Mode")
        self.radioFrame.grid(row = 40, column = 1, padx = 0, pady = (10, 0), sticky = tk.W + tk.E)

        #   styling for radiobuttons
        s = ttk.Style()
        s.configure('color.TRadiobutton', background = 'black', foreground = 'white')
        
        #   "set initial points" radio button
        self.setInitialMode = ttk.Radiobutton(self.radioFrame, text = "Set Initial Conditions", variable = self.modeVar, value = 0, command = lambda: self.selectMode(0))
        self.setInitialMode.configure(style = 'color.TRadiobutton')
        self.setInitialMode.grid(row = 1, column = 1, padx = (10,1), pady = 0, sticky = tk.W + tk.E)

        #   "configure rule" radio button
        self.setRuleMode = ttk.Radiobutton(self.radioFrame, text = "Configure Rule", variable = self.modeVar, value = 1, command = lambda: self.selectMode(1))
        self.setRuleMode.configure(style = 'color.TRadiobutton')
        self.setRuleMode.grid(row = 2, column = 1, padx = (10,1), pady = 0, sticky = tk.W + tk.E)

        #*************************************************************
        #BUTTON FRAME

        #1. new FRAME for buttons
        self.buttonFrame = tk.LabelFrame(self.controlFrame, bg = 'black', fg = 'white')
        self.buttonFrame.configure(text = "control buttons")
        self.buttonFrame.grid(row = 50, column = 1, padx = 0, pady = 5, sticky = tk.N + tk.S)

        #2. ADD button
        self.addButton = ttk.Button(self.buttonFrame, text = "ADD TO RULE", command = lambda: self.addToRule(self.entryGrid, self.ruleListbox))
        self.addButton.grid(row = 1, column = 1, padx = 0, pady = 2, sticky = tk.W + tk.E)

        #3. EDIT button
        self.editButton = ttk.Button(self.buttonFrame, text = "EDIT RULE", command = lambda: self.editRule(self.entryGrid, self.ruleListbox))
        self.editButton.grid(row = 1, column = 2, padx = 0, pady = 2, sticky = tk.W + tk.E)

        #4. DELETE button
        self.removeButton = ttk.Button(self.buttonFrame, text = "REMOVE FROM RULE", command = lambda: self.removeFromRule(self.ruleListbox))
        self.removeButton.grid(row = 2, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        #5. STEP button
        self.stepButton = ttk.Button(self.buttonFrame, text = "STEP", command = lambda: self.evaluate(self.grid, self.win, self.rule, self.squares))
        self.stepButton.grid(row = 2, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        #6. RUN button
        self.runButton = ttk.Button(self.buttonFrame, text = "RUN", command = lambda: self.run())
        self.runButton.grid(row = 3, column = 1, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        #7. STOP button
        self.stopButton = ttk.Button(self.buttonFrame, text = "STOP", command = lambda: self.stopEval())
        self.stopButton.grid(row = 3, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        
        #*************************************************************
        #INITIALIZE WIDGETS
        self.frame.pack()
        self.selectMode(0)


    #*************************************************************
    #GUI FUNCTIONS
            
    def selectMode(self, mod):
        # Set the mode
        self.mode = mod
        while(self.mode == 0):
            click = self.win.getMouse()
            try:
                self.toggleSquare(click.getX(), click.getY(), self.grid, self.win, self.squares)
            except:
                pass
        while(self.mode == 1):
            click = self.entryWin.getMouse()
            try:
                self.toggleSquare(click.getX(), click.getY(), self.entryGrid, self.entryWin, self.entrySquares)
            except:
                pass

    def addToRule(self, ruleGrid, lb):
        try:
            total = 0
            # Check the ruleGrid and evaluate
            if(ruleGrid[0][2]):
                total = total + 1
            if(ruleGrid[1][2]):
                total = total + 2
            if(ruleGrid[2][2]):
                total = total + 4
            if(ruleGrid[0][1]):
                total = total + 8
            if(ruleGrid[1][1]):
                total = total + 16
            if(ruleGrid[2][1]):
                total = total + 32
            if(ruleGrid[0][0]):
                total = total + 64
            if(ruleGrid[1][0]):
                total = total + 128
            if(ruleGrid[2][0]):
                total = total + 256
            # Add the total to the rule
            self.rule.append(total)
            # Add the neighborhood to the rule list box
            lb.insert(len(self.rule) - 1, str(self.rule[len(self.rule) - 1]))
        except:
            pass

    def editRule(self, ruleGrid, lb):
        try:
            # get the index of the listbox item
            index = lb.index('active')

            # Check the ruleGrid and evaluate
            total = 0
            # Check the ruleGrid and evaluate
            if(ruleGrid[0][2]):
                total = total + 1
            if(ruleGrid[1][2]):
                total = total + 2
            if(ruleGrid[2][2]):
                total = total + 4
            if(ruleGrid[0][1]):
                total = total + 8
            if(ruleGrid[1][1]):
                total = total + 16
            if(ruleGrid[2][1]):
                total = total + 32
            if(ruleGrid[0][0]):
                total = total + 64
            if(ruleGrid[1][0]):
                total = total + 128
            if(ruleGrid[2][0]):
                total = total + 256
            # Add the total to the rule
            self.rule.append(total)
            # Change the rule value at the index
            self.rule[index] = total
            # Change the value in the listbox item
            lb.delete(index)
            lb.insert(index, str(self.rule[index]))
        except:
            pass

    def removeFromRule(self, lb):
        try:
            # get the index of the listbox item
            index = lb.index('active')

            # remove the transformation from the rule and the listbox
            del self.rule[index]
            lb.delete(index)
        except:
            pass

    def run(self):
        try:
            self.stop = False
            while(self.stop == False):
                self.evaluate(self.grid, self.win, self.rule, self.squares)
                sleep(0.05)
        except:
            pass

    def stopEval(self):
        try:
            self.stop = True
        except:
            pass

        
    #*************************************************************
    #BACKGROUND FUNCTIONS
        
    def toggleSquare(self, x, y, grid, win, squares):
        "Turns on a cell and activates its position in a grid"
        square = -1

        # Check if there is a square drawn (bl = 1, tr = 2)
        for i in range(len(squares)):
            blCorner = squares[i].getP1()
            trCorner = squares[i].getP2()
            if(x >= blCorner.getX() and x < trCorner.getX()):
                if(y >= blCorner.getY() and y < trCorner.getY()):
                    square = i 

        # Draw a square if no square is present, else undraw
        if(square == -1):
            self.drawSquare(x, y, win, squares)
            grid[int(x)][int(y)] = True
        else:
            self.eraseSquare(square, squares)
            grid[int(x)][int(y)] = False

    def drawSquare(self, x, y, win, squares):
        newSquare = Rectangle(Point(int(x),int(y)), Point(int(x) + 1, int(y) + 1))
        newSquare.setFill('black')
        newSquare.draw(win)
        squares.append(newSquare)

    def eraseSquare(self, index, squares):
        squares[index].undraw()
        squares.pop(index)

    def setSquares(self, x_index, y_index, win, squares):
        # delete all squares
        for i in squares:
            del i

        # draw the new squares at the specified indecies
        for i in range(x_index):
            self.drawSquare(x_index[i], y_index[i], win, squares)

    def activeCells(self, grid):
        "Returns the indecies of active cells in a grid in a list length of two"
        x = []
        y = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if(grid[col][row]):
                    x.append(col)
                    y.append(row)
        active = [x,y]
        return active

    #*************************************************************
    #MAIN FUNCTIONS

    

    def check(self, x, y, grid, rule):
        total = 0

        # Check each cell in the surrounding neighborhood if it's active
        # Inner Cells
        if((x > 0 and x < len(grid) - 1) and (y > 0 and y < len(grid) - 1)):
            # Top Left
            if(grid[x - 1][y + 1]):
                total = total + 1
            # Top Center
            if(grid[x][y + 1]):
                total = total + 2
            # Top Right
            if(grid[x + 1][y + 1]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[x + 1][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[x + 1][y - 1]):
                total = total + 256
        # West Cells
        if(x == 0 and y > 0 and y < len(grid) - 1):
            # Top Left
            if(grid[len(grid) - 1][y + 1]):
                total = total + 1
            # Top Center
            if(grid[x][y + 1]):
                total = total + 2
            # Top Right
            if(grid[x + 1][y + 1]):
                total = total + 4
            # Mid Left
            if(grid[len(grid) - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[x + 1][y]):
                total = total + 32
            # Bot Left
            if(grid[len(grid) - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[x + 1][y - 1]):
                total = total + 256
        # East Cells
        if(x == len(grid) - 1 and y > 0 and y < len(grid) - 1):
            # Top Left
            if(grid[x - 1][y + 1]):
                total = total + 1
            # Top Center
            if(grid[x][y + 1]):
                total = total + 2
            # Top Right
            if(grid[0][y + 1]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[0][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[0][y - 1]):
                total = total + 256
        # North Cells
        if(x > 0 and x < len(grid) - 1 and y == len(grid) - 1):
            # Top Left
            if(grid[x - 1][0]):
                total = total + 1
            # Top Center
            if(grid[x][0]):
                total = total + 2
            # Top Right
            if(grid[x + 1][0]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[x + 1][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[x + 1][y - 1]):
                total = total + 256
        # South Cells
        if(x > 0 and x < len(grid) - 1 and y == 0):
            # Top Left
            if(grid[x - 1][y + 1]):
                total = total + 1
            # Top Center
            if(grid[x][y + 1]):
                total = total + 2
            # Top Right
            if(grid[x + 1][y + 1]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[x + 1][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][len(grid) - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][len(grid) - 1]):
                total = total + 128
            # Bot Right
            if(grid[x + 1][len(grid) - 1]):
                total = total + 256
        # NorthWest Corner
        if(x == 0 and y == len(grid) - 1):
            # Top Left
            if(grid[len(grid) - 1][0]):
                total = total + 1
            # Top Center
            if(grid[x][0]):
                total = total + 2
            # Top Right
            if(grid[x + 1][0]):
                total = total + 4
            # Mid Left
            if(grid[len(grid) - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[x + 1][y]):
                total = total + 32
            # Bot Left
            if(grid[len(grid) - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[x + 1][y - 1]):
                total = total + 256
        # SouthEast Corner
        if(x == len(grid) - 1 and y == 0):
            # Top Left
            if(grid[x - 1][1]):
                total = total + 1
            # Top Center
            if(grid[x][1]):
                total = total + 2
            # Top Right
            if(grid[0][1]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[0][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][x]):
                total = total + 64
            # Bot Center
            if(grid[x][x]):
                total = total + 128
            # Bot Right
            if(grid[0][x]):
                total = total + 256
        # NorthEast Corner
        if(x == len(grid) - 1 and y == len(grid) - 1):
            # Top Left
            if(grid[x - 1][0]):
                total = total + 1
            # Top Center
            if(grid[x][0]):
                total = total + 2
            # Top Right
            if(grid[0][0]):
                total = total + 4
            # Mid Left
            if(grid[x - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[0][y]):
                total = total + 32
            # Bot Left
            if(grid[x - 1][y - 1]):
                total = total + 64
            # Bot Center
            if(grid[x][y - 1]):
                total = total + 128
            # Bot Right
            if(grid[0][y - 1]):
                total = total + 256
        # SouthWest Corner
        if(x == 0 and y == 0):
            # Top Left
            if(grid[len(grid) - 1][1]):
                total = total + 1
            # Top Center
            if(grid[0][1]):
                total = total + 2
            # Top Right
            if(grid[1][1]):
                total = total + 4
            # Mid Left
            if(grid[len(grid) - 1][y]):
                total = total + 8
            # Mid Center
            if(grid[x][y]):
                total = total + 16
            # Mid Right
            if(grid[1][y]):
                total = total + 32
            # Bot Left
            if(grid[len(grid) - 1][len(grid) - 1]):
                total = total + 64
            # Bot Center
            if(grid[0][len(grid) - 1]):
                total = total + 128
            # Bot Right
            if(grid[1][len(grid) - 1]):
                total = total + 256
            
        # Check current neighborhood against the rule
        for i in range(len(rule)):
            if(rule[i] == total):
                return True
        return False

    def evaluate(self, grid, win, rule, squares):
        " Takes a step in the cellular automata"
        # Take the grid, find all active cells, and store the x and y positions
        activeCellsCoords = self.activeCells(grid)
        x_active = activeCellsCoords[0]
        y_active = activeCellsCoords[1]

        x_cellsToActivate = []
        y_cellsToActivate = []

        # Evaluate all cells in the neighborhood of currently active cells
        for i in range(len(x_active)):
            x = x_active[i]
            y = y_active[i]
            # Inner Squares
            if((x > 0 and x < len(grid) - 1) and (y > 0 and y < len(grid) - 1)):
                # Top Left
                if(self.check(x - 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y + 1)
                # Top Center
                if(self.check(x, y + 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y + 1)
                # Top Right
                if(self.check(x + 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y + 1)
                # Mid Left
                if(self.check(x - 1, y, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(x + 1, y, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(x - 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y - 1)
                # Bot Center
                if(self.check(x, y - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y - 1)
                # Bot Right
                if(self.check(x + 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y - 1)
            # West Cells
            if(x == 0 and y > 0 and y < len(grid) - 1):
                # Top Left
                if(self.check(len(grid) - 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(y + 1)
                # Top Center
                if(self.check(x, y + 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y + 1)
                # Top Right
                if(self.check(x + 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y + 1)
                # Mid Left
                if(self.check(len(grid) - 1, y, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(x + 1, y, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(len(grid) - 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(y - 1)
                # Bot Center
                if(self.check(x, y - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y - 1)
                # Bot Right
                if(self.check(x + 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y - 1)
            # East Cells
            if(x == len(grid) - 1 and y > 0 and y < len(grid) - 1):
                # Top Left
                if(self.check(x - 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y + 1)
                # Top Center
                if(self.check(x, y + 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y + 1)
                # Top Right
                if(self.check(0, y + 1, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(y + 1)
                # Mid Left
                if(self.check(x - 1, y, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(0, y, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(x - 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y - 1)
                # Bot Center
                if(self.check(x, y - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y - 1)
                # Bot Right
                if(self.check(0, y - 1, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(y - 1)
            # North Cells
            if(x > 0 and x < len(grid) - 1 and y == len(grid) - 1):
                # Top Left
                if(self.check(x - 1, 0, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(0)
                # Top Center
                if(self.check(x, 0, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(0)
                # Top Right
                if(self.check(x + 1, 0, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(0)
                # Mid Left
                if(self.check(x - 1, y, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(x + 1, y, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(x - 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y - 1)
                # Bot Center
                if(self.check(x, y - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y - 1)
                # Bot Right
                if(self.check(x + 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y - 1)
            # South Cells
            if(x > 0 and x < len(grid) - 1 and y == 0):
                # Top Left
                if(self.check(x - 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y + 1)
                # Top Center
                if(self.check(x, y + 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y + 1)
                # Top Right
                if(self.check(x + 1, y + 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y + 1)
                # Mid Left
                if(self.check(x - 1, y, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(x + 1, y, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(x - 1, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(len(grid) - 1)
                # Bot Center
                if(self.check(x, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(len(grid) - 1)
                # Bot Right
                if(self.check(x + 1, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(len(grid) - 1)
            # NorthWest Corner
            if(x == 0 and y == len(grid) - 1):
                # Top Left
                if(self.check(y, 0, grid, rule)):
                    x_cellsToActivate.append(y)
                    y_cellsToActivate.append(0)
                # Top Center
                if(self.check(0, 0, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(0)
                # Top Right
                if(self.check(1, 0, grid, rule)):
                    x_cellsToActivate.append(1)
                    y_cellsToActivate.append(0)
                # Mid Left
                if(self.check(y, y, grid, rule)):
                    x_cellsToActivate.append(y)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(x + 1, y, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(y, y - 1, grid, rule)):
                    x_cellsToActivate.append(y)
                    y_cellsToActivate.append(y - 1)
                # Bot Center
                if(self.check(x, y - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y - 1)
                # Bot Right
                if(self.check(x + 1, y - 1, grid, rule)):
                    x_cellsToActivate.append(x + 1)
                    y_cellsToActivate.append(y - 1)
            # SouthWest Corner
            if(x == len(grid) - 1 and y == 0):
                # Top Left
                if(self.check(x - 1, 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(1)
                # Top Center
                if(self.check(x, 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(1)
                # Top Right
                if(self.check(0, 1, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(1)
                # Mid Left
                if(self.check(x - 1, 0, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(0)
                # Mid Center
                if(self.check(x, 0, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(0)
                # Mid Right
                if(self.check(0, 0, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(0)
                # Bot Left
                if(self.check(x - 1, x, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(x)
                # Bot Center
                if(self.check(x, x, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(x)
                # Bot Right
                if(self.check(0, x, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(x)
            # NorthEast Corner
            if(x == len(grid) - 1 and y == len(grid) - 1):
                # Top Left
                if(self.check(x - 1, 0, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(0)
                # Top Center
                if(self.check(x, 0, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(0)
                # Top Right
                if(self.check(0, 0, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(0)
                # Mid Left
                if(self.check(x - 1, y, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(0, y, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(x - 1, x - 1, grid, rule)):
                    x_cellsToActivate.append(x - 1)
                    y_cellsToActivate.append(x - 1)
                # Bot Center
                if(self.check(x, x - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(x - 1)
                # Bot Right
                if(self.check(0, x - 1, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(x - 1)
            # SouthWest Corner
            if(x == 0 and y == 0):
                # Top Left
                if(self.check(len(grid) - 1, 1, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(1)
                # Top Center
                if(self.check(0, 1, grid, rule)):
                    x_cellsToActivate.append(0)
                    y_cellsToActivate.append(1)
                # Top Right
                if(self.check(1, 1, grid, rule)):
                    x_cellsToActivate.append(1)
                    y_cellsToActivate.append(1)
                # Mid Left
                if(self.check(len(grid) - 1, y, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(y)
                # Mid Center
                if(self.check(x, y, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(y)
                # Mid Right
                if(self.check(1, y, grid, rule)):
                    x_cellsToActivate.append(1)
                    y_cellsToActivate.append(y)
                # Bot Left
                if(self.check(len(grid) - 1, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(len(grid) - 1)
                    y_cellsToActivate.append(len(grid) - 1)
                # Bot Center
                if(self.check(x, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(x)
                    y_cellsToActivate.append(len(grid) - 1)
                # Bot Right
                if(self.check(1, len(grid) - 1, grid, rule)):
                    x_cellsToActivate.append(1)
                    y_cellsToActivate.append(len(grid) - 1)

        # delete all squares
        for i in range(len(squares)):
            squares[i].undraw()
        for i in squares:
            del i
            
        # convert the entire grid to false
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                grid[col][row] = False

        # using the new list of points, go through the grid and draw all squares at those points
        for i in range(len(x_cellsToActivate)):
            self.drawSquare(x_cellsToActivate[i], y_cellsToActivate[i], win, squares)

        # Convert the grid to include True statements at now currently active cells
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                for i in range(len(x_cellsToActivate)):
                    if(col == x_cellsToActivate[i] and row == y_cellsToActivate[i]):
                        grid[col][row] = True

        
    
    
        
