from cocos.actions import MoveBy

__author__ = 'danielqiu'


class CustomizeMoveBy(MoveBy):
    is_paused = False

    def update(self, t, **kwargs):

        self.target.position = self.start_position + self.delta * t
        car = self.target
        if car.from_direction is "north":
            if car.position[1] < 800:
                car.set_has_started()

        elif car.from_direction is "south":
            if car.position[1] > 0:
                car.set_has_started()

        elif car.from_direction is "west":
            if car.position[0] > 0:
                car.set_has_started()
        elif car.from_direction is "east":
            if car.position[0] < 800:
                car.set_has_started()
                # self.control_interval(car,t)




                # def control_interval(self,car,t):
                #
                #     if car.from_direction is "north":
                #         pass
                #         # if car.previous_car and car.position[1] > 350:
                #         #     if abs(car.previous_car.position[1] - car.position[1]) < 70:
                #         #         self.is_paused = True
                #         #     else:
                #         #         self.is_paused = False
                #
                #
                #
                #     if car.from_direction is "south":
                #         # if car.previous_car and car.position[1] < 350:
                #         #     if abs(car.previous_car.position[1] - car.position[1]) < 70:
                #         #         self.is_paused = True
                #         #     else:
                #         #         self.is_paused = False
                #
                #
                #
                #
                #
                #     if car.from_direction is "east":
                #         # if car.previous_car and car.position[0] > 350:
                #         #     if abs(car.previous_car.position[0] - car.position[0]) < 70:
                #         #         self.is_paused = True
                #         #     else:
                #         #         self.is_paused = False
                #
                #         # if 530<car.position[0]<540 and car.lane.map.from_east_light.is_red():
                #         #     self.is_paused = True
                #         # elif 530<car.position[0]<540 and car.lane.map.from_east_light.is_green():
                #         #     self.is_paused = False
                #
                #         # if car.position[0] < 350:
                #         #     car.in_map = False
                #         #     if not car.removed:
                #         #         car.lane.remove_car()
                #         #         print "remove"
                #         #         car.removed = True
                #         #         if car.following:
                #         #             car.following.previous_car = None
                #
                #     if car.from_direction is "west":
                #         if car.previous_car and car.position[0] < 350:
                #             if abs(car.previous_car.position[0] - car.position[0]) < 70:
                #                 self.is_paused = True
                #             else:
                #                 self.is_paused = False
                #
                #         # if 260<car.position[0]<270 and car.lane.map.from_west_light.is_red():
                #         #     self.is_paused = True
                #         # elif 260<car.position[0]<270 and car.lane.map.from_west_light.is_green():
                #         #     self.is_paused = False
                #
                #         if car.position[0] > 350:
                #             car.in_map = False
                #             if not car.removed:
                #                 car.lane.remove_car()
                #                 print "remove"
                #                 car.removed = True
                #                 if car.following:
                #                     car.following.previous_car = None
                #
                #
                #     if self.is_paused is False:
                #         self.target.position = self.start_position + self.delta * t