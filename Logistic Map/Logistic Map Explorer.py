# Logistic Map Explorer
# Peter Kang
# 10/21/2016

from pkg.graphics import *
import random
import math

def main():
    """ Initialize Instance Fields """
    # Color Settings
    bg_color = 'black'
    ln_color = 'green'

    # Processing Settings
    process = True
    
    """ Create a Menu Window """    
    # Create a menu window
    menu = GraphWin('Main Menu', 400, 400)
    menu.setBackground(bg_color)

    # Draw a title text object
    title = Text(Point(200, 100), "Exploring the Logistic Graph")
    title.setTextColor(ln_color)
    title.draw(menu)

    # Draw the bifurcation button
    bifButton = Rectangle(Point(150, 150), Point(250, 190))
    bifButton.setFill(bg_color)
    bifButton.setOutline(ln_color)
    bifButton.draw(menu)

    bifText = Text(Point(200, 170), "Bifurcation")
    bifText.setTextColor(ln_color)
    bifText.draw(menu)

    # Draw the time series button
    timeButton = Rectangle(Point(150, 200), Point(250, 240))
    timeButton.setFill(bg_color)
    timeButton.setOutline(ln_color)
    timeButton.draw(menu)

    timeText = Text(Point(200, 220), "Time Series")
    timeText.setTextColor(ln_color)
    timeText.draw(menu)
    
    # Draw the cobweb button
    cobButton = Rectangle(Point(150, 250), Point(250, 290))
    cobButton.setFill(bg_color)
    cobButton.setOutline(ln_color)
    cobButton.draw(menu)

    cobText = Text(Point(200, 270), "Cobweb")
    cobText.setTextColor(ln_color)
    cobText.draw(menu)
    

    # Draw a quit button
    quitButton = Rectangle(Point(150, 300), Point(250, 340))
    quitButton.setFill(bg_color)
    quitButton.setOutline(ln_color)
    quitButton.draw(menu)

    quitText = Text(Point(200, 320), "Quit")
    quitText.setTextColor(ln_color)
    quitText.draw(menu)

    """ Processing of the Menu Window """
    while(process):
        # Wait for the user to click on the main menu
        click = menu.getMouse()
        
        if(click.getX() > 150 and click.getX() < 250):
            # If the user clicked the bifurcation button...
            if(click.getY() > 150 and click.getY() < 190):

                # Launch the bifurcation program
                bifurcation()

            # If the user clicked the time series button...
            if(click.getY() > 200 and click.getY() < 240):

                # Launch the time series program
                timeSeries()

            # If the user clicked the cobweb button...
            if(click.getY() > 250 and click.getY() < 290):

                # Launch the cobweb program
                cobWeb()


            # If the user clicked the quit button...
            if(click.getY() > 300 and click.getY() < 340):
                
                # Shut down the program
                process = False
                menu.close()

#----------------------------------------------------------------------------------------------

""" Bifurcation Diagram Code """

