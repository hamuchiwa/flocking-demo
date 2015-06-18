__author__ = 'zhengwang'

from kivy.properties import NumericProperty
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.core.window import Window
from random import randint

class Fish(Image):
    # velocity of the ball on x and y axis
    velocity_x = 0
    velocity_y = 0
    angle = NumericProperty(0)

    velocity = Vector(0, 0)

    def move(self):
        self.pos = self.velocity + self.pos

    def init_pos(self):
        x = randint(Window.width/2 - 150, Window.width/2 + 150)
        y = randint(Window.height/2 - 150, Window.height/2 + 150)
        self.pos = (x, y)
        print("Pos: " + str(self.pos))
