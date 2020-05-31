import simple_draw as sd

from simple_user_interface import UserInterface
from splines import loopResolve

EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2
LEFT_CLICK = 3

mode = EMPTY_MODE

sd.caption = "Интерполяция"


class Figure:
    def __init__(self):
        self.points = []
        self.radius = 4
        self.figure_resolution = 10

    def append(self, point: sd.Point):
        self.points.append(point)

    def draw(self):
        if not self.points:
            return

        self.draw_point(self.points[0])
        start_point = self.points[0]
        for point in self.points[1:]:
            self.draw_point(point)
            sd.line(start_point=start_point, end_point=point)
            start_point = point

    def draw_point(self, point: sd.Point):
        sd.circle(center_position=point, radius=self.radius, width=0)


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def set_event(func):
    def wrapper(figure):
        def surrogate():
            func(figure)
        return surrogate
    return wrapper


@set_event
def test_main_spline(figure):
    loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)


@set_event
def clear(figure):
    figure.points = []


@set_event
def resolution_minus(figure):
    figure.figure_resolution += 10
    loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)


@set_event
def resolution_plus(figure):
    figure.figure_resolution -= 10
    figure.figure_resolution = max(10, figure.figure_resolution)
    loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)


@set_event
def flip_radius(figure):
    if figure.radius == 0:
        figure.radius = 4
    else:
        figure.radius = 0


@set_event
def print_figure(figure):
    result = []
    for point in figure.points:
        result.append([point.x, point.y])
    print(result)


if __name__ == "__main__":
    sd._init()
    figure = Figure()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "run", event=test_main_spline(figure)).set_size(60, 30)
    user_interface.add_button(80, 10, "clear", event=clear(figure)).set_size(80, 30)
    user_interface.add_button(180, 10, "+", event=resolution_plus(figure)).set_size(30, 30)
    user_interface.add_button(220, 10, "-", event=resolution_minus(figure)).set_size(30, 30)
    user_interface.add_button(270, 10, "point", event=flip_radius(figure)).set_size(60, 30)
    user_interface.add_button(340, 10, "print", event=print_figure(figure)).set_size(60, 30)
    while True:
        mouse_pos, mouse_buttons = sd.get_mouse_state()
        point = mouse_pos
        on_click = False

        if mouse_buttons[2] == 1 and mode == EMPTY_MODE:
            figure.append(point)
            mode = START_MODE

        elif mouse_buttons[2] == 0 and mode == START_MODE:
            mode = EMPTY_MODE

        elif mouse_buttons[0] == 1 and mode == EMPTY_MODE:
            mode = LEFT_CLICK

        elif mouse_buttons[0] == 0 and mode == LEFT_CLICK:
            on_click = True
            mode = EMPTY_MODE

        sd.start_drawing()
        clear_screen()
        figure.draw()
        user_interface.show(cursor_pos=mouse_pos, is_click=on_click)
        sd.finish_drawing()
        if sd.user_want_exit():
            break
