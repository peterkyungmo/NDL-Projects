# Koch Curve
# Peter Kang
# v 1.0
from pkg.graphics import *
from math import *

def main():

    # Processing Settings
    process = True
    
    # Parameters
    global win
    global menu
    global bg_color
    global ln_color
    global drawn
    global lines
    
    # Color Settings
    bg_color = 'black'
    ln_color = 'green'

    # Window Settings
    win = GraphWin('Koch Curve', 800, 800, autoflush = False)
    win.setBackground(bg_color)
    win.setCoords(-10, -10, 10, 10)
    
    # Menu Settings
    menu = GraphWin('Menu', 400, 400)
    menu.setBackground(bg_color)
    drawn = False

    # Menu Text
    text_ds = Text(Point(100,50), "Similarity Dimension:")
    text_length = Text(Point(100,100), "Total Length:")
    text_theta = Text(Point(100,150), "Generating Angle:")
    text_level = Text(Point(100,200), "Desired Level:")
    
    text_ds.setTextColor(ln_color)
    text_length.setTextColor(ln_color)
    text_theta.setTextColor(ln_color)
    text_level.setTextColor(ln_color)

    text_ds.draw(menu)
    text_length.draw(menu)
    text_theta.draw(menu)
    text_level.draw(menu)

    text_ds_output = Text(Point(250,50), "")
    text_length_output = Text(Point(250,100), "")

    text_ds_output.setTextColor(ln_color)
    text_length_output.setTextColor(ln_color)

    text_ds_output.draw(menu)
    text_length_output.draw(menu)

    # Menu Entry Objects
    input_theta = Entry(Point(250, 150), 15)
    input_level = Entry(Point(250, 200), 15)

    input_theta.setText("60")
    input_level.setText("5")

    input_theta.draw(menu)
    input_level.draw(menu)

    # Draw/Clear button
    setValue = Rectangle(Point(150, 250), Point(250, 290))
    setValue.setFill(bg_color)
    setValue.setOutline(ln_color)
    setValue.draw(menu)

    text_setValue = Text(Point(200, 270), "Draw/Clear")
    text_setValue.setTextColor(ln_color)
    text_setValue.draw(menu)

    # Quit Button
    quitButton = Rectangle(Point(150, 300), Point(250, 340))
    quitButton.setFill(bg_color)
    quitButton.setOutline(ln_color)
    quitButton.draw(menu)

    quitText = Text(Point(200, 320), "Close")
    quitText.setTextColor(ln_color)
    quitText.draw(menu)

    # Initilaize Starting Parameters
    initialPoint = Point(-9,-5)
    initialLength = 18
    initialAngle = 0

    lines = []

    # Console Notes
    print('Note: Lengths are presented in inches and were measured using a 16:9, 14.0" display running in 1080p')

    # Program processing
    while(process):
        # Wait for the user to click
        click = menu.getMouse()

        if(click.getX() > 150 and click.getX() < 250):
            
            # If the user clicks the Draw Button...
            if(click.getY() > 250 and click.getY() < 290):

                # Check if there is a graph drawn
                if(drawn):

                    # Clear the graph
                    clearKC()

                    # Set drawn to false
                    drawn = False

                else:
                    # Store the new parameters
                    generatingAngle = eval(input_theta.getText())
                    initialLevel = eval(input_level.getText())

                    # Compute and output the similarity dimension and the length of the curve
                    dimension = ds(generatingAngle)
                    length = totalLength(initialLevel, initialLength, generatingAngle)

                    text_ds_output.setText(dimension)
                    text_length_output.setText(str(length) + " inches")

                    # Cap max level at 6
                    if(initialLevel > 6):
                        initialLevel = 6

                    # Draw the graph
                    drawKC(initialPoint, generatingAngle, initialAngle, initialLength, initialLevel)
                    
                    # Set drawn to true
                    drawn = True
                    
            # If the user clicks the quit button...
            if(click.getY() > 300 and click.getY() < 340):
                # Turn off process and close the windows
                process = False
                win.close()
                menu.close()

def drawLine(pt_init, angle, length):
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

    # Draw the line
    newLine = Line(pt_init, pt_final)
    newLine.setOutline(ln_color)
    newLine.draw(win)
    lines.append(newLine)

def scaleFactor(theta):
    return 1 / (2 * (1 + cos(theta * (pi/180))))

def endPoint(pt_init, angle, length):
    angle = angle * (pi/180)
    finalX = (pt_init.getX() + (length * cos(angle)))
    finalY = (pt_init.getY() + (length * sin(angle)))
    return Point(finalX, finalY)

def ds(theta):
    dimension = log(4) / (log(2) + log(1 + cos(theta * (pi/180))))
    return round(dimension, 2)

def totalLength(level, init_length, theta):
    pixel_length = (4 ** level) * (scaleFactor(theta) ** level) * (init_length)
    inch_length = pixel_length * (4.5 / 18)
    return round(inch_length, 1)

def clearKC():
    for idx, val in enumerate(lines):
        val.undraw()
    del lines[:]

def drawKC(pt_init, theta, angle, length, level):
    # Base case if level == 0
    if(level == 0):
        # Draw the four sections
        drawLine(pt_init, angle, length)
        return endPoint(pt_init, angle, length)
        
    else:
        sf = scaleFactor(theta)
        # Compute new angles and length and starting point
        pt_init = drawKC(pt_init, theta, angle, length * sf, level - 1)
        pt_init = drawKC(pt_init, theta, angle + theta, length * sf, level - 1)
        pt_init = drawKC(pt_init, theta, angle - theta, length * sf, level - 1)
        pt_init = drawKC(pt_init, theta, angle, length * sf, level - 1)
    return pt_init

if __name__ == "__main__":
    main()


    