def bifurcation():
    # Color Settings
    bg_color = 'black'
    ln_color = 'green'

    # Processing Settings
    process = True

    """ Setting up the interface """

    # Open a Graph Window
    winBifurcation = GraphWin('Bifurcation Diagram', 800, 400, autoflush = False)
    winBifurcation.setBackground(bg_color)
    winBifurcation.setCoords(-0.1, -0.05, 4.02, 1.01)

    # Draw the Y axis
    yAxis = Line(Point(0,-0.05), Point(0, 1.01))
    yAxis.setOutline(ln_color)
    yAxis.draw(winBifurcation)

    # Draw the X axis
    xAxis = Line(Point(-0.1, 0), Point(4.02, 0))
    xAxis.setOutline(ln_color)
    xAxis.draw(winBifurcation)
    update()

    # Open a Graph Menu
    menu = GraphWin('Bifurcation Menu', 400, 400)
    menu.setBackground(bg_color)

    # Draw labels for instance fields
    text_transient = Text(Point(100,100), "Number of Transients:")
    text_iterations = Text(Point(100,150), "Number of Iterations:")
    text_initX = Text(Point(100,200), "Initial Value:")

    text_transient.setTextColor(ln_color)
    text_iterations.setTextColor(ln_color)
    text_initX.setTextColor(ln_color)

    text_transient.draw(menu)
    text_iterations.draw(menu)
    text_initX.draw(menu)

    # Draw Entry Objects for instance fields
    input_transient = Entry(Point(250, 100), 7)
    input_iterations = Entry(Point(250, 150), 7)
    input_initX = Entry(Point(250, 200), 7)

    input_transient.setText("1000")
    input_iterations.setText("300")
    input_initX.setText("0.123")

    input_transient.draw(menu)
    input_iterations.draw(menu)
    input_initX.draw(menu)

    # Draw a SetValue Button
    setValue = Rectangle(Point(150, 250), Point(250, 290))
    setValue.setFill(bg_color)
    setValue.setOutline(ln_color)
    setValue.draw(menu)

    text_setValue = Text(Point(200, 270), "Set Values")
    text_setValue.setTextColor(ln_color)
    text_setValue.draw(menu)

    # Draw a Button for zoom
    zoomButton = Rectangle(Point(10, 300), Point(100, 390))
    zoomButton.setFill(bg_color)
    zoomButton.setOutline(ln_color)
    zoomButton.draw(menu)

    text_zoom = Text(Point(55,345), "Zoom Mode")
    text_zoom.setTextColor(ln_color)
    text_zoom.draw(menu)

    # Draw a Button for getPeriod

    periodButton = Rectangle(Point(300, 300), Point(390, 390))
    periodButton.setFill(bg_color)
    periodButton.setOutline(ln_color)
    periodButton.draw(menu)

    text_period = Text(Point(345, 345), "Get Period")
    text_period.setTextColor(ln_color)
    text_period.draw(menu)

    # Draw a quit button
    quitButton = Rectangle(Point(150, 300), Point(250, 340))
    quitButton.setFill(bg_color)
    quitButton.setOutline(ln_color)
    quitButton.draw(menu)

    quitText = Text(Point(200, 320), "Close")
    quitText.setTextColor(ln_color)
    quitText.draw(menu)

    # Draw an output Message
    output = Text(Point(200, 370), "")
    output.setTextColor(ln_color)
    output.draw(menu)
    
    """ Processing of the Bifurcation Program """
    while(process):
        # Wait for the user to click on the menu
        click = menu.getMouse()

        if(click.getX() > 150 and click.getX() < 250):
            
            # If the user clicks the setValue Button...
            if(click.getY() > 250 and click.getY() < 290):
                
                # Clear the graph
                winBifurcation.clear()
                
                # Set the values to what is in the entry objects
                transient = eval(input_transient.getText())
                iterations = eval(input_iterations.getText())
                initX = eval(input_initX.getText())

                # Display "Graphing" on output
                output.setText("graphing...")
                
                # Draw the Bifurcation Diagram
                a = 0
                while a < 4.0:
                    x = initX
                    for n in range(transient):
                        x = a * x * (1 - x)
                    for n in range(iterations):
                        x = a * x * (1 - x)
                        winBifurcation.plot(a,x, ln_color)
                    a = a + 0.01
                update()
                output.setText("")
                
            # If the user clicks the quit button...
            if(click.getY() > 300 and click.getY() < 340):
                # Turn off process and close the windows
                process = False
                winBifurcation.close()
                menu.close()
                
        # If the user clicks the get period button...
        if(click.getX() > 300 and click.getX() < 390):
            if(click.getY() > 300 and click.getY() < 390):

                # Display get period instructions on output
                output.setText("Click a point on the graph")

                # Wait for the user to click on the Graph
                point_a = winBifurcation.getMouse()

                # Based on the 'a' value of that point, return the periodicity
                period_a = getPeriod(point_a.getX(), 1000000, 1000, 0.0001)
                output.setText(period_a)
                
                

        # If the user clicks the zoom button...
        if(click.getX() > 10 and click.getX() < 100):
            if(click.getY() > 300 and click.getY() < 390):

                # Display zoom mode instructions on output
                output.setText("Click the upper left bound")

                # Wait for the first click on the Graph
                upperLeft = winBifurcation.getMouse()

                # Display zoom mode instructions on output
                output.setText("Click the lower right bound")

                # Wait for the second click on the Graph
                bottomRight = winBifurcation.getMouse()

                # Calculate the proper coordinates and check for error
                if(bottomRight.getX() <= upperLeft.getX() or upperLeft.getY() <= bottomRight.getY()):

                    #Output error message
                    output.setText("error: zoom mode disabled")

                else:
                    # Output zooming message
                    output.setText("zooming...")
                    
                    leftX = upperLeft.getX()
                    rightX = bottomRight.getX()
                    topY = upperLeft.getY()
                    bottomY = bottomRight.getY()

                    # Set the coords and replot points
                    winBifurcation.clear()
                    winBifurcation.setCoords(leftX, bottomY, rightX, topY)

                    # Set the values to what is in the entry objects
                    transient = eval(input_transient.getText())
                    iterations = eval(input_iterations.getText())
                    initX = eval(input_initX.getText())

                    # Draw the Bifurcation Diagram
                    a = 0
                    while a < 4.0:
                        x = initX
                        for n in range(transient):
                            x = f(x,a)
                        for n in range(iterations):
                            x = f(x,a)
                            winBifurcation.plot(a,x, ln_color)
                        a = a + 0.01
                    update()
                    output.setText("")


