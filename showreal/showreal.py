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
            sd.line(start_point=start_point, end_point=_point, width=4)
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


class Snake:
    def __init__(self, figure: Figure):
        self.lengths = []
        self._points = []
        self.vertices = [[0, 0] for _ in range(len(figure.points))]
        self.start_point = [0, 0]
        self.width_line = 4
        self.radius_point = 0
        self.color = sd.COLOR_YELLOW
        first_point = figure.points[0]
        for point in figure.points[1:]:
            self.lengths.append(self._get_dist(first_point, point))
            first_point = point

        for point in figure.points:
            _point = [point[0] + figure.origin.x,
                      point[1] + figure.origin.y]
            self._points.append(_point)

    def set_start_position(self, point):
        self.start_point = point
        self._calculate_vertices()

    def _calculate_vertices(self):
        first_vert = self.start_point
        self.vertices[0] = first_vert
        for idx, vert in enumerate(self.vertices[1:], 1):
            length = self.lengths[idx - 1]
            target_point = self._points[idx]
            vec = self._get_vector_for_move(first_vert, target_point, length)
            vert[0] = first_vert[0] + vec[0]
            vert[1] = first_vert[1] + vec[1]
            first_vert = vert

    def _get_vector_for_move(self, first_vert, target_point, length):
        koeff_normalize = length / self._get_dist(target_point, first_vert)
        vec = [(target_point[0] - first_vert[0]) * koeff_normalize,
               (target_point[1] - first_vert[1]) * koeff_normalize]

        return vec

    def go_forward(self, dist):
        target_point = self._points[0]
        vec = self._get_vector_for_move(self.start_point, target_point, dist)
        self.start_point[0] += vec[0]
        self.start_point[1] += vec[1]
        self._calculate_vertices()

    def draw(self):
        if not self.vertices:
            return

        start_point = sd.get_point(x=self.start_point[0], y=self.start_point[1])
        self.draw_point(start_point)
        for vert in self.vertices[1:]:
            _point = sd.get_point(x=vert[0], y=vert[1])
            self.draw_point(_point)
            sd.line(start_point=start_point, end_point=_point, width=4, color=self.color)
            start_point = _point

    def draw_point(self, point):
        sd.circle(center_position=point, radius=self.radius_point, width=0)

    @staticmethod
    def _get_dist(a, b):
        """Длина линии между двумя точками"""
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def show_figure1():
    word = "skillbox"
    dist = 15
    for i in range(50):
        start_spell = sd.get_point(100, 250)
        sd.start_drawing()
        clear_screen()
        for idx, ch in enumerate(word):
            scale_val = abs(sd.sin(idx * 20 + i * 10)) * 0.2 + 0.2
            figure = Figure()
            figure.radius = 0
            figure.points = copy(segments[ch]['data'])
            figure.prepare_points()

            figure.scale([scale_val, scale_val, 1])

            figure.origin = start_spell
            figure.draw()
            start_spell.x += segments[ch]['width'] * scale_val + dist

        sd.sleep(0.1)
        sd.finish_drawing()
        if sd.user_want_exit():
            break


def show_figure2():
    word = "skillbox"
    dist = 15

    start_spell = sd.get_point(100, 250)
    sd.start_drawing()
    clear_screen()
    snakes = []
    angle = 360 / len(word)
    for idx, ch in enumerate(word):
        scale_val = 0.3
        figure = Figure()
        figure.radius = 0
        figure.points = copy(segments[ch]['data'])
        figure.prepare_points()

        figure.scale([scale_val, scale_val, 1])

        figure.origin = start_spell
        # figure.draw()
        start_spell = sd.get_point(x=start_spell.x + segments[ch]['width'] * scale_val + dist,
                                   y=start_spell.y)

        snake = Snake(figure)
        snake.color = sd.random_color()

        center = sd.get_point(400, 300)
        radius = 1000
        x = sd.sin(angle * idx) * radius + center.x
        y = sd.cos(angle * idx) * radius + center.y
        snake.set_start_position([x, y])
        snakes.append(snake)

    sd.sleep(0.1)
    sd.finish_drawing()

    dist = 15
    for step in range(210):
        dist -= step / 500
        sd.start_drawing()
        clear_screen()
        for snake in snakes:
            snake.go_forward(dist)
            snake.draw()

        sd.sleep(0.1)
        sd.finish_drawing()
        if sd.user_want_exit():
            break


def strat_showreal():
    show_figure2()


if __name__ == "__main__":
    sd._init()
    sd.background_color = (50, 50, 50)
    clear_screen()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "fig1", event=show_figure1).set_size(60, 30)
    user_interface.add_button(80, 10, "fig2", event=show_figure2).set_size(60, 30)
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
