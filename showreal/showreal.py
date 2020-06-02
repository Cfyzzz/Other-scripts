import simple_draw as sd

from simple_user_interface import UserInterface
from data_showreal import segments
import Draw3D
from copy import copy

EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2
LEFT_CLICK = 3

mode = EMPTY_MODE

sd.caption = "Эффекты"
sd.resolution = (800, 600)


class Figure:
    def __init__(self):
        self.points = []
        self.radius = 4
        self.figure_resolution = 10
        self.origin = sd.get_point(0, 0)

    def append(self, point: sd.Point):
        self.points.append(point)

    def draw(self):
        if not self.points:
            return

        start_point = sd.get_point(self.points[0][0], self.points[0][1])
        start_point.x += self.origin.x
        start_point.y += self.origin.y
        self.draw_point(start_point)
        for point in self.points[1:]:
            _point = sd.get_point(point[0], point[1])
            _point.x += self.origin.x
            _point.y += self.origin.y
            self.draw_point(_point)
            sd.line(start_point=start_point, end_point=_point)
            start_point = _point

    def draw_point(self, point):
        sd.circle(center_position=point, radius=self.radius, width=0)

    def prepare_points(self):
        for point in self.points:
            if len(point) < 3:
                point.append(0)

    def scale(self, vec):
        mat_scale = Draw3D.scale(vec)
        self.apply_matrix(mat_scale)

    def apply_matrix(self, matrix):
        for idx, vertex in enumerate(self.points):
            self.points[idx] = Draw3D.vec_mul_matrix(vertex, matrix)


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def strat_showreal():
    word = "skillbox"
    dist = 10
    start_spell = sd.get_point(100, 300)
    scale_val = 0.3
    for idx, ch in enumerate(word):
        figure = Figure()
        figure.radius = 0
        figure.points = copy(segments[ch]['data'])
        figure.prepare_points()

        figure.scale([scale_val, scale_val, 1])

        figure.origin = start_spell
        figure.draw()
        start_spell.x += segments[ch]['width'] * scale_val + dist


if __name__ == "__main__":
    sd._init()
    sd.background_color = sd.COLOR_BLACK
    clear_screen()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "run", event=strat_showreal).set_size(60, 30)
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
