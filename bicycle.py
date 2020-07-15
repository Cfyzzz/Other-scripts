import math

import simple_draw as sd
from simple_user_interface import UserInterface

LENGTH_HEAD_TUBE = 150
LENGTH_TOP_TUBE = 100
LENGTH_HUB_TO_SADDLE = 200
LENGTH_ARC_SEGMENT = 10

COLOR_GREY = (150, 150, 150)
PI = 3.14159

EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2
LEFT_CLICK = 3

mode = EMPTY_MODE

sd.caption = "Bicycle"


class Bicycle:

    def __init__(self, radius_front_wheel, radius_back_wheel, pos_wheel_front, pos_wheel_back):
        self.radius_front_wheel = radius_front_wheel
        self.radius_back_wheel = radius_back_wheel
        self.pos_wheel_front = pos_wheel_front
        self.pos_wheel_back = pos_wheel_back
        self.pos_wheel_back.y = pos_wheel_front.y + self.radius_back_wheel - self.radius_front_wheel
        self.pos_saddle = sd.get_point(0, 0)

    def draw(self):
        self.draw_wheel_front()
        self.draw_wheel_back()
        self.draw_frame()
        self.draw_saddle()
        self.draw_handlebar()

    def draw_wheel_front(self):
        self.draw_wheel(center=self.pos_wheel_front, radius=self.radius_front_wheel)

    def draw_wheel_back(self):
        self.draw_wheel(center=self.pos_wheel_back, radius=self.radius_back_wheel)

    def draw_wheel(self, center, radius):
        self._draw_spokes(center, radius, 10)
        sd.circle(center_position=center, radius=radius, color=COLOR_GREY, width=7)
        sd.circle(center_position=center, radius=radius + 7, color=sd.COLOR_BLACK, width=7)
        self._draw_protec(center, radius + 6)

    def _draw_protec(self, center, radius, angle=0):
        step_angle = int(LENGTH_ARC_SEGMENT * 180 / PI / radius)
        for ang in range(0, 360, step_angle):
            point1 = self.get_point_from_angle(center=center, angle=angle + ang, radius=radius)
            point2 = self.get_point_from_angle(center=center, angle=angle + ang + 1, radius=radius + 2)
            point3 = self.get_point_from_angle(center=center, angle=angle + ang + 2, radius=radius + 2)
            point4 = self.get_point_from_angle(center=center, angle=angle + ang + 3, radius=radius)
            poly_line = [point1, point2, point3, point4]
            sd.polygon(point_list=poly_line, color=sd.COLOR_BLACK, width=3)

    def _draw_spokes(self, center, radius_out, radius_in):
        self._build_side_spokes(center=center, radius_out=radius_out, radius_in=radius_in, offset_out=85)
        self._build_side_spokes(center=center, radius_out=radius_out, radius_in=radius_in, offset_out=-85)

    @staticmethod
    def _build_side_spokes(center, radius_out, radius_in, offset_out):
        step_angle = 360 // 9
        offset_in = step_angle // 2
        for angle in range(0, 360, step_angle):
            point1_in = sd.get_point(x=sd.cos(angle) * radius_in + center.x,
                                     y=sd.sin(angle) * radius_in + center.y)
            point1_out = sd.get_point(x=sd.cos(angle + offset_out) * radius_out + center.x,
                                      y=sd.sin(angle + offset_out) * radius_out + center.y)
            point2_in = sd.get_point(x=sd.cos(angle + offset_in) * radius_in + center.x,
                                     y=sd.sin(angle + offset_in) * radius_in + center.y)
            point2_out = sd.get_point(x=sd.cos(angle - offset_out + offset_in) * radius_out + center.x,
                                      y=sd.sin(angle - offset_out + offset_in) * radius_out + center.y)
            sd.line(point1_in, point1_out, color=COLOR_GREY, width=2)
            sd.line(point2_in, point2_out, color=COLOR_GREY, width=2)

    @staticmethod
    def get_point_from_angle(center, angle, radius):
        x = sd.cos(angle) * radius + center.x
        y = sd.sin(angle) * radius + center.y + 1
        return sd.get_point(x, y)

    def draw_frame(self):
        pos_pedal = sd.get_point(x=self.pos_wheel_back.x + self.radius_back_wheel + 30, y=self.pos_wheel_back.y)
        _pos_saddle = sd.get_point(x=pos_pedal.x, y=pos_pedal.y + self.radius_back_wheel + 20)
        pos_handlebar = sd.get_point(x=self.pos_wheel_front.x, y=self.pos_wheel_front.y + self.radius_front_wheel + 50)

        critical_point = sd.get_point(x=(pos_pedal.x + pos_handlebar.x) / 2,
                                      y=(pos_pedal.y + pos_handlebar.y) / 2)
        critical_dist = self._get_dist(critical_point, self.pos_wheel_front) - 20
        if critical_dist < self.radius_front_wheel:
            frame_points = [pos_pedal, self.pos_wheel_back, _pos_saddle, pos_handlebar, _pos_saddle, pos_pedal]

            critical_point = sd.get_point(x=(_pos_saddle.x + pos_handlebar.x) / 2,
                                          y=(_pos_saddle.y + pos_handlebar.y) / 2)
            critical_dist = self._get_dist(critical_point, self.pos_wheel_front) - 20
            if critical_dist < self.radius_front_wheel:
                length_to_saddle = min(LENGTH_HUB_TO_SADDLE, self.radius_front_wheel + 10)

                ang_rad = math.acos((LENGTH_HEAD_TUBE ** 2 + length_to_saddle ** 2 - LENGTH_TOP_TUBE ** 2) / (
                            2 * LENGTH_HEAD_TUBE * length_to_saddle))
                _pos_saddle = sd.get_point(x=math.cos(ang_rad + PI / 2) * LENGTH_HUB_TO_SADDLE + self.pos_wheel_front.x,
                                           y=math.sin(ang_rad + PI / 2) * LENGTH_HUB_TO_SADDLE + self.pos_wheel_front.y)
                frame_points = [self.pos_wheel_back, _pos_saddle, pos_handlebar, _pos_saddle]
                pos_pedal = self.pos_wheel_front
        else:
            frame_points = [pos_pedal, self.pos_wheel_back, _pos_saddle, pos_handlebar]

        sd.polygon(point_list=frame_points, width=10, color=sd.COLOR_BLUE)
        sd.line(self.pos_wheel_front, pos_handlebar, width=10, color=sd.COLOR_BLUE)
        sd.circle(center_position=pos_pedal, radius=20, width=15, color=COLOR_GREY)

        self.pos_saddle.x = _pos_saddle.x
        self.pos_saddle.y = _pos_saddle.y

    @staticmethod
    def _get_dist(a, b):
        """Длина линии между двумя точками"""
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    def draw_saddle(self):
        points_saddle = [
            sd.get_point(self.pos_saddle.x, self.pos_saddle.y + 20),
            sd.get_point(self.pos_saddle.x - 15, self.pos_saddle.y + 35),
            sd.get_point(self.pos_saddle.x + 50, self.pos_saddle.y + 35)
        ]
        sd.line(self.pos_saddle, points_saddle[0], color=sd.COLOR_BLUE, width=10)
        sd.polygon(point_list=points_saddle, color=sd.COLOR_BLACK, width=15)

    def draw_handlebar(self):
        pos_handlebar = sd.get_point(x=self.pos_wheel_front.x, y=self.pos_wheel_front.y + self.radius_front_wheel + 50)
        points_handlebar = [
            sd.get_point(pos_handlebar.x + 20, pos_handlebar.y + 20),
            sd.get_point(pos_handlebar.x - 60, pos_handlebar.y + 20)
        ]

        sd.line(pos_handlebar, sd.get_point(pos_handlebar.x, pos_handlebar.y + 20), color=sd.COLOR_BLUE, width=10)
        sd.polygon(point_list=points_handlebar, color=sd.COLOR_BLACK, width=15)


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def show_bicycle():
    rad_back = 70

    for rad_front in range(70, 120):
        sd.start_drawing()
        clear_screen()
        rad_back -= 0.4
        bicycle = Bicycle(radius_front_wheel=rad_front,
                          radius_back_wheel=rad_back,
                          pos_wheel_front=sd.get_point(450, 300),
                          pos_wheel_back=sd.get_point(200, 300))
        bicycle.draw()
        sd.finish_drawing()

        sd.sleep(0.1)
        sd.finish_drawing()
        if sd.user_want_exit():
            break


if __name__ == "__main__":
    sd._init()
    sd.background_color = sd.COLOR_WHITE
    clear_screen()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "fig1", event=show_bicycle).set_size(60, 30)
    while True:
        mouse_pos, mouse_buttons = sd.get_mouse_state()
        point = mouse_pos
        on_click = False

        if mouse_buttons[2] == 1 and mode == EMPTY_MODE:
            mode = START_MODE

        elif mouse_buttons[2] == 0 and mode == START_MODE:
            mode = EMPTY_MODE

        elif mouse_buttons[0] == 1 and mode == EMPTY_MODE:
            mode = LEFT_CLICK

        elif mouse_buttons[0] == 0 and mode == LEFT_CLICK:
            on_click = True
            mode = EMPTY_MODE

        sd.start_drawing()
        user_interface.show(cursor_pos=mouse_pos, is_click=on_click)
        sd.finish_drawing()
        if sd.user_want_exit():
            break
