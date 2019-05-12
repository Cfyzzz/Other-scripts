import simple_draw as sd

# Author: Nedovizin Alexander

sd.background_color = sd.COLOR_BLACK
sd.resolution = (700, 300)
sd.caption = "Russia"


def draw_flag(point, correct_color, angle=90):
    abs_color = abs(correct_color ** 2) * 0.3 + 0.6
    color_red = (int(255 * abs_color), 0, 0)
    color_blue = (0, 0, int(255 * abs_color))
    color_white = (int(255 * abs_color), int(255 * abs_color), int(255 * abs_color))

    red_line = sd.get_vector(start_point=point, angle=angle, length=50)
    red_line.draw(color=color_red, width=5)
    end_point = red_line.end_point
    blue_line = sd.get_vector(start_point=end_point, angle=angle, length=50)
    blue_line.draw(color=color_blue, width=5)
    end_point = blue_line.end_point
    white_line = sd.get_vector(start_point=end_point, angle=angle, length=50)
    white_line.draw(color=color_white, width=5)


for move_wave in range(0, 600, 1):
    sd.start_drawing()
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution),
                 color=sd.background_color, width=0)

    point = sd.get_point(x=200, y=-30)
    stick = sd.get_vector(start_point=point, angle=90 - sd.sin(move_wave * 10) * 30, length=150)
    point_end_stick = stick.end_point

    angle_flag = 90 - sd.sin(move_wave * 10) * 30
    for x in range(10, 300, 1):
        angle = -move_wave * 20 + x
        point = sd.get_point(x=point_end_stick.x + x, y=point_end_stick.y + sd.sin(angle) * 40 * x / 300)
        draw_flag(point=point, correct_color=sd.cos(angle * 0.5 - 60), angle=angle_flag)

    stick.draw(color=sd.COLOR_DARK_YELLOW, width=15)
    sd.vector(start=point_end_stick, angle=angle_flag, length=160, width=15, color=sd.COLOR_DARK_YELLOW)

    sd.finish_drawing()
    if sd.user_want_exit():
        break
    sd.sleep(0.1)
sd.pause()
