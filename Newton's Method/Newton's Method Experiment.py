# Newton's Method Experiment
# Peter Kang
# v 1.0
from graphics import*
from math import*
import cmath as cm

''' functions '''
def f(z):
    return (z ** 4) - 1

def fPrime(z):
    return 4 * (z ** 3)

def T(z):
    return z - (f(z) / fPrime(z))

''' graph drawers '''
def colorGraph(win, xMin, xMax, yMin, yMax, stepSizeX, stepSizeY):
    x = xMin
    while(x < xMax):
        y = yMin
        while(y < yMax):
            z0 = complex(x,y)
            z = z0
            for i in range(10):
                z = T(z)
            plt_color = color(z)
            win.plot(x, y, plt_color)
            y += stepSizeY
        x += stepSizeX
    update()
    print('finished')
    

''' other features '''

def color(z):
    scale = 1
    first = abs(z + 1)
    second = abs(z - 1)
    third = abs(z + 1j)
    fourth = abs(z - 1j)
    roots = [first, second, third, fourth]
    if(max(roots) == first):
        return 'white'
    if(max(roots) == second):
        return color_rgb(107, 202, 249)
    if(max(roots) == third):
        return color_rgb(100, 103, 104)
    if(max(roots) == fourth):
        return 'black'

def zoom(win, ln_color):
    unConfirmed = True
    
    # Ask User to click two points and get those points
    print("Click the upper-left bound of your zoom")
    upperLeft = win.getMouse()
    
    print("Click the bottom-right bound of your zoom")
    bottomRight = win.getMouse()

    # Check for error
    if(bottomRight.getX() <= upperLeft.getX() or upperLeft.getY() <= bottomRight.getY()):
        # Output error message
        print("error: zoom mode disabled")

    else:
        # Draw the zoom box on the zoomable window
        zoom_top = Line(Point(upperLeft.getX(), upperLeft.getY()), Point(bottomRight.getX(),upperLeft.getY()))
        zoom_bottom = Line(Point(upperLeft.getX(), bottomRight.getY()),Point(bottomRight.getX(),bottomRight.getY()))
        zoom_right = Line(Point(bottomRight.getX(),upperLeft.getY()),Point(bottomRight.getX(),bottomRight.getY()))
        zoom_left = Line(Point(upperLeft.getX(), upperLeft.getY()), Point(upperLeft.getX(), bottomRight.getY()))

        zoom_top.setOutline(ln_color)
        zoom_bottom.setOutline(ln_color)
        zoom_right.setOutline(ln_color)
        zoom_left.setOutline(ln_color)

        zoom_top.draw(win)
        zoom_bottom.draw(win)
        zoom_right.draw(win)
        zoom_left.draw(win)

        # Ask the user to confirm zoom
        confirm = GraphWin("", 400, 100)
        confirm.setBackground('black')
        text_confirm = Text(Point(200,25), "Do you want to zoom?")
        text_confirm.setTextColor(ln_color)
        text_confirm.draw(confirm)

        yesButton = Rectangle(Point(100,50), Point(190,90))
        noButton = Rectangle(Point(210, 50), Point(300,90))

        yesButton.setOutline(ln_color)
        noButton.setOutline(ln_color)

        yesButton.draw(confirm)
        noButton.draw(confirm)

        text_yes = Text(Point(145,70), "Yes")
        text_no = Text(Point(255, 70), "No")

        text_yes.setTextColor(ln_color)
        text_no.setTextColor(ln_color)

        text_yes.draw(confirm)
        text_no.draw(confirm)

        # Wait for the user to click on the confirmation window
        while(unConfirmed):
            click = confirm.getMouse()

            # Check if the user clicked yes or no
            if(click.getY() > 50 and click.getY() < 90):
                if(click.getX() > 100 and click.getX() < 190):
                    unConfirmed = False
                    confirm.close()
                    
                    # Zoom code
                    print("zooming...")

                    # Set the new coordinates and clear the graph
                    xMin = upperLeft.getX()
                    xMax = bottomRight.getX()
                    yMax = upperLeft.getY()
                    yMin = bottomRight.getY()
                    win.clear()
                    win.setCoords(xMin, yMin, xMax, yMax)

                    # Reset stepSizes
                    stepSizeX = (xMax - xMin) / (win.width - 1)
                    stepSizeY = (yMax - yMin) / (win.width - 1)

                    # Redraw the graph previously on screen
                    colorGraph(win, xMin, xMax, yMin, yMax, stepSizeX, stepSizeY)
              
                if(click.getX() > 210 and click.getX() < 300):
                    unConfirmed = False
                    confirm.close()

        # Close all zoom instructions
        zoom_top.undraw()
        zoom_bottom.undraw()
        zoom_right.undraw()
        zoom_left.undraw()

''' main '''

def main():
    # Window
    win_color = GraphWin("color graph", 800, 800, autoflush = False)
    win_color.setCoords(-4, -4, 4, 4)

    # Parameters
    global stepSizeX
    global stepSizeY
    global precision

    global xMin
    global xMax
    global yMin
    global yMax

    global plt_color
    global ln_color

    xMin = -4
    xMax = 4
    yMin = -4
    yMax = 4
    
    stepSizeX = 0.01
    stepSizeY = 0.01
    plt_color = 'black'
    ln_color = 'white'
    unrooted = True

    # For every point in the complex plane
    colorGraph(win_color, xMin, xMax, yMin, yMax, stepSizeX, stepSizeY)

    # Draw the Y axis
    yAxis = Line(Point(0, -4), Point(0, 4))
    yAxis.setOutline('black')
    yAxis.draw(win_color)

    # Draw the X axis
    xAxis = Line(Point(-4, 0), Point(4, 0))
    xAxis.setOutline('black')
    xAxis.draw(win_color)

    # Draw the Roots
    firstRoot = Circle(Point(0,-1), 0.1)
    secondRoot = Circle(Point(-1,0), 0.1)
    thirdRoot = Circle(Point(1,0), 0.1)
    fourthRoot = Circle(Point(0,1), 0.1)

    firstRoot.setFill(color_rgb(100, 103, 104))
    secondRoot.setFill('white')
    thirdRoot.setFill(color_rgb(107, 202, 249))
    fourthRoot.setFill('black')

    firstRoot.draw(win_color)
    secondRoot.draw(win_color)
    thirdRoot.draw(win_color)
    fourthRoot.draw(win_color)

    while(True):
        zoom(win_color, ln_color)
                

if __name__ == "__main__":
    main()
    
    
