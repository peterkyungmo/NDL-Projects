# Mandelbrot Set Explorer
# Peter Kang
# v 1.1

from pkg.graphics import*

def T(z,c):
    return z * z + c

def main():

    # Processing Settings
    process = True
    
    # Parameters
    c = complex(0,0)
    x = -3
    escapeRadius = 20
    maxIters = 30
    stepSize = 0.01
    bg_color = 'black'
    ln_color = 'white'

    # Input Window
    menu = GraphWin("Menu", 400, 400)
    menu.setBackground(bg_color)

    # Draw labels for instance fields
    text_cVal = Text(Point(100,100), "C Value:")
    text_escRadius = Text(Point(100,150), "Escape Radius:")
    text_maxIters = Text(Point(100,200), "Max Iterations:")

    text_cVal.setTextColor(ln_color)
    text_escRadius.setTextColor(ln_color)
    text_maxIters.setTextColor(ln_color)

    text_cVal.draw(menu)
    text_escRadius.draw(menu)
    text_maxIters.draw(menu)

    # Draw Entry Objects for instance fields
    input_cVal = Entry(Point(250, 100), 15)
    input_escRadius = Entry(Point(250, 150), 15)
    input_maxIters = Entry(Point(250, 200), 15)

    input_cVal.setText("complex(0,0)")
    input_escRadius.setText("20")
    input_maxIters.setText("30")

    input_cVal.draw(menu)
    input_escRadius.draw(menu)
    input_maxIters.draw(menu)

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
    
    
    # Graph Window for Julius Sets
    winJset = GraphWin("Jsets", 600, 600, autoflush = False)
    winJset.setBackground(bg_color)
    winJset.setCoords(-3,-3,3,3)

    # Graph the initial Jset
    output.setText("graphing...")
    # Escape Algorithm
    while(x < 3):
        y = -3
        while(y < 3):
            z0 = complex(x,y)
            numIters = 0
            color = 'white'
            while(abs(z0) < escapeRadius) and (numIters < maxIters):
                z0 = T(z0,c)
                numIters += 1
            # Changes the color if it escaped
            color = escape(numIters, maxIters)
            winJset.plot(x,y,color)
            y += stepSize
        x += stepSize
    update()
    output.setText("")
    x = -3
    
    

    # Processing of the Program
    while(process):
        # Wait for the user to click on the menu
        click = menu.getMouse()

        if(click.getX() > 150 and click.getX() < 250):
            
            # If the user clicks the setValue Button...
            if(click.getY() > 250 and click.getY() < 290):
                
                # Clear the graph
                winJset.clear()
                
                # Set the values to what is in the entry objects
                c = eval(input_cVal.getText())
                escapeRadius = eval(input_escRadius.getText())
                maxIters = eval(input_maxIters.getText())

                # Display "Graphing" on output
                output.setText("graphing...")
                
                # Draw the Jset Graph
                # Escape Algorithm
                while(x < 3):
                    y = -3
                    while(y < 3):
                        z0 = complex(x,y)
                        numIters = 0
                        color = 'white'
                        while(abs(z0) < escapeRadius) and (numIters < maxIters):
                            z0 = T(z0,c)
                            numIters += 1
                        # Changes the color if it escaped
                        color = escape(numIters, maxIters)
                        winJset.plot(x,y,color)
                        y += stepSize
                    x += stepSize
                update()
                output.setText("")
                x = -3

            # If the user clicks the quit button...
            if(click.getY() > 300 and click.getY() < 340):
                # Turn off process and close the windows
                process = False
                winJset.close()
                menu.close()


def escape(n,maxIt):
    if(n < maxIt):
        return color_rgb(int(n / maxIt * 255), int(n / maxIt * 255), int(n / maxIt * 255))
    return 'white'
    

if __name__ == "__main__":
    main()
