import pygame
import simple_draw as sd


class Button:
    def __init__(self, x, y, caption, event=None):
        self.x = x
        self.y = y
        self.caption = caption
        self._color1 = sd.COLOR_YELLOW
        self._color2 = sd.COLOR_DARK_YELLOW
        self._height = 10
        self._width = 30
        if event is None:
            self._event = self._even_null
        else:
            self._event = event

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
        myfont = pygame.font.SysFont('Comic Sans MS', int(self._height * 0.7))
        textsurface = myfont.render(self.caption, False, (0, 0, 0))
        sd._screen.blit(textsurface,
                        (self.x + (self._width - textsurface.get_width()) // 2,
                         sd.resolution[1] - self.y + (self._height - textsurface.get_height()) // 2 - self._height))

    def check_over(self, cursor_pos):
        return (not cursor_pos is None
                and self.x <= cursor_pos.x <= self.x + self._width
                and self.y <= cursor_pos.y <= self.y + self._height)

    def _even_null(self):
        pass


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