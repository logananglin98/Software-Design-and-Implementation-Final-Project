######################################################################
# Authors: Logan Anglin and Sara Adhikari
# Usernames: anglinl, adhikaris
#
# Assignment: P01 Final Project
#
# Purpose: Create an interactive turtle art program.
#
######################################################################
# Acknowledgements:
#
#
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import turtle
import tkinter as tk
import random
import ctypes


class TurtleArtGUI:
    def __init__(self, window_text="Turtle Art"):
        self.root = tk.Tk()
        self.root.minsize(width=400, height=200)
        self.root.title(window_text)

        # For getting the screen resolution from the OS and using it for the turtle window.
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()

        self.num_of_sides = tk.IntVar()
        self.num_of_sides.set(6)  # Initial number of sides
        self.side_length = tk.IntVar()
        self.side_length.set(50)
        self.is_random = False  # Will be set to True if the user clicks random button or pushes r.
        self.is_paused = False  # User can use this to pause the program.
        self.on_click_input = False  # Changes when the user clicks within the turtle window.
        self.running = False  # Keeps the user from creating new turtle objects with the draw shape button.
        self.x_from_click = 0
        self.y_from_click = 0
        self.setup_gui()

    def setup_gui(self):
        self.message_label = tk.Label(self.root, text='Press "C" to show or hide controls'
                                                      '\nwhile the program is executing'
                                                      '\n\nSelect the number of sides:')
        self.message_label.pack()

        # Create a dropdown for selecting the number of sides
        sides_options = list(range(3, 16))  # Options from 3 to 15 sides
        self.side_dropdown = tk.OptionMenu(self.root, self.num_of_sides, *sides_options)
        self.side_dropdown.pack()

        self.myButton1 = tk.Button(self.root, text="Draw Shape (or press enter)", command=self.draw_shape_from_input)
        self.myButton1.pack()

        self.increase_sides_button = tk.Button(self.root, text='Increase Sides (or press "A" key)',
                                               command=self.increase_sides)
        self.increase_sides_button.pack()

        self.decrease_sides_button = tk.Button(self.root, text='Decrease Sides (or press "D" key)',
                                               command=self.decrease_sides)
        self.decrease_sides_button.pack()

        self.increase_size_button = tk.Button(self.root, text='Increase Size (or press "W" key)',
                                              command=self.increase_size)
        self.increase_size_button.pack()

        self.decrease_size_button = tk.Button(self.root, text='Decrease Size (or press "S" key)',
                                              command=self.decrease_size)
        self.decrease_size_button.pack()

        self.randomize_button = tk.Button(self.root, text='Randomize (or press "R" key)',
                                          command=self.randomize)
        self.randomize_button.pack()

        self.pause_button = tk.Button(self.root, text='Pause/Unpause Program (or press space bar)',
                                      command=self.pause)
        self.pause_button.pack()

        self.quit_button = tk.Button(self.root, text='Quit Program (or press "Q" key)',
                                     command=self.quit)
        self.quit_button.pack()

        self.myTextLabel1Text = tk.StringVar()
        self.myTextLabel1 = tk.Label(self.root, textvariable=self.myTextLabel1Text)
        self.myTextLabel1.pack()

        self.myTextLabel2Text = tk.StringVar()
        self.myTextLabel2 = tk.Label(self.root, textvariable=self.myTextLabel2Text)
        self.myTextLabel2.pack()

        # Keybinds for controlling the execution of the program if the user chooses not to use the GUI.
        self.root.bind("<KeyPress-Return>", self.draw_shape_from_input_key)  # Initiates the turtle and draws shapes.
        self.root.bind("<KeyPress-a>", self.increase_sides_key)  # For changing the shape.
        self.root.bind("<KeyPress-d>", self.decrease_sides_key)
        self.root.bind("<KeyPress-w>", self.increase_size_key)  # For changing the size of the shape.
        self.root.bind("<KeyPress-s>", self.decrease_size_key)
        self.root.bind("<KeyPress-r>", self.randomize_key)  # Randomizes the shape and shape size.
        self.root.bind("<KeyPress-space>", self.pause_key)  # Pauses the program unitl the user hits the space again.
        self.root.bind("<KeyPress-q>", self.quit_key)  # Immediately closes the program.

        self.root.mainloop()

    def increase_sides(self):
        self.is_random = False
        if self.num_of_sides.get() < 15:
            self.num_of_sides.set(self.num_of_sides.get() + 1)
            self.shape_dimensions()
        elif not self.is_paused:
            self.myTextLabel1Text.set("Number of sides cannot be increased further")

    def decrease_sides(self):
        self.is_random = False
        if self.num_of_sides.get() > 3:
            self.num_of_sides.set(self.num_of_sides.get() - 1)
            self.shape_dimensions()
        elif not self.is_paused:
            self.myTextLabel1Text.set("Number of sides cannot be decreased further")

    def increase_size(self):
        self.is_random = False
        if self.side_length.get() < 100:
            self.side_length.set(self.side_length.get() + 5)
            self.shape_dimensions()
        elif not self.is_paused:
            self.myTextLabel2Text.set("Shapes can not be any larger.")

    def decrease_size(self):
        self.is_random = False
        if self.side_length.get() > 5:
            self.side_length.set(self.side_length.get() - 5)
            self.shape_dimensions()
        elif not self.is_paused:
            self.myTextLabel2Text.set("Shapes can not be any smaller.")

    def bring_controls_to_front(self):
        """
        Brings the GUI window listing controls and buttons in front of the turtle window using the C key. Hides the
        controls when the user types C again. Uses self.is_hidden to do the appropriate action.
        :return:
        """
        if self.is_hidden:
            self.root.lift()
            self.is_hidden = False
        else:
            self.root.lower()
            self.is_hidden = True

    def randomize(self):
        """
        Sets is_random to True. This controls an if statement in the draw_shape_from_input function that will randomize
        the shape and shape size instead of using what is currently set for those values. This is set up so these
        random values change each time.
        :return:
        """
        self.is_random = True
        self.shape_dimensions()

    def pause(self):
        """
        The program will finish drawing whatever shape it is currently drawing and then wait until the user hits the
        pause button again or closes the program. Sets the text labels so the user knows the program is paused.
        :return:
        """
        if not self.is_paused:
            self.pause_turtle.write("The program is paused!", False, "center", ("Comic Sans", 20, "normal"))

            self.is_paused = True
            self.myTextLabel1Text.set(f"The program is paused!")
            self.myTextLabel2Text.set("")
        else:
            self.is_paused = False
            self.shape_dimensions()
            self.pause_turtle.clear()

    def quit(self):
        """
        Immediately stops the program when activated by the user.
        :return:
        """
        turtle.bye()
        exit()

    # All functions ending with "key" are event loggers for if the user uses the keyboard controls instead of the
    # buttons provided by the setup_gui() function.
    def draw_shape_from_input_key(self, event):
        self.draw_shape_from_input()

    def increase_sides_key(self, event):
        self.increase_sides()

    def decrease_sides_key(self, event):
        self.decrease_sides()

    def increase_size_key(self, event):
        self.increase_size()

    def decrease_size_key(self, event):
        self.decrease_size()

    def randomize_key(self, event):
        self.randomize()

    def pause_key(self, event):
        self.pause()

    def quit_key(self, event):
        self.quit()

    def shape_dimensions(self):
        """
        Uses the text labels initialized above to inform the user of the dimensions they have chosen. The
        pause function also uses these text labels.
        :return:
        """
        if not self.is_paused:
            if self.is_random:
                self.myTextLabel1Text.set(f"Number of sides is randomized!")
                self.myTextLabel2Text.set(f"Shape size is randomized!")
            else:
                self.myTextLabel1Text.set(f"Number of sides: {self.num_of_sides.get()}")
                self.myTextLabel2Text.set(f"Size of Shape: {self.side_length.get()}")

    def h1(self, x, y):
        """
        The user can click somewhere within the turtle window and the next shape will draw in that area. This is coded
        so the turtle will go back to drawing the shapes in random locations after a shape is drawn where the user
        clicks using the on_click_input variable.
        :param x: The x coordinate of where the user clicks.
        :param y: The y coordinate of where the user clicks.
        :return:
        """
        self.on_click_input = True
        self.x_from_click = x
        self.y_from_click = y

    def draw_shape_from_input(self):
        """
        Adds user-chosen parameters to the draw_shape() function so the user can control the shapes and the execution
        of the program.
        :return:
        """
        # Main turtle for drawing.
        if not self.running:
            self.running = True
            self.wn = turtle.Screen()
            self.wn.title("Press C to show/hide controls. Press space to pause the program. Press Q to quit.")
            self.wn.setup(self.window_width, self.window_height, 0, 0)
            self.t = turtle.Turtle()
            self.is_hidden = True  # Assists in the execution of the bring_controls_to_front function.

            # These lines create a turtle object that notifies the user of the program being paused via text when the pause
            # function is used.
            self.pause_turtle = turtle.Turtle()
            self.pause_turtle.hideturtle()
            self.pause_turtle.penup()

            self.wn.listen()

            self.wn.onclick(self.h1)

            # These are for if the user clicks on the turtle window. For some reason, the key binds in the _init_ area do
            # not work if the turtle window has been clicked on.
            self.wn.onkey(self.bring_controls_to_front, "c")
            self.wn.onkey(self.increase_sides, "a")
            self.wn.onkey(self.decrease_sides, "d")
            self.wn.onkey(self.increase_size, "w")
            self.wn.onkey(self.decrease_size, "s")
            self.wn.onkey(self.randomize, "r")
            self.wn.onkey(self.pause, "space")
            self.wn.onkey(self.quit, "q")

            self.shape_dimensions()  # Shows the initial dimensions when the user starts running the program.
            while True:  # Infinite loop.
                while not self.is_paused:  # Runs the loop as long as the user hasn't hit the passe button.
                    self.t.showturtle()
                    self.t.penup()

                    # Used for checking if the user has utilized the h1 click handler.
                    if self.on_click_input:
                        self.on_click_input = False
                        self.t.goto(self.x_from_click, self.y_from_click)
                    else:  # If the user hasn't clicked on the Python window.
                        self.t.goto(random.randint(-700, 700), random.randint(-300, 300))

                    self.t.pendown()  # Draws shape
                    self.t.speed(0)  # Just so the user doesn't have to watch the turtle spin for a bit.
                    self.t.left(random.randint(0, 359))
                    self.t.speed(4)
                    self.t.begin_fill()
                    if self.is_random:  # Checks if the random button has been used.
                        self.draw_shape(self.t, random.randint(3, 15), random.randint(5, 100))
                    else:  # For if the user has specified dimensions and is not using the randomize function.
                        self.draw_shape(self.t, self.num_of_sides.get(), self.side_length.get())  # Use a default size of 50
                    self.t.end_fill()

                    self.shape_dimensions()  # keeps dimensions info up-to-date.

                # I only added this hideturtle() function and the showturtle() function above because the program
                # crashes if there is no code to run while the inner while loop is not executing.
                self.t.hideturtle()

    @staticmethod
    def draw_shape(turt, num_of_sides=6, side_length=50):
        turt.color((random.random(), random.random(), random.random()))

        for num in range(num_of_sides):
            turt.forward(side_length)
            # Uses a formula to draw a closed, equal-sided shape.
            turt.left((180 - (((num_of_sides - 2) * 180) / num_of_sides)))


def main():
    # This line lets the get_resolution method in the turtle_art_gui class get the correct resolution.
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    turtle_art_gui = TurtleArtGUI()


if __name__ == "__main__":
    main()
