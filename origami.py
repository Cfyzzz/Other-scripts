import simple_draw as sd
from lesson_004.Draw3D import Mesh
from lesson_004.Draw3D import length_line

vertices = [
    [40, 100],
    [0, 0], [0, 10], [0, 40], [0, 60], [0, 83], [0, 90], [0, 100],
    [40, 0],
    [80, 0], [80, 10], [80, 40], [80, 60], [80, 83], [80, 90], [80, 100],
    [40, 60],
    [0, 74], [80, 74],
    [40, 45],  # 19
    [15, 0], [65, 0],
    [40, 0, 20], [65, 0]
]

polygons = [
    (8, 20, 0), (8, 0, 21), (20, 1, 2, 0), (21, 0, 10, 9), (2, 3, 0), (10, 0, 11), (3, 4, 0), (11, 0, 12), (4, 17, 0),
    (12, 0, 18), (17, 5, 0), (18, 0, 13), (5, 6, 0), (13, 0, 14), (6, 7, 0), (14, 0, 15)
]

COLOR = (240, 240, 240)
COLOR_BACK = (120, 0, 0)

plain = Mesh(vertices=vertices, polygons=polygons)
plain.scale([4, 4])
plain.move_to(point=sd.get_point(300, 300))
plain.rotate(-2)


def clear_screen():
    sd.rectangle(left_bottom=sd.get_point(0, 0), right_top=sd.get_point(*sd.resolution), color=sd.background_color)


def act_one():
    sd.start_drawing()
    plain.render(color=COLOR, color_back=COLOR_BACK)
    # sd.line(start_point=sd.get_point(300, 300), end_point=sd.get_point(301, 301), color=sd.COLOR_RED, width=2)
    sd.finish_drawing()


def distance_point_to_line(pa, pb1, pb2):
    a = pb2[1] - pb1[1]
    b = pb2[0] - pb1[0]
    c = pb2[0] * pb1[1] - pb2[1] * pb1[0]
    numerator = abs(a * pa[0] - b * pa[1] + c)
    denominator = (a * a + b * b) ** .5
    if denominator < 1e-7:
        distance = ((pa[1] - pb1[1]) ** 2 + (pa[0] - pb1[0]) ** 2) ** .5
    else:
        distance = numerator / denominator
    return distance


def flip_paper(index_points, index_axe_points, idx_purpose_first, steps, callback=None):
    points = [plain.vertices[idx] for idx in index_points]
    axe_points = [plain.vertices[idx] for idx in index_axe_points]
    radii = []
    for point in points:
        radius = distance_point_to_line(pa=point, pb1=axe_points[0], pb2=axe_points[1])
        radii.append(radius)

    # center = list(map(lambda a: (a[0] + a[1]) // 2, zip(axe_points[0], axe_points[1])))
    purpose_first = plain.vertices[idx_purpose_first]
    center = list(map(lambda a: (a[0] + a[1]) // 2, zip(purpose_first, points[0])))
    vector = list(map(lambda a: a[0] - a[1], zip(center, points[0])))
    normal_vector = list(map(lambda a: a / radii[0], vector))
    centers = []
    for point, radius in zip(points, radii):
        delta_vec = list(map(lambda a: int(a * radius), normal_vector))
        center_p = list(map(lambda a: (a[0] + a[1]), zip(point, delta_vec)))
        centers.append(center_p)

    for step in range(int(steps)):
        if steps // 2 - 1 == step and callback:
            result = callback()
            callback = None
            if result == "finish":
                return

        sd.start_drawing()
        clear_screen()
        angle = 180 * (step + 1) / steps
        z = sd.sin(angle)
        percent_dist = sd.cos(angle)
        for point, radius, center_p in zip(points, radii, centers):
            vec_p = list(map(lambda a: int(-a * radius * percent_dist), normal_vector))
            point[0] = center_p[0] + vec_p[0]
            point[1] = center_p[1] + vec_p[1]
            point[2] = center_p[2] + int(z * radius)

        plain.render(color=COLOR, color_back=COLOR_BACK)
        sd.finish_drawing()
        sd.sleep(0.1)


def rotate_paper(angle, steps):
    angle = angle / steps
    for _ in range(steps):
        sd.start_drawing()
        clear_screen()
        plain.rotate(angle)
        plain.render(color=COLOR, color_back=COLOR_BACK)
        sd.finish_drawing()
        sd.sleep(0.05)


def up_prioritet(idx_pol, idx):
    polygon = plain.polygons.pop(idx_pol)
    plain.polygons.insert(idx, polygon)


def act_two():
    points = [15, 14, 13, 18]
    axe_points = [0, 12]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=16, steps=20)


def act_three():
    points = [7, 6, 5, 17]
    axe_points = [4, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=16, steps=20)


def act_four():
    def up_pol():
        up_prioritet(idx_pol=7, idx=15)
        up_prioritet(idx_pol=5, idx=15)

    points = [12, 18, 11]
    axe_points = [10, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=19, steps=20, callback=up_pol)


def act_five():
    def up_pol():
        up_prioritet(idx_pol=5, idx=15)
        up_prioritet(idx_pol=4, idx=15)

    points = [4, 17, 3]
    axe_points = [2, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=19, steps=20, callback=up_pol)


def act_six():
    def finish():
        up_prioritet(idx_pol=3, idx=15)
        # return "finish"

    points = [10, 13, 9]
    axe_points = [21, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=8, steps=20, callback=finish)


def act_seven():
    def finish():
        up_prioritet(idx_pol=2, idx=15)
        # return "finish"

    points = [2, 5, 1]
    axe_points = [20, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=8, steps=20, callback=finish)


def act_eight():
    def finish():
        return "finish"

    points = [21, 9, 10, 11, 18, 13, 14]
    axe_points = [8, 0]
    flip_paper(index_points=points, index_axe_points=axe_points, idx_purpose_first=20, steps=20, callback=None)


def act_nine():
    for deg in range(40):
        sd.start_drawing()
        clear_screen()
        plain.rotateY(angle_deg=2)
        plain.render(color=COLOR, color_back=COLOR_BACK, need_edge=True)
        sd.finish_drawing()
        sd.sleep(0.1)


def main():
    act_one()
    sd.sleep(5)
    act_two()
    rotate_paper(angle=4, steps=10)
    act_three()
    rotate_paper(angle=-10, steps=10)  # -6
    act_four()
    rotate_paper(angle=8, steps=10)  # +2
    act_five()
    rotate_paper(angle=-3, steps=10)  # -1
    act_six()
    act_seven()
    act_eight()

    sd.pause()


if __name__ == "__main__":
    main()
