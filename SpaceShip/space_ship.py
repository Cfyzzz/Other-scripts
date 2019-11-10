import simple_draw as sd

import Draw3D
from space_ship_data import vertices, polygons

COLOR = (240, 240, 240)
COLOR_BACK = (120, 0, 0)


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def rotate_paper(angle, steps):
    angle = angle / steps
    for _ in range(steps):
        sd.start_drawing()
        clear_screen()
        plain.rotateY(angle)
        plain.render(color=COLOR, need_edge=True)
        sd.finish_drawing()
        sd.sleep(0.05)


def main():
    sd.start_drawing()
    plain.render(color=COLOR, need_edge=True)
    sd.finish_drawing()
    sd.sleep(5)
    rotate_paper(360, 240)

    sd.pause()


plain = Draw3D.Mesh(vertices=vertices, polygons=polygons)
plain.scale([100, 100, 100])
plain.move_to(point=sd.get_point(300, 300))
plain.rotateX(60)
plain.rotateY(200)

if __name__ == "__main__":
    sd.caption = "Space ship"
    main()
