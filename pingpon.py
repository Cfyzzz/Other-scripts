import random

import simple_draw as sd


sd.caption = "Приведение"

class Field:

    def __init__(self, steps, distance, balls):
        self.steps = steps
        self.current_step = 0
        self.current_offset = 0
        self.old_offset = 0
        self.distance = distance
        self.size_ceil = distance - 4
        self.y = 0
        self.balls = balls

    def draw(self, offset, color):
        dist = self.distance * 2
        steps_x = (sd.resolution[0] + self.distance * 8) // dist
        steps_y = (sd.resolution[1] + self.distance * 8) // dist

        for x in range(steps_x):
            for y in range(steps_y):
                left_bottom = sd.get_point(x=x * dist - offset - self.distance * 2,
                                           y=y * dist + self.y - self.distance * 2)
                right_top = sd.get_point(x=left_bottom.x + self.size_ceil,
                                         y=left_bottom.y + self.size_ceil)

                center = sd.get_point(x=left_bottom.x + self.size_ceil // 2,
                                      y=left_bottom.y + self.size_ceil // 2)

                _color = color
                for ball in self.balls:
                    dist_for_ball = ((center.x - ball.x) ** 2 + (center.y - ball.y) ** 2) ** 0.5
                    if dist_for_ball <= ball.radius and color != sd.background_color:
                        _color = sd.COLOR_WHITE
                        break

                sd.rectangle(left_bottom=left_bottom, right_top=right_top, color=_color)

    def redraw(self):
        self.y = 0
        self.draw(offset=self.old_offset, color=sd.background_color)
        self.draw(offset=self.distance + self.old_offset, color=sd.background_color)
        self.y = self.distance
        self.draw(offset=self.distance - self.old_offset, color=sd.background_color)
        self.y = self.distance + self.old_offset
        self.draw(offset=0, color=sd.background_color)

        self.y = 0
        self.draw(offset=self.current_offset, color=sd.COLOR_ORANGE)
        self.draw(offset=self.distance + self.current_offset, color=sd.COLOR_GREEN)
        self.y = self.distance
        self.draw(offset=self.distance - self.current_offset, color=sd.COLOR_ORANGE)
        self.y = self.distance + self.current_offset
        self.draw(offset=0, color=sd.COLOR_GREEN)

        self.old_offset = self.current_offset

    def move(self):
        self.current_step += 1 if self.current_step < self.steps * 2 else -self.current_step + 1
        self.current_offset = self.distance * self.current_step // self.steps


class Ball:
    def __init__(self, radius):
        self.radius = radius
        self.x = radius * 3
        self.y = radius


ball = Ball(radius=50)
ball2 = Ball(radius=30)
ball3 = Ball(radius=20)
balls = [ball, ball2, ball3]
field = Field(steps=10, distance=20, balls=balls)
ball.y = 100
dx = 20
dy = 10
old_x = ball.x
old_y = ball.y
old_x2 = ball2.x
old_y2 = ball2.y
old_x3 = ball3.x
old_y3 = ball3.y
sd._init()
# sd.sleep(5)
while True:
    sd.start_drawing()
    field.move()
    field.redraw()

    old_x = ball.x
    old_y = ball.y

    new_x = ball.x + dx
    new_y = ball.y + dy
    if new_x > sd.resolution[0] - ball.radius:
        dx = -random.randint(a=20, b=50)
        new_x = sd.resolution[0] - ball.radius
    elif new_x < ball.radius:
        dx = random.randint(a=20, b=50)
        new_x = ball.radius

    if new_y > sd.resolution[1] - ball.radius:
        dy = -random.randint(a=10, b=40)
        new_y = sd.resolution[1] - ball.radius
    elif new_y < ball.radius:
        dy = random.randint(a=10, b=40)
        new_y = ball.radius

    ball.x = new_x
    ball.y = new_y

    ball2.x = old_x
    ball2.y = old_y

    ball3.x = old_x2
    ball3.y = old_y2

    old_x2 = ball2.x
    old_y2 = ball2.y
    old_x3 = ball3.x
    old_y3 = ball3.y



    sd.finish_drawing()
    sd.sleep(0.02)
    if sd.user_want_exit():
        break
