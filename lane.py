__author__ = 'danielqiu'

from Queue import *


class Lane:
    def __init__(self, m, from_direction):
        self.car_queue = []
        self.map = m
        self.from_direction = from_direction
        self.normal_car_num = 0
        self.emergency_car_num = 0
        self.waiting_normal_car = 0
        self.waiting_emergency_car = 0

    def add_car(self, car):
        if self.car_queue:
            car.previous_car = self.car_queue[len(self.car_queue) - 1]
            self.car_queue[len(self.car_queue) - 1].following = car
        if car.type is "normal":
            self.normal_car_num += 1
        elif car.type is "emergency":
            self.emergency_car_num += 1
        self.car_queue.append(car)

    def remove_car(self):
        c = self.car_queue[-1]
        if c.type is "normal":
            self.normal_car_num -= 1
        elif c.type is "emergency":
            self.emergency_car_num -= 1

    def get_from(self):
        return self.from_direction

    def has_emergency(self):
        if self.emergency_car_num is 0:
            return False
        else:
            return True

    def has_normal_waiting(self):
        if self.waiting_normal_car is 0:
            return False
        else:
            return True

    def has_emergency_waiting(self):
        if self.waiting_emergency_car is 0:
            return False
        else:
            return True

    def has_waiting_car(self):
        if self.has_normal_waiting() or self.has_emergency_waiting():
            print self.waiting_normal_car+self.waiting_emergency_car
            return True
        else:
            return False

    def get_waiting_normal_car_num(self):
        return self.waiting_normal_car