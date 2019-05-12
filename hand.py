import copy
import math

import simple_draw as sd


def length_line(a, b):
    """Длина линии между двумя точками"""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def get_length_vector(vec):
    return length_line(a=sd.get_point(x=0, y=0), b=vec)


def get_angle(point1, point2, origin):
    dx = point1.x - origin.x
    dy = point1.y - origin.y
    dx2 = point2.x - origin.x
    dy2 = point2.y - origin.y

    scal_mul = dx * dx2 + dy * dy2
    modul = get_length_vector(sd.get_point(x=dx, y=dy))
    modul2 = get_length_vector(sd.get_point(x=dx2, y=dy2))
    modul_mul = modul * modul2

    if modul_mul == 0:
        modul_mul = 1e-7

    try:
        cos_a = scal_mul / modul_mul
        angle = math.acos(cos_a) * 180 / 3.14159
    except:
        angle = 0
    return angle


class Bone:

    def __init__(self, point, color=sd.COLOR_YELLOW):
        self._base_point = point
        self.angle = 0
        self.adv_angle = 0
        self.old_point_end = point
        self.old_point_start = point
        self.color = color
        self.length = 0
        self.parent = None
        self.children = []
        self.level = 0

    def redraw(self):
        angle = self.angle + self.adv_angle
        sd.line(start_point=self.old_point_start, end_point=self.old_point_end, color=sd.background_color, width=2)
        vector = sd.get_vector(start_point=self.base_point, angle=angle, length=self.length)
        vector.draw(color=self.color, width=2)
        self.old_point_end = vector.end_point
        self.old_point_start = copy.deepcopy(self.base_point)

    def set_parent(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        self.base_point = copy.deepcopy(self._base_point)
        self.level = self.parent.level + 1

    @property
    def base_point(self):
        if self.parent is not None:
            vector = sd.get_vector(start_point=self.parent.base_point, angle=self.parent.angle + self.adv_angle,
                                   length=self.parent.length)
            parent_base_point = vector.end_point
        else:
            parent_base_point = self._base_point  # sd.get_point(x=0, y=0)
        return sd.get_point(x=parent_base_point.x,
                            y=parent_base_point.y)

    @base_point.setter
    def base_point(self, point):
        if self.parent is not None:
            vector = sd.get_vector(start_point=self.parent.base_point, angle=self.parent.angle,
                                   length=self.parent.length)
            parent_base_point = vector.end_point
        else:
            parent_base_point = sd.get_point(x=0, y=0)

        dx = point.x - parent_base_point.x
        dy = point.y - parent_base_point.y
        self._base_point = sd.get_point(x=dx, y=dy)

    def set_to_point(self, point):
        dx = point.x - self.base_point.x
        dy = point.y - self.base_point.y
        modul = get_length_vector(sd.get_point(x=dx, y=dy))
        if modul == 0:
            modul = dx + dy + 1e-7

        cos_a = dx / modul
        angle = math.acos(cos_a) * 180 / 3.14159
        length = get_length_vector(sd.get_point(x=dx, y=dy))
        self.angle = angle
        self.length = length


class UserHand:

    def __init__(self):
        point = sd.random_point()
        self.base_point = point
        self.next_point = point
        self.angle = 0

    def get_angle(self, origin):
        dx = self.base_point.x - origin.x
        dy = self.base_point.y - origin.y
        dx2 = self.next_point.x - origin.x
        dy2 = self.next_point.y - origin.y

        scal_mul = dx * dx2 + dy * dy2
        modul = get_length_vector(sd.get_point(x=dx, y=dy))
        modul2 = get_length_vector(sd.get_point(x=dx2, y=dy2))
        modul_mul = modul * modul2

        if modul_mul == 0:
            modul_mul = 1e-7

        try:
            cos_a = scal_mul / modul_mul
            angle = math.acos(cos_a) * 180 / 3.14159
            self.angle = angle
        except:
            self.angle = 0


EMPTY_MODE = 0
START_MODE = 1
GET_POS_MOD = 2

user_hand = UserHand()

bones = []
mode = EMPTY_MODE
vector = sd.get_point(x=0, y=0)
base_bone = None
if __name__ == "__main__":
    sd._init()
    sign_rot = 1
    counter_level_1 = 0
    while True:
        mouse_pos, mouse_buttons = sd.get_mouse_state()
        point = mouse_pos

        if mouse_buttons[0] == 1 and mode == EMPTY_MODE:
            bone = Bone(point=point)
            bones.append(bone)
            base_bone = bones[0]

            mode = START_MODE

        elif mouse_buttons[0] == 0 and mode == START_MODE:
            bone = bones[-1]
            bone.set_to_point(point=point)
            if len(bones) > 1:
                sub_length = 1000
                sub_parent = bones[0]
                for sub_bone in bones:
                    if sub_bone is bone:
                        continue

                    _length = length_line(a=bone.base_point, b=sub_bone.old_point_end)
                    if _length < sub_length:
                        sub_parent = sub_bone
                        sub_length = _length
                if sub_length < 20:
                    bone.set_parent(sub_parent)

            mode = EMPTY_MODE
        elif mouse_buttons[0] == 1 and mode == START_MODE:
            bone = bones[-1]
            bone.set_to_point(point=point)

        elif mouse_buttons[2] == 1 and mode == EMPTY_MODE:
            user_hand.base_point = point
            mode = GET_POS_MOD
        elif mouse_buttons[2] == 1 and mode == GET_POS_MOD:
            user_hand.next_point = point
            user_hand.get_angle(origin=base_bone.base_point)
        elif mouse_buttons[2] == 0 and mode == GET_POS_MOD:
            user_hand.angle = 0
            mode = EMPTY_MODE

        sd.start_drawing()

        if base_bone:
            base_bone.adv_angle = user_hand.angle

        counter_level_1 += 1
        for bone in bones:
            bone.adv_angle = user_hand.angle
            if bone.level > 0:
                bone.angle += bone.adv_angle * bone.level * sign_rot / 80
                if counter_level_1 > 200:
                    sign_rot = -1
                if counter_level_1 > 400:
                    sign_rot = 1
                    counter_level_1 = 0
            bone.redraw()

        sd.finish_drawing()
        if sd.user_want_exit():
            break
