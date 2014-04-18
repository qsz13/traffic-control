from threading import Thread
import thread
import threading
from car import Car
from cocos.actions import MoveBy, Hide, Show
from lane import Lane
from cocos.actions.move_actions import Move
import pyglet

__author__ = 'danielqiu'
from cocos.layer import ColorLayer
from cocos.draw import Line, Canvas
from cocos.sprite import Sprite
import pyglet.image as image
from button import Button
from trafficlight import TrafficLight
from action import CustomizeMoveBy
import time


class TrafficMap(ColorLayer):
    def __init__(self):
        super(TrafficMap, self).__init__(46, 139, 87, 255)
        self.north_stop_line = None
        self.east_stop_line = None
        self.south_stop_line = None
        self.west_stop_line = None
        self.north_normal_button = Button("normal", "north", self)
        self.east_normal_button = Button("normal", "east", self)
        self.south_normal_button = Button("normal", "south", self)
        self.west_normal_button = Button("normal", "west", self)
        self.north_emergency_button = Button("emergency", "north", self)
        self.east_emergency_button = Button("emergency", "east", self)
        self.south_emergency_button = Button("emergency", "south", self)
        self.west_emergency_button = Button("emergency", "west", self)

        self.car_queue = []

        self.from_north_light = TrafficLight("north")
        self.from_east_light = TrafficLight("east")
        self.from_south_light = TrafficLight("south")
        self.from_west_light = TrafficLight("west")
        self.from_north_light.push_handlers(self)
        self.from_east_light.push_handlers(self)
        self.from_south_light.push_handlers(self)
        self.from_west_light.push_handlers(self)

        self.north_lane = Lane(self, 'north')
        self.south_lane = Lane(self, 'south')
        self.east_lane = Lane(self, 'east')
        self.west_lane = Lane(self, 'west')

        self.central_occupied = 0

        self.draw_road()
        self.draw_button()
        self.draw_light()
        self.running_lane = "horizontal"
        self.last_change_time = time.time()



        pyglet.clock.schedule_interval(self.schedule, 0.1)
        self.aging = False


    def draw_road(self):

        road_image_1 = image.create(200, 800, image.SolidColorImagePattern(color=(190, 190, 190, 255)))
        road_image_2 = image.create(800, 200, image.SolidColorImagePattern(color=(190, 190, 190, 255)))
        road_1 = Sprite(road_image_1, position=(400, 400))
        road_2 = Sprite(road_image_2, position=(400, 400))
        self.add(road_1)
        self.add(road_2)
        self.draw_line()

    def draw_line(self):
        line_1 = Line(start=(0, 400), end=(300, 400), color=(255, 215, 0, 255), stroke_width=5)
        self.add(line_1)
        line_2 = Line(start=(400, 800), end=(400, 500), color=(255, 215, 0, 255), stroke_width=5)
        self.add(line_2)
        line_3 = Line(start=(500, 400), end=(800, 400), color=(255, 215, 0, 255), stroke_width=5)
        self.add(line_3)
        line_4 = Line(start=(400, 300), end=(400, 0), color=(255, 215, 0, 255), stroke_width=5)
        self.add(line_4)
        self.north_stop_line = Line(start=(300, 500), end=(500, 500), color=(255, 255, 255, 255), stroke_width=5)
        self.add(self.north_stop_line)
        self.east_stop_line = Line(start=(500, 500), end=(500, 300), color=(255, 255, 255, 255), stroke_width=5)
        self.add(self.east_stop_line)
        self.south_stop_line = Line(start=(500, 300), end=(300, 300), color=(255, 255, 255, 255), stroke_width=5)
        self.add(self.south_stop_line)
        self.west_stop_line = Line(start=(300, 300), end=(300, 500), color=(255, 255, 255, 255), stroke_width=5)
        self.add(self.west_stop_line)

    def draw_button(self):

        self.add(self.north_normal_button)
        self.add(self.east_normal_button)
        self.add(self.south_normal_button)
        self.add(self.west_normal_button)
        self.add(self.north_emergency_button)
        self.add(self.east_emergency_button)
        self.add(self.south_emergency_button)
        self.add(self.west_emergency_button)


    def draw_light(self):

        self.add(self.from_north_light)
        self.add(self.from_south_light)
        self.add(self.from_east_light)
        self.add(self.from_west_light)

        self.from_west_light.switch_signal()
        self.from_east_light.switch_signal()


    def add_car(self, type, from_direction):
        car = None

        if from_direction is "north":
            car = Car(type, self.north_lane)
            self.north_lane.add_car(car)
            car.do(CustomizeMoveBy((0, -900), duration=4))

        elif from_direction is "south":
            car = Car(type, self.south_lane)
            self.south_lane.add_car(car)
            car.do(CustomizeMoveBy((0, 900), duration=4))
        elif from_direction is "east":
            car = Car(type, self.east_lane)
            self.east_lane.add_car(car)
            car.do(CustomizeMoveBy((-900, 0), duration=4))
        elif from_direction is "west":
            car = Car(type, self.west_lane)
            self.west_lane.add_car(car)

            car.do(CustomizeMoveBy((900, 0), duration=4))

        self.add(car)
        print car
        self.car_queue.append(car)


    def swtich_lights(self):
        self.last_change_time = time.time()
        self.from_north_light.switch_signal()
        self.from_west_light.switch_signal()
        self.from_east_light.switch_signal()
        self.from_south_light.switch_signal()


    def allow_vertical(self):
        self.running_lane = "vertical"
        self.last_change_time = time.time()
        self.from_north_light.set_green()
        self.from_south_light.set_green()
        self.from_east_light.set_red()
        self.from_west_light.set_red()


    def allow_horizontal(self):
        self.running_lane = "horizontal"
        self.last_change_time = time.time()
        self.from_west_light.set_green()
        self.from_east_light.set_green()
        self.from_north_light.set_red()
        self.from_south_light.set_red()

    def clear_central(self):

        self.from_west_light.set_red()
        self.from_east_light.set_red()
        self.from_north_light.set_red()
        self.from_south_light.set_red()

    def has_emergency_car(self):
        if not self.north_lane.has_emergency() and not self.south_lane.has_emergency() \
                and not self.west_lane.has_emergency() and not self.east_lane.has_emergency():
            return False
        else:
            return True

    def has_waiting_car(self):
        if self.north_lane.has_waiting_car() or self.south_lane.has_waiting_car() \
                or self.west_lane.has_waiting_car() or self.east_lane.has_waiting_car():
            return True
        else:
            return False

    def has_emergency_waiting(self):
        if not self.north_lane.has_emergency_waiting() and not self.south_lane.has_emergency_waiting() \
                and not self.west_lane.has_emergency_waiting() and not self.east_lane.has_emergency_waiting():
            return False
        else:
            return True

    def is_empty(self):
        if self.north_lane.normal_car_num + self.north_lane.emergency_car_num is 0 \
                and self.south_lane.normal_car_num + self.south_lane.emergency_car_num is 0 \
                and self.east_lane.normal_car_num + self.east_lane.emergency_car_num is 0 \
                and self.west_lane.normal_car_num + self.west_lane.emergency_car_num is 0:
            return True
        else:
            return False

    def schedule(self, dt):

        # print time.time() -self.last_change_time
        # print "aging",self.aging
        if time.time() - self.last_change_time > 4.0 and (self.aging or self.is_empty()):
            # if self.aging or self.is_empty():
                if not self.central_occupied:
                    if self.running_lane is "horizontal":
                        self.allow_vertical()
                    else:
                        self.allow_horizontal()
                else:
                    self.clear_central()
        else:
            if not self.has_waiting_car():
                self.aging = False
                if not self.has_emergency_car():
                    if self.north_lane.normal_car_num > self.west_lane.normal_car_num and self.north_lane.normal_car_num > self.east_lane.normal_car_num \
                            or self.south_lane.normal_car_num > self.west_lane.normal_car_num and self.south_lane.normal_car_num > self.east_lane.normal_car_num:
                        if not self.central_occupied:
                            if self.running_lane is "horizontal":
                                self.allow_vertical()
                                for car in self.car_queue:
                                    car.resume()
                    else:
                        if not self.central_occupied:
                            if self.running_lane is "vertical":
                                self.allow_horizontal()
                                for car in self.car_queue:
                                    car.resume()

                else:
                    if self.north_lane.emergency_car_num > self.west_lane.emergency_car_num and self.north_lane.emergency_car_num > self.east_lane.emergency_car_num \
                            or self.south_lane.emergency_car_num > self.west_lane.emergency_car_num and self.south_lane.emergency_car_num > self.east_lane.emergency_car_num:
                        if not self.central_occupied:
                            if self.running_lane is "horizontal":
                                self.allow_vertical()
                                for car in self.car_queue:
                                    car.resume()
                    else:
                        if not self.central_occupied:
                            if self.running_lane is "vertical":
                                self.allow_horizontal()
                                for car in self.car_queue:
                                    car.resume()
                        else:
                            self.clear_central()
            else:
                print "has waiting"
                self.aging = True
                if not self.has_emergency_waiting():

                    if self.north_lane.waiting_normal_car > self.west_lane.waiting_normal_car and self.north_lane.waiting_normal_car > self.east_lane.waiting_normal_car \
                            or self.south_lane.waiting_normal_car > self.west_lane.waiting_normal_car and self.south_lane.waiting_normal_car > self.east_lane.waiting_normal_car:
                        if not self.central_occupied:
                            if self.running_lane is "horizontal":
                                self.allow_vertical()
                                for car in self.car_queue:
                                    car.resume()
                    else:
                        if not self.central_occupied:
                            if self.running_lane is "vertical":
                                self.allow_horizontal()
                                for car in self.car_queue:
                                    car.resume()

                else:
                    if self.north_lane.waiting_emergency_car > self.west_lane.waiting_emergency_car and self.north_lane.waiting_emergency_car > self.east_lane.waiting_emergency_car \
                            or self.south_lane.waiting_emergency_car > self.west_lane.waiting_emergency_car and self.south_lane.waiting_emergency_car > self.east_lane.waiting_emergency_car:
                        if not self.central_occupied:
                            if self.running_lane is "horizontal":
                                self.allow_vertical()
                                for car in self.car_queue:
                                    car.resume()
                    else:
                        if not self.central_occupied:
                            if self.running_lane is "vertical":
                                self.allow_horizontal()
                                for car in self.car_queue:
                                    car.resume()
                        else:
                            self.clear_central()




