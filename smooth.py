import simple_draw as sd
from splines import main_spline


EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2

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

    def set_size(self, height, width):
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
        # TODO - Вывести caption по середине кнопки и с нужной высотой шрифта

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

    def show(self, cursor_pos):
        for button in self.buttons:
            is_over = button.check_over(cursor_pos)
            button.draw(is_over)
            if is_over:
                button._event()


class Figure:
    def __init__(self):
        self.points = []
        self.radius = 4

    def append(self, point: sd.Point):
        self.points.append(point)
        # print(*([p.x, p.y] for p in self.points))

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


def test_main_spline(points):
    def wrap():
        main_spline(points)
        print("click!")
    return wrap


if __name__ == "__main__":
    sd._init()
    figure = Figure()
    user_interface = UserInterface()
    user_interface.add_button(10, 10, "+", event=test_main_spline(figure.points)).set_size(30, 60)
    user_interface.add_button(80, 10, "-").set_size(30, 60)
    while True:
        mouse_pos, mouse_buttons = sd.get_mouse_state()
        point = mouse_pos
        cursor_pos = None

        if mouse_buttons[2] == 1 and mode == EMPTY_MODE:
            figure.append(point)
            print(len(figure.points))
            mode = START_MODE

        elif mouse_buttons[2] == 0 and mode == START_MODE:
            mode = EMPTY_MODE

        elif mouse_buttons[0] == 1 and mode == EMPTY_MODE:
            cursor_pos = mouse_pos
            # mode = START_MODE

        # elif mouse_buttons[0] == 0 and mode == START_MODE:
        #     mode = EMPTY_MODE

        # elif mouse_buttons[2] == 1 and mode == EMPTY_MODE:
        #     print("2")
        #     mode = GET_POS_MOD
        #
        # elif mouse_buttons[2] == 1 and mode == GET_POS_MOD:
        #     print("3")
        #
        # elif mouse_buttons[2] == 0 and mode == GET_POS_MOD:
        #     print("4")
        #     mode = EMPTY_MODE

        sd.start_drawing()
        clear_screen()
        figure.draw()
        user_interface.show(cursor_pos)
        sd.finish_drawing()
        if sd.user_want_exit():
            break
