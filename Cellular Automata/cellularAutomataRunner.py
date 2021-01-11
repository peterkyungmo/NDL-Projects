# cellularAutomataRunner.py
# v 1.0
# Peter Kang

try:
    import Tkinter as tk
    import ttk
except ImportError: #for python 3.3
    import tkinter as tk
    from tkinter import ttk

import pkg.RP_graphics as graphics
from math import*
from random import random
from cellularAutomata2D import*

def main():
    #**********************************************************
    # 1. define the root window
    root = tk.Tk()

    #**********************************************************
    # 2. set up some of the important root window properties
    # 2a. main window caption
    root.title("Cellular Automata 2D")

    # 2b. pixel dimensions of main window (width x height)
    root.geometry("1280x720")

    # 2c. distance from top-left conrer of screen upon opening
    root.geometry("+200+120")

    # 2d. main window background color
    root.configure(background = 'black')

    #**********************************************************
    # 3. run the program by calling the App below
    window = CellularAutomata2D(root)
    root.mainloop()

if __name__ == "__main__":
    main()
