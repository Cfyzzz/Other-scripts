# -*- coding: utf-8 -*-

import simple_draw as sd

CATCH_MODE = 1
EMPTY_MODE = 0

sd.caption = "Super star"
sd.background_color = (10, 10, 10)


class Segment:

    def __init__(self, point1: sd.Point, point2: sd.Point):
        self.point1 = point1
        self.point2 = point2

    @property
    def length(self):
        dx = self.point1.x - self.point2.x
        dy = self.point1.y - self.point2.y
        return (dx ** 2 + dy ** 2) ** 0.5

    def get_part_segment(self, percent):
        dx = (self.point1.x - self.point2.x) * percent
        dy = (self.point1.y - self.point2.y) * percent
        point_base = sd.get_point(x=self.point2.x, y=self.point2.y)
        point_to = sd.get_point(x=self.point2.x + dx, y=self.point2.y + dy)
        return Segment(point1=point_to, point2=point_base)


class Star:

    def __init__(self, point_base, branches, segments, length, color):
        self.point_base = point_base
        self.branches = branches
        self.segments = segments
        self.length = length
        self.color = color

    def draw(self, fake_base=None, rotate_angle=0):
        if fake_base is None:
            fake_base = self.point_base

        dangle = 360 // self.branches
        for angle in range(dangle, 361, dangle):
            angle1 = angle - dangle + rotate_angle
            angle2 = angle + rotate_angle
            vector_branch1 = sd.Vector(start_point=self.point_base, direction=angle1, length=self.length)
            vector_branch2 = sd.Vector(start_point=self.point_base, direction=angle2, length=self.length)
            segment2 = Segment(fake_base, vector_branch2.end_point)
            segment1 = Segment(vector_branch1.end_point, fake_base)
            for offset in range(self.segments):
                koeff = offset / self.segments
                koeff_color = (offset / self.segments) ** 0.5
                sub_segment1 = segment1.get_part_segment(koeff)
                sub_segment2 = segment2.get_part_segment(koeff)
                color_mod = (self.color[0] * koeff_color * 0.7,
                             255 - self.color[1] * koeff_color * 0.9,
                             self.color[2] * koeff_color * 1
                             )
                sd.line(start_point=sub_segment1.point1, end_point=sub_segment2.point1, color=color_mod, width=2)


star = Star(point_base=sd.get_point(x=300, y=300), length=300, color=sd.COLOR_WHITE,
            branches=8, segments=20)

mode = EMPTY_MODE
base_center = sd.get_point(x=300, y=300)
center = base_center
angle = 0
sd._init()
while True:
    angle += 0.1

    mouse_pos, mouse_buttons = sd.get_mouse_state()
    point = mouse_pos

    if mouse_buttons[0] == 1 and mode == EMPTY_MODE:
        mode = CATCH_MODE

    if mouse_buttons[0] == 1:
        center = point

    if mouse_buttons[0] == 0 and mode == CATCH_MODE:
        center = base_center
        mode = EMPTY_MODE

    sd.start_drawing()
    sd.rectangle(left_bottom=sd.get_point(x=0, y=0), right_top=sd.get_point(x=sd.resolution[0], y=sd.resolution[1]),
                 color=sd.background_color)
    star.draw(fake_base=center, rotate_angle=angle)
    sd.finish_drawing()

    sd.finish_drawing()
    if sd.user_want_exit():
        break
