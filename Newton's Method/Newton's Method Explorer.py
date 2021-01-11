# Newton's Method Explorer
# Peter kang
# v 1.0
from graphics import*
from math import*
import cmath as cm

def main():
    function = setFunction()
    print (f(5, function))

def setFunction():
    f = input("Enter the single variable function using (x): ")
    return f

def f(x, function):
    eval(function)

if __name__ == "__main__":
    main()