#-----------------------------------------------------------------------------------------------

""" Time Series Diagram Code """

def timeSeries():
    
    # Color Settings
    bg_color = 'black'
    ln_color = 'green'

    # Processing Settings
    process = True

    """ Setting up the interface """
    
    # Draw the Time Series Graph
    winTimeSeries = GraphWin('Time Series Diagram', 800, 400, autoflush = False)
    winTimeSeries.setBackground('black')

    # Open a Graph Menu
    menu = GraphWin('Time Series Menu', 400, 400)
    menu.setBackground(bg_color)

    # Draw labels for instance fields
    text_a = Text(Point(100,50), "A Value:")
    text_transient = Text(Point(100,100), "Number of Transients:")
    text_iterations = Text(Point(100,150), "Number of Iterations:")
    text_initX = Text(Point(100,200), "Initial Value:")

    text_a.setTextColor(ln_color)
    text_transient.setTextColor(ln_color)
    text_iterations.setTextColor(ln_color)
    text_initX.setTextColor(ln_color)

    text_a.draw(menu)
    text_transient.draw(menu)
    text_iterations.draw(menu)
    text_initX.draw(menu)

    # Draw Entry Objects for instance fields
    input_a = Entry(Point(250, 50), 7)
    input_transient = Entry(Point(250, 100), 7)
    input_iterations = Entry(Point(250, 150), 7)
    input_initX = Entry(Point(250, 200), 7)

    input_a.setText("3.8")
    input_transient.setText("1000")
    input_iterations.setText("5000")
    input_initX.setText("0.123")

    input_a.draw(menu)
    input_transient.draw(menu)
    input_iterations.draw(menu)
    input_initX.draw(menu)

    # Draw a Button for zoom
    zoomButton = Rectangle(Point(10, 300), Point(100, 390))
    zoomButton.setFill(bg_color)
    zoomButton.setOutline(ln_color)
    zoomButton.draw(menu)

    text_zoom = Text(Point(55,345), "Zoom Mode")
    text_zoom.setTextColor(ln_color)
    text_zoom.draw(menu)

    # Draw a SetValue Button
    setValue = Rectangle(Point(150, 250), Point(250, 290))
    setValue.setFill(bg_color)
    setValue.setOutline(ln_color)
    setValue.draw(menu)

    text_setValue = Text(Point(200, 270), "Set Values")
    text_setValue.setTextColor(ln_color)
    text_setValue.draw(menu)

    # Draw a quit button
    quitButton = Rectangle(Point(150, 300), Point(250, 340))
    quitButton.setFill(bg_color)
    quitButton.setOutline(ln_color)
    quitButton.draw(menu)

    quitText = Text(Point(200, 320), "Close")
    quitText.setTextColor(ln_color)
    quitText.draw(menu)

    # Draw an output Message
    output = Text(Point(200, 370), "")
    output.setTextColor(ln_color)
    output.draw(menu)

    """ Processing of the Time Series Program """
    while(process):
        # Wait for the user to click on the menu
        click = menu.getMouse()

        if(click.getX() > 150 and click.getX() < 250):
            
            # If the user clicks the setValue Button...
            if(click.getY() > 250 and click.getY() < 290):
                
                # Clear the graph
                winTimeSeries.clear()
                
                # Set the values to what is in the entry objects
                a = eval(input_a.getText())
                transient = eval(input_transient.getText())
                iterations = eval(input_iterations.getText())
                initX = eval(input_initX.getText())

                # Display "Graphing" on output
                output.setText("graphing...")

                # Rescale window according to the iteration and transient
                winTimeSeries.setCoords(transient - 0.03, -0.01, transient + iterations + 1, 1.01)
                
                # Draw the Time Series Diagram
                x = initX
                for n in range(transient):
                    x = f(x,a)
                for n in range(iterations):
                    x = f(x,a)
                    winTimeSeries.plot(n + transient, x, ln_color)
                update()
                output.setText("")
                
            # If the user clicks the quit button
            if(click.getY() > 300 and click.getY() < 340):
                process = False
                winTimeSeries.close()
                menu.close()

        # If the user clicks the zoom button...
        if(click.getX() > 10 and click.getX() < 100):
            if(click.getY() > 300 and click.getY() < 390):

                # Display zoom mode instructions on output
                output.setText("Click the upper left bound")

                # Wait for the first click on the Graph
                upperLeft = winTimeSeries.getMouse()

                # Display zoom mode instructions on output
                output.setText("Click the lower right bound")

                # Wait for the second click on the Graph
                bottomRight = winTimeSeries.getMouse()

                # Calculate the proper coordinates and check for error
                if(bottomRight.getX() <= upperLeft.getX() or upperLeft.getY() <= bottomRight.getY()):

                    # Output error message
                    output.setText("error: zoom mode disabled")

                else:
                    # Output zooming message
                    output.setText("zooming...")
                    
                    leftX = upperLeft.getX()
                    rightX = bottomRight.getX()
                    topY = upperLeft.getY()
                    bottomY = bottomRight.getY()

                    # Set the coords and replot points
                    winTimeSeries.clear()
                    winTimeSeries.setCoords(leftX, bottomY, rightX, topY)

                    # Set the values to what is in the entry objects
                    a = eval(input_a.getText())
                    transient = eval(input_transient.getText())
                    iterations = eval(input_iterations.getText())
                    initX = eval(input_initX.getText())

                    # Draw the Time Series Diagram
                    x = initX
                    for n in range(transient):
                        x = f(x,a)
                    for n in range(iterations):
                        x = f(x,a)
                        winTimeSeries.plot(n + transient, x, ln_color)
                    update()
                    output.setText("")

