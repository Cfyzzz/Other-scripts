import simple_draw as sd


class Segment:
    def __init__(self):
        self.points = [sd.Point() for _ in range(4)]

    def calc_p1(self, t, b):
        if t == 0:
            t = 1e-6
        if t == 1:
            t -= 1e-6

        nt = 1 - t
        nt2 = nt * nt
        t2 = t * t

        p = sd.Point()
        p.x = (b.x - nt2 * self.points[0].x - t2 * self.points[2].x) / (2 * t * nt)
        p.y = (b.y - nt2 * self.points[0].y - t2 * self.points[2].y) / (2 * t * nt)
        self.points[1] = p

    def calc(self, t, b):
        nt = 1 - t
        nt2 = nt * nt
        t2 = t * t

        b.x = nt2 * self.points[0].x + 2 * t * nt * self.points[1].x + t2 * self.points[2].x
        b.y = nt2 * self.points[0].y + 2 * t * nt * self.points[1].y + t2 * self.points[2].y


def find_all_segments(verts, min_vts=3):
    if len(verts) < min_vts:
        return []

    segments = []
    for idx, vert in enumerate(verts[:-1]):
        segments.append([vert, verts[idx + 1]])
    return segments


def copy(p: sd.Point) -> sd.Point:
    return sd.Point(p.x, p.y)


def loopResolve(verts, STEP, dist=None):
    def getTBSegment(segment, Pc, T, R, D):
        kk = (1 - T) * 0.5
        t = kk + T
        k_extr = 0
        b = sd.Point()
        for cycle in range(100):
            segment.calc(t, b)
            d_ = length_line(b, Pc) - R

            if abs(d_) <= D:
                return (t, b)

            if kk == k_extr:
                k = -0.5 if d_ > 0 else 0.5
            else:
                k = -1 if d_ > 0 else 1
                k_extr = kk

            kk *= k
            t += kk
            kk = abs(kk)
        return (t, b)

    segments_2d = [verts]
    if not segments_2d:
        return False

    # Запускаем 2д-перестроение по сплайну
    lv_for_del = []
    old_len_lfd = 0
    old_len_bmv = 0
    bm_verts = []

    for i, sort_list_ in enumerate(segments_2d):

        if len(sort_list_) == 2:
            extreme_vs = sort_list_
        else:
            extreme_vs = [sort_list_[0], sort_list_[-1]]

        sort_list = sort_list_[:]
        list_length = []
        sum_length = 0.0
        cou_vs = len(sort_list) - 1
        list_koeff = []
        if cou_vs == 1:
            p1co = sd.Point(sort_list[0].x, sort_list[0].y)
            p3co = sd.Point(sort_list[1].x, sort_list[1].y)
            p2co = sd.Point((p1co.x + p3co.x) / 2, (p1co.y + p3co.y) / 2)
            sum_length = length_line(p3co, p1co)

            list_koeff = [0.5, 0.5]
            values = [p1co, p2co, p3co]
        else:
            for sl in range(cou_vs):
                subb_length = length_line(sort_list[sl + 1], sort_list[sl])
                sum_length += subb_length
                list_length.append(subb_length)

            for sl in range(cou_vs):
                tmp = list_length[sl] / sum_length
                list_koeff.append(tmp)

            values = sort_list[:]

        n = len(values) - 1
        bezier = [Segment() for _ in range(n)]

        step_ = STEP - 1
        new_vts = []

        if not dist:
            r = sum_length / step_
        else:
            r = dist
            step_ = 1e+6

        pi_ = 0
        delta = 0.001
        for i in range(n):
            if i == n - 1:
                pi_ = 1

            tl = list_koeff[i - pi_]
            tr = list_koeff[i + 1 - pi_]
            tt = tl / (tl + tr)

            bezier[i].points[0] = values[i - pi_]
            b = values[i + 1 - pi_]
            bezier[i].points[2] = values[i + 2 - pi_]
            bezier[i].calc_p1(tt, b)
            bezier[i].points[3] = b

        for j in range(4):
            segment = bezier[0]
            Pc = copy(segment.points[0])
            t = 0
            i = 0
            ii = 0
            iii = 0
            pi_ = 0
            i_virtual = 0
            dr = 0
            old_point = copy(extreme_vs[0])
            while i < len(bezier):
                ii += 1
                segment = bezier[i]
                if i == len(bezier) - 1:
                    pi_ = 1

                if length_line(Pc, segment.points[3 - pi_]) < r:
                    t = 0 if i < len(bezier) - 2 else t
                    i += 1
                    if i_virtual < step_:
                        i_virtual += 1
                    if i == len(bezier) and j == 3:
                        t, b = getTBSegment(segment, Pc, t, r, delta)
                        if len(new_vts) < step_:
                            new_vts.append(copy(b))
                    continue

                t, b = getTBSegment(segment, Pc, t, r, delta)
                Pc = b
                if i_virtual < step_ + 1:
                    i_virtual += 1

                if j == 3:
                    if len(new_vts) < step_:
                        new_vts.append(copy(b))

                iii += 1
                dr += length_line(old_point, Pc)
                old_point = copy(Pc)

            r = dr / iii
            if dist:
                r = dist

        new_vts.insert(0, copy(extreme_vs[0]))

        # В списке new_vts имеем координаты новых вершин
        lv_for_del.extend(verts)
        for v in new_vts[1:-1]:
            new_v = copy(v)
            bm_verts.append(new_v)

        v0_insert = lv_for_del.pop(old_len_lfd)
        v1_insert = lv_for_del.pop(-1)

        bm_verts.insert(old_len_bmv, v0_insert)
        bm_verts.append(v1_insert)

        old_len_lfd = len(lv_for_del)
        old_len_bmv = len(bm_verts)

    for v in lv_for_del:
        if v in verts:
            verts.remove(v)

    verts.pop()
    verts.extend(bm_verts)
    return True


def length_line(a, b):
    """Длина линии между двумя точками"""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def test_resolve(verts):
    loopResolve(verts=verts, STEP=100)
