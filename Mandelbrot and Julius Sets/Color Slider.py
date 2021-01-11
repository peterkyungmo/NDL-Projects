# Color Slider
from pkg.graphics import*

def main():
    # Base colors
    bg_color = 'black'
    ln_color = 'white'

    # Processing Parameter
    process = True

    # Create a new window
    global win
    win = GraphWin("square", 600, 600, autoflush = False)
    win.setBackground(bg_color)

    # Create a square and fill it with a color
    global square
    square = Rectangle(Point(100,100), Point(500,500))
    square.setFill(ln_color)
    square.draw(win)

    # Create a menu window
    global menu
    menu = GraphWin("menu", 400, 400, autoflush = False)
    menu.setBackground(bg_color)

    # Draw the color gradient for the menu
    gradient = Image(Point(200, 300), "img_color_gradient.png")
    gradient.draw(menu)

    # Draw the color slider for the menu
    slider = Rectangle(Point(195,275), Point(205, 325))
    slider.setFill(ln_color)
    slider.draw(menu)

    #

    while(process):
        click = menu.getMouse()
        if(click.getY() > 270 and click.getY() < 330):
            if(click.getX() > 50 and click.getX() < 350):
                slider.undraw()
                slider = Rectangle(Point((click.getX() - 5),275), Point((click.getX() + 5),325))
                slider.setFill(ln_color)
                slider.draw(menu)

main()