#-----------------------------------------------------------------------------------------------

""" CobWeb Diagram Code """

def cobWeb():

    # Color Settings
    bg_color = 'black'
    ln_color = 'green'

    # Processing Settings
    process = True

    """ Setting up the interface """

    # Draw the window (setCoords is based on x_t vs x_t+1)
    winCobWeb = GraphWin('CobWeb Graph', 400, 400, autoflush = False)
    winCobWeb.setBackground('black')

    # All graphing should fall underneath 1 on both axis
    winCobWeb.setCoords(-0.05, -0.02, 1.01, 1.01)

    # Draw the Axis
    yAxis = Line(Point(0, -0.02), Point(0, 1.01))
    yAxis.setOutline('green')
    yAxis.draw(winCobWeb)

    xAxis = Line(Point(-0.05, 0), Point(1.01, 0))
    xAxis.setOutline('green')
    xAxis.draw(winCobWeb)
    
    # Open a Graph Menu
    menu = GraphWin('CobWeb Menu', 400, 400)
    menu.setBackground(bg_color)

    # Draw labels for instance fields
    text_a = Text(Point(100,50), "A Value:")
    text_transient = Text(Point(100,100), "Number of Transients:")
    text_iterations = Text(Point(100,150), "Number of Iterations:")
    text_initX = Text(Point(100,200), "Initial Value:")

    text_a.setTextColor(ln_color)
    text_transient.setTextColor(ln_color)
    text_iterations.setTextColor(ln_color)
    text_initX.setTextColor(ln_color)

    text_a.draw(menu)
    text_transient.draw(menu)
    text_iterations.draw(menu)
    text_initX.draw(menu)

    # Draw Entry Objects for instance fields
    input_a = Entry(Point(250, 50), 7)
    input_transient = Entry(Point(250, 100), 7)
    input_iterations = Entry(Point(250, 150), 7)
    input_initX = Entry(Point(250, 200), 7)

    input_a.setText("3.8")
    input_transient.setText("1000")
    input_iterations.setText("100")
    input_initX.setText("0.123")

    input_a.draw(menu)
    input_transient.draw(menu)
    input_iterations.draw(menu)
    input_initX.draw(menu)

    # Draw a SetValue Button
    setValue = Rectangle(Point(150, 250), Point(250, 290))
    setValue.setFill(bg_color)
    setValue.setOutline(ln_color)
    setValue.draw(menu)

    text_setValue = Text(Point(200, 270), "Set Values")
    text_setValue.setTextColor(ln_color)
    text_setValue.draw(menu)

    # Draw a Button for zoom
    zoomButton = Rectangle(Point(10, 300), Point(100, 390))
    zoomButton.setFill(bg_color)
    zoomButton.setOutline(ln_color)
    zoomButton.draw(menu)

    text_zoom = Text(Point(55,345), "Zoom Mode")
    text_zoom.setTextColor(ln_color)
    text_zoom.draw(menu)

    # Draw a quit button
    quitButton = Rectangle(Point(150, 300), Point(250, 340))
    quitButton.setFill(bg_color)
    quitButton.setOutline(ln_color)
    quitButton.draw(menu)

    quitText = Text(Point(200, 320), "Close")
    quitText.setTextColor(ln_color)
    quitText.draw(menu)

    # Draw an output Message
    output = Text(Point(200, 370), "")
    output.setTextColor(ln_color)
    output.draw(menu)

    """ Processing of the Bifurcation Program """
    while(process):
        # Wait for the user to click on the menu
        click = menu.getMouse()

        if(click.getX() > 150 and click.getX() < 250):
            
            # If the user clicks the setValue Button...
            if(click.getY() > 250 and click.getY() < 290):
                
                # Close the previous graph
                winCobWeb.close()
                
                # Set the values to what is in the entry objects
                a = eval(input_a.getText())
                transient = eval(input_transient.getText())
                iterations = eval(input_iterations.getText())
                initX = eval(input_initX.getText())

                # Draw the window (setCoords is based on x_t vs x_t+1)
                winCobWeb = GraphWin('CobWeb Graph', 400, 400, autoflush = False)
                winCobWeb.setBackground('black')

                # All graphing should fall underneath 1 on both axis
                winCobWeb.setCoords(-0.05, -0.02, 1.01, 1.01)

                # Draw the Axis
                yAxis = Line(Point(0, -0.02), Point(0, 1.01))
                yAxis.setOutline('green')
                yAxis.draw(winCobWeb)

                xAxis = Line(Point(-0.05, 0), Point(1.01, 0))
                xAxis.setOutline('green')
                xAxis.draw(winCobWeb)

                # Draw the function and the x = x line
                n = 0
                while n<=1:
                    # Plot x = x
                    winCobWeb.plot(n, n, 'green')

                    # Plot f(x)
                    winCobWeb.plot(n, f(n,a), 'green')
                    n += 0.0001

                # Display "Graphing" on output
                output.setText("graphing...")
                
                # Draw the Cob Web Diagram
                x = initX
                for i in range(iterations):
                    xPrev = x
                    x = f(x,a)
                    h_line = Line(Point(xPrev, x), Point(x,x))
                    h_line.setFill('blue')
                    v_line = Line(Point(x,x), Point(x,f(x,a)))
                    v_line.setFill('orange')
                    
                    h_line.draw(winCobWeb)
                    update()
                    v_line.draw(winCobWeb)
                    update()
        
                output.setText("")
                
            # If the user clicks the quit button
            if(click.getY() > 300 and click.getY() < 340):
                process = False
                winCobWeb.close()
                menu.close()

        # If the user clicks the zoom button...
        if(click.getX() > 10 and click.getX() < 100):
            if(click.getY() > 300 and click.getY() < 390):

                # Display zoom mode instructions on output
                output.setText("Click the upper left bound")

                # Wait for the first click on the Graph
                upperLeft = winCobWeb.getMouse()

                # Display zoom mode instructions on output
                output.setText("Click the lower right bound")

                # Wait for the second click on the Graph
                bottomRight = winCobWeb.getMouse()

                # Calculate the proper coordinates and check for error
                if(bottomRight.getX() <= upperLeft.getX() or upperLeft.getY() <= bottomRight.getY()):

                    # Output error message
                    output.setText("error: zoom mode disabled")

                else:
                    # Output zooming message
                    output.setText("zooming...")
                    
                    leftX = upperLeft.getX()
                    rightX = bottomRight.getX()
                    topY = upperLeft.getY()
                    bottomY = bottomRight.getY()

                    # Set the coords and replot points
                    winCobWeb.clear()
                    winCobWeb.setCoords(leftX, bottomY, rightX, topY)

                    # Set the values to what is in the entry objects
                    a = eval(input_a.getText())
                    transient = eval(input_transient.getText())
                    iterations = eval(input_iterations.getText())
                    initX = eval(input_initX.getText())

                    # Draw the function and the x = x line
                    n = 0
                    while n<=1:
                        # Plot x = x
                        winCobWeb.plot(n, n, 'green')

                        # Plot f(x)
                        winCobWeb.plot(n, f(n,a), 'green')
                        n += 0.0001

                    output.setText("")

#-----------------------------------------------------------------------------------------------


""" Logistic Function """

def f(x,a):
    return a * x * (1 - x)

""" getPeriod function """

def getPeriod(a, maxPeriod, numTransients, tol):
    infinity = float('inf')
    
    # randomly generate a starting x-value
    x = random.uniform(0, 1)

    # iterate it by the numTransients
    x = iterate(numTransients, x, a)

    # iterate the function until a period is found or the period exceeds the maxPeriod
    periodCount = 1
    initX = f(x,a)
    x = f(initX,a)
    
    while(abs(x - initX) > tol and periodCount < maxPeriod):
        x = f(x,a)
        periodCount += 1
        
    if(periodCount == maxPeriod or periodCount > maxPeriod):
        return infinity
    return periodCount

def iterate(n, x, a):
    for i in range(n):
        x = f(x,a)
    return x


if __name__ == "__main__":
    main()

                
