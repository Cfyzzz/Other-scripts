import simple_draw as sd

from simple_user_interface import UserInterface


EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2
LEFT_CLICK = 3

mode = EMPTY_MODE

sd.caption = "Эффекты"


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def strat_showreal():
    pass


if __name__ == "__main__":
    sd._init()
    sd.background_color = sd.COLOR_BLACK
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
        clear_screen()
        user_interface.show(cursor_pos=mouse_pos, is_click=on_click)
        sd.finish_drawing()
        if sd.user_want_exit():
            break
