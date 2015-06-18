__author__ = 'zhengwang'

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from random import randint
from kivy.uix.slider import Slider
from kivy.core.window import Window
from fish import Fish


class FlockingDemo(Widget):

    flock_list = []
    cohesion_weight = 0.8
    alignment_weight = 0.5
    separation_weight = 0.3
    view_angle = 75             #field of view angle

    def __init__(self, **kwargs):
        super(FlockingDemo, self).__init__(**kwargs)
        self.add_slider()
        self.add_fish()

    def add_fish(self):
        """
        add 20 fish

        """
        for i in range(0, 20):
            fish = Fish()
            fish.init_pos()
            fish.angle = randint(0, 360)
            fish.velocity = Vector(-3, 0).rotate(fish.angle)
            self.add_widget(fish)
            self.flock_list.append(fish)

    def compute_cohesion(self, current_fish):

        """
        calculate cohesion vector and return this value
        :param current_fish:
        :return:
        """
        neighbor_count = 0.0        # internal use
        vector = Vector(0, 0)       # internal use

        for fish in self.flock_list:
            angle_to_neighbor = current_fish.velocity.angle(fish.pos)       # angle between self and neighbor
            d = Vector(fish.pos).distance(current_fish.pos)                 # distance between self and neighbor
            if fish != current_fish:
                if 0 < d < 150:                                             # cohesion radius is set to 150
                    # check if neighbor in in the field of view
                    if current_fish.angle - self.view_angle < angle_to_neighbor < current_fish.angle + self.view_angle:
                        vector += Vector(fish.pos)                          # sum neighbor's pos
                        neighbor_count += 1

        if neighbor_count > 0:
            vector_ave = vector / neighbor_count                            # average sum of pos as a new vector
            vector = (vector_ave - Vector(current_fish.pos)).normalize()    # normalize the vector
            steer = (vector - current_fish.velocity)                        # calculate steering
            return self.limit(steer, 0.05)                            # set speed limit
        else:
            return vector

    def compute_alignment(self, current_fish):
        neighbor_count = 0.0
        vector = Vector(0, 0)
        for fish in self.flock_list:
            angle_to_neighbor = current_fish.velocity.angle(fish.pos)
            d = Vector(fish.pos).distance(current_fish.pos)
            if fish != current_fish:
                if 0 < d < 100:
                    if current_fish.angle - self.view_angle < angle_to_neighbor < current_fish.angle + self.view_angle:
                        vector += fish.velocity                             # sum neighbor's velocity
                        neighbor_count += 1
        if neighbor_count > 0:
            vector = vector / neighbor_count
        return self.limit(vector, 0.05)

    def compute_separation(self, current_fish):

        neighbor_count = 0.0
        vector = Vector(0, 0)

        for fish in self.flock_list:
            angle_to_neighbor = current_fish.velocity.angle(fish.pos)
            d = Vector(fish.pos).distance(current_fish.pos)
            if fish != current_fish:
                if 0 < d < 50:
                    if current_fish.angle - self.view_angle < angle_to_neighbor < current_fish.angle + self.view_angle:
                        # negate the vector and normalize it
                        vector += (Vector(current_fish.pos) - Vector(fish.pos)).normalize()
                        neighbor_count += 1

        if neighbor_count > 0:
            vector = vector / neighbor_count
        return vector

    def update(self, dt):

        for i in self.flock_list:

            i.move()

            cohesion = self.compute_cohesion(i) * self.cohesion_weight
            alignment = self.compute_alignment(i) * self.alignment_weight
            separation = self.compute_separation(i) * self.separation_weight

            vector = (cohesion + alignment + separation)        # sum three vectors

            i.angle = i.velocity.angle(i.pos)                   # set heading angle
            i.velocity = (vector + i.velocity).normalize()*2    # set new velocity

            # wrapping
            if i.y < 0:
                i.y = i.y + self.height
            if i.top > self.height:
                i.y = i.y - self.height
            if i.x < 0:
                i.x = i.x + self.width
            if i.right > self.width:
                i.x = i.x - self.width

    @staticmethod
    def limit(vector, max_value):
        """
        limit vector length to max_value
        :param vector:
        :param max_value:
        :return:
        """
        if vector.length() > max_value:
            vector.normalize()
            return vector * max_value
        else:
            return vector

    def add_slider(self):

        """
        add sliders

        """
        box1 = BoxLayout(orientation="vertical", size = (150, 110), pos = (Window.width * 2/7, 0))
        box2 = BoxLayout(orientation="vertical", size = (380, 110), pos = (Window.width * 1/2, 0))

        # Cohesion
        slider1 = Slider(min=0, max=1, value = self.cohesion_weight, step = 0.1)
        label1 = Label(text = "Cohesion: " + str(slider1.value), color = (0,0,0,1))

        # Alignment
        slider2 = Slider(min=0, max=1, value = self.alignment_weight, step = 0.1)
        label2 = Label(text = "Alignment: " + str(slider2.value), color = (0,0,0,1))

        # Separation
        slider3 = Slider(min=0, max=1, value = self.separation_weight, step = 0.1)
        label3 = Label(text = "Separation: " + str(slider3.value), color = (0,0,0,1))

        # Field of View
        slider4 = Slider(min=0, max=180, value = self.view_angle * 2, step = 1)
        label4 = Label(text = "Field of View (degree): " + str(slider4.value), color = (0,0,0,1))

        # bind slider value to label
        def on_value1(object, value):
            self.cohesion_weight = float(value)
            label1.text = "Cohesion: " + str(float(value))

        def on_value2(object, value):
            self.alignment_weight = float(value)
            label2.text = "Alignment: "+ str(float(value))

        def on_value3(object, value):
            self.separation_weight = float(value)
            label3.text = "Separation: " + str(value)

        def on_value4(object, value):
            self.view_angle = float(value)
            label4.text = "Field of View (degree): " + str(value)

        slider1.bind(value = on_value1)
        slider2.bind(value = on_value2)
        slider3.bind(value = on_value3)
        slider4.bind(value = on_value4)

        # add widgets to screen
        box1.add_widget(label1)
        box2.add_widget(slider1)
        box1.add_widget(label2)
        box2.add_widget(slider2)
        box1.add_widget(label3)
        box2.add_widget(slider3)
        box1.add_widget(label4)
        box2.add_widget(slider4)
        self.add_widget(box1)
        self.add_widget(box2)

class FlockingDemoApp(App):
    def build(self):
        game = FlockingDemo()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    FlockingDemoApp().run()
