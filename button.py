from cocos.director import director
from cocos.sprite import Sprite
import pyglet.image as image
from cocos.text import Label
from cocos.menu import MenuItem
import time

__author__ = 'danielqiu'



class Button(Sprite):
    is_event_handler=True

    def __init__(self, type, place, map):
        self.type = type
        self.place = place
        self.map = map
        self.last_click_time = 0

        self.size = None
        if place is "north":
            if type is "normal":
                # self.buttonimage = image.load()
                super(Button, self).__init__("addnormalcar.png" ,position=(200,750))

            elif type is "emergency":
                super(Button, self).__init__("addemergencycar.png" ,position=(200,710))

        elif place is "east":
            if type is "normal":
                # self.buttonimage = image.load()
                super(Button, self).__init__("addnormalcar.png" ,position=(680,600))

            elif type is "emergency":
                super(Button, self).__init__("addemergencycar.png" ,position=(680,560))

        elif place is "south":
            if type is "normal":
                # self.buttonimage = image.load()
                super(Button, self).__init__("addnormalcar.png" ,position=(600,100))

            elif type is "emergency":
                super(Button, self).__init__("addemergencycar.png" ,position=(600,60))

        elif place is "west":
            if type is "normal":
                # self.buttonimage = image.load()
                super(Button, self).__init__("addnormalcar.png" ,position=(90,250))

            elif type is "emergency":
                super(Button, self).__init__("addemergencycar.png" ,position=(90,210))


        self.size =(self.image.width,self.image.height)
    # self.is_end=False
    def on_enter(self):
        super(Button,self).on_enter()
        director.window.push_handlers(self.on_mouse_press)
    def on_exit(self):
        director.window.pop_handlers()
        super(Button,self).on_exit()

    def on_mouse_press(self,x,y,buttons,modifiers):
        if time.time()-self.last_click_time > 0.3:
           if self.position[0]-self.size[0]/2 < x < self.position[0]+self.size[0]/2 and \
                           self.position[1]-self.size[1]/2 < y < self.position[1]+self.size[1]/2:
               self.map.add_car(self.type,self.place)
               self.last_click_time = time.time()






