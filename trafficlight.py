__author__ = 'danielqiu'
from pyglet import image
from cocos.sprite import Sprite




class TrafficLight(Sprite):
    is_event_handler=True

    def __init__(self,position):

        self.signal = "red"
        self.red_image = image.create(50,50,image.SolidColorImagePattern(color=(255,0,0,255)))
        self.green_image = image.create(50,50,image.SolidColorImagePattern(color=(50,205,50,255)))

        super(TrafficLight,self).__init__(self.red_image)
        if position is "north":
            self.position = (250,550)
        if position is "east":
            self.position = (550,550)
        if position is "south":
            self.position = (550, 250)
        if position is "west":
            self.position = (250,250)



    def switch_signal(self):
        if self.signal is "red":
            self.set_green()

        elif self.signal is "green":
            self.set_red()


    def set_green(self):
        self.signal = "green"
        self.image = self.green_image

    def set_red(self):
        self.signal = "red"
        self.image = self.red_image

    def is_red(self):
        if self.signal is "red":
            return True
        else:
            return False

    def is_green(self):
        if self.signal is "green":
            return True
        else:
            return False


