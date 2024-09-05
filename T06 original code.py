######################################################################
# Author: Logan
# Username: anglinl
#
# Assignment: T06: Turtle Art
#
# Purpose: Create beautiful works of art through iteration
#
######################################################################
# Acknowledgements:
#   Original Author: Dr. Scott Heggen
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import turtle
import tkinter as tk
import random

class turtle_art:
    def __init__(self, windowtext="Exploring Tkinter"):
        self.root = tk.Tk()
        self.root.minsize(width=250, height=100)
        self.root.maxsize(width=250, height=100)
        self.root.title(windowtext)

        self.count = 0
        self.myButton1 = None
        self.myTextBox1 = tk.Entry(self.root)

        self.myTextLabel1Text = tk.StringVar()
        self.myTextLabel1 = None


    def draw_shape(turt, num_of_sides=6, side_length_amount=50):
        turt.color((random.random(), random.random(), random.random()))

        for num in range(num_of_sides):
            turt.forward(side_length_amount)
            turt.left((180-(((num_of_sides-2)*180)/num_of_sides)))

def main():
    sides = input("Enter how many sides you would like each shape to have, or press enter for each shape "
                  "to have a random number of sides: ")
    wn = turtle.Screen()
    t = turtle.Turtle()

    if sides == "":
        while True:
            t.penup()
            t.goto(random.randint(-300, 300), random.randint(-300, 300))
            t.pendown()
            t.left(random.randint(0, 359))
            t.begin_fill()
            turtle_art.draw_shape(t, random.randint(3, 10), random.randint(5, 100))
            t.end_fill()
        wn.onclick(wn.bye)
    else:
        while True:
            t.penup()
            t.goto(random.randint(-300, 300), random.randint(-300, 300))
            t.pendown()
            t.left(random.randint(0, 359))
            t.begin_fill()
            turtle_art.draw_shape(t, int(sides), random.randint(5, 100))
            t.end_fill()
        wn.onclick(wn.bye)

    wn.mainloop()

if __name__ == "__main__":
    main()
