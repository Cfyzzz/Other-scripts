import simple_draw as sd
import pygame
from splines import loopResolve

EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2
LEFT_CLICK = 3

mode = EMPTY_MODE

sd.caption = "Интерполяция"


class Button:
    def __init__(self, x, y, caption, event=None):
        self.x = x
        self.y = y
        self.caption = caption
        self._event = event
        self._color1 = sd.COLOR_YELLOW
        self._color2 = sd.COLOR_DARK_YELLOW
        self._height = 10
        self._width = 30

    def set_size(self, width, height):
        self._height = height
        self._width = width
        return self

    def set_color_passive(self, color):
        self._color1 = color
        return self

    def set_color_active(self, color):
        self._color2 = color
        return self

    def draw(self, is_passive=True):
        color1 = self._color1 if is_passive else self._color2
        color2 = self._color2 if is_passive else self._color1

        sd.rectangle(left_bottom=sd.get_point(self.x, self.y),
                     right_top=sd.get_point(self.x + self._width, self.y + self._height),
                     color=color1,
                     width=0)
        sd.rectangle(left_bottom=sd.get_point(self.x, self.y),
                     right_top=sd.get_point(self.x + self._width, self.y + self._height),
                     color=color2,
                     width=2)
        self._draw_text_on_button()

    def _draw_text_on_button(self):
        # pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', int(self._height * 0.8))
        textsurface = myfont.render(self.caption, False, (0, 0, 0))
        sd._screen.blit(textsurface,
                        (self.x + (self._width - textsurface.get_width()) // 2,
                         sd.resolution[1] - self.y + (self._height - textsurface.get_height()) // 2 - self._height))

    def check_over(self, cursor_pos):
        return (not cursor_pos is None
                and self.x <= cursor_pos.x <= self.x + self._width
                and self.y <= cursor_pos.y <= self.y + self._height)


class UserInterface:

    def __init__(self):
        self.buttons = []

    def add_button(self, x, y, caption, event=None):
        new_button = Button(x=x, y=y, caption=caption, event=event)
        self.buttons.append(new_button)
        return new_button

    def show(self, cursor_pos, is_click=False):
        for button in self.buttons:
            is_over = button.check_over(cursor_pos)
            button.draw(is_over)
            if is_over and is_click:
                button._event()


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


def test_main_spline(figure):
    def wrap_test_main_spline():
        loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)
    return wrap_test_main_spline


def clear(figure):
    def wrap_clear():
        figure.points = []
    return wrap_clear


def resolution_minus(figure):
    def wrap_resolution_minus():
        figure.figure_resolution += 10
        loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)
    return wrap_resolution_minus


def resolution_plus(figure):
    def wrap_resolution_plus():
        figure.figure_resolution -= 10
        figure.figure_resolution = max(10, figure.figure_resolution)
        loopResolve(verts=figure.points, step=0, dist=figure.figure_resolution)
    return wrap_resolution_plus


def flip_radius(figure):
    def wrap_flip_radius():
        if figure.radius == 0:
            figure.radius = 4
        else:
            figure.radius = 0
    return wrap_flip_radius


if __name__ == "__main__":
    sd._init()
    figure = Figure()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "run", event=test_main_spline(figure)).set_size(60, 30)
    user_interface.add_button(80, 10, "clear", event=clear(figure)).set_size(80, 30)
    user_interface.add_button(180, 10, "+", event=resolution_plus(figure)).set_size(30, 30)
    user_interface.add_button(220, 10, "-", event=resolution_minus(figure)).set_size(30, 30)
    user_interface.add_button(270, 10, "point", event=flip_radius(figure)).set_size(60, 30)
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
