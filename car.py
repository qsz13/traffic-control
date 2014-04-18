from cocos.sprite import Sprite
from cocos import euclid
import pyglet
import pyglet.image as image
import time
from cocos import collision_model

__author__ = 'danielqiu'


class Car(Sprite, pyglet.event.EventDispatcher):
    def __init__(self, type, lane):
        self.previous_car = None
        self.in_map = True
        self.following = None
        self.car_normal_image = image.create(50, 50, image.SolidColorImagePattern(color=(0, 0, 255, 255)))
        self.car_emergency_image = image.create(50, 50, image.SolidColorImagePattern(color=(255, 0, 0, 255)))
        self.lane = lane
        self.type = type
        self.from_direction = lane.get_from()
        self.appear_time = time.time()
        self.removed = False
        self.has_started = False
        self.state = "running"
        self.has_set_occupied = False
        self.has_unset_occupied = False
        # self.stoppable = True
        if self.type is "normal":
            super(Car, self).__init__(self.car_normal_image)
        elif self.type is "emergency":
            super(Car, self).__init__(self.car_emergency_image)

        if self.from_direction is "north":
            self.position = (350, 850)
        if self.from_direction is "east":
            self.position = (850, 450)
        if self.from_direction is "south":
            self.position = (450, -50)
        if self.from_direction is "west":
            self.position = (-50, 350)

        pyglet.clock.schedule_interval(self.traffic_light_control, 0.01)

    def distance(self,car):
        return ((self.position[0]-car.position[0])**2 + (self.position[1]-car.position[1])**2)**(1/2.0)

    def set_wait(self):
        if self.has_started and self.state is "running":
            self.state = "waiting"
            # print self.type
            if self.type is "normal":
                self.lane.waiting_normal_car += 1
                print self.lane.waiting_normal_car
            if self.type is "emergency":
                self.lane.waiting_emergency_car += 1
                # print self.lane.waiting_normal_car

    def set_running(self):
        if self.has_started and self.state is "waiting":
            # self.resume()
            self.state = "running"
            if self.type is "normal":
                self.lane.waiting_normal_car -= 1
            if self.type is "emergency":
                self.lane.waiting_emergency_car -= 1

    def set_has_started(self):
        self.has_started = True

    def traffic_light_control(self, t):

        if 275 < self.position[0] < 525 and 275 < self.position[1] < 525:
            if not self.has_set_occupied:
                self.has_set_occupied = True
                self.lane.map.central_occupied += 1
        else:
            if self.has_set_occupied and not self.has_unset_occupied:
                self.has_unset_occupied = True
                self.lane.map.central_occupied -= 1

        if not self.removed:

            if self.previous_car:
                # print self.distance(self.previous_car)
                if self.distance(self.previous_car) < 70:
                    self.set_wait()
                    self.pause()
                else:
                    self.set_running()
                    self.resume()

            if self.from_direction is "north":

                if 530 < self.position[1] < 540 and self.lane.map.from_north_light.is_red():
                    self.set_wait()
                    self.pause()
                elif 530 < self.position[1] < 540 and self.lane.map.from_north_light.is_green():
                    self.set_running()
                    self.resume()

                if self.position[1] < 375:
                    self.in_map = False
                    if not self.removed:
                        self.lane.remove_car()
                        self.removed = True
                        if self.following:
                            # print "remove",self.following.previous_car
                            self.following.previous_car = None

            if self.from_direction is "south":


                if 260 < self.position[1] < 270 and self.lane.map.from_south_light.is_red():
                    self.set_wait()
                    self.pause()
                elif 260 < self.position[1] < 270 and self.lane.map.from_south_light.is_green():
                    self.set_running()
                    self.resume()

                if self.position[1] > 350:
                    self.in_map = False
                    if not self.removed:
                        self.lane.remove_car()
                        self.removed = True
                        if self.following:
                            self.following.previous_car = None

            if self.from_direction is "east":

                if 530 < self.position[0] < 540 and self.lane.map.from_east_light.is_red():
                    self.set_wait()
                    self.pause()
                elif 530 < self.position[0] < 540 and self.lane.map.from_east_light.is_green():

                    self.set_running()
                    self.resume()

                if self.position[0] < 350:
                    self.in_map = False
                    if not self.removed:
                        self.lane.remove_car()
                        self.removed = True
                        if self.following:
                            self.following.previous_car = None

            if self.from_direction is "west":


                if 260 < self.position[0] < 270 and self.lane.map.from_west_light.is_red():

                    self.set_wait()
                    self.pause()
                elif 260 < self.position[0] < 270 and self.lane.map.from_west_light.is_green():

                    self.set_running()
                    self.resume()

                if self.position[0] > 350:
                    self.in_map = False
                    if not self.removed:
                        self.lane.remove_car()

                        self.removed = True
                        if self.following:
                            self.following.previous_car = None

