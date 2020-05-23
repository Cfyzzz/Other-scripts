import simple_draw as sd

class Segment:
    # def __init__(self):
    #     self.points = [sd.Point() for _ in range(4)]
    #
    # def calc_p1(self, t, b):
    #     if t == 0:
    #         t = 1e-6
    #     if t == 1:
    #         t -= 1e-6
    #
    #     nt = 1 - t
    #     nt2 = nt * nt
    #     t2 = t * t
    #
    #     p = sd.Point()
    #     p.x = (b.x - nt2 * self.points[0].x - t2 * self.points[2].x) / (2 * t * nt)
    #     p.y = (b.y - nt2 * self.points[0].y - t2 * self.points[2].y) / (2 * t * nt)
    #     self.points[1] = p
    #
    # def calc(self, t, b):
    #     nt = 1 - t
    #     nt2 = nt * nt
    #     t2 = t * t
    #
    #     b.x = nt2 * self.points[0].x + 2 * t * nt * self.points[1].x + t2 * self.points[2].x
    #     b.y = nt2 * self.points[0].y + 2 * t * nt * self.points[1].y + t2 * self.points[2].y
    pass


class BuilderSplines:
    # def getTBSegment(segment, Pc, T, R, D):
    #     kk = (1 - T) * 0.5
    #     t = kk + T
    #     k_extr = 0
    #     b = sd.Point()
    #     for cycle in range(100):
    #         segment.calc(t, b)
    #         d_ = (b - Pc).length - R
    #
    #         if abs(d_) <= D: return (t, b)
    #
    #         if kk == k_extr:
    #             k = -0.5 if d_ > 0 else 0.5
    #         else:
    #             k = -1 if d_ > 0 else 1
    #             k_extr = kk
    #
    #         kk *= k
    #         t += kk
    #         kk = abs(kk)
    #     return (t, b)
    #
    # def build(self):
    #     lv_for_del = []
    #     old_len_lfd = 0
    #     old_len_bmv = 0
    #
    #     list_length = []
    #     sum_length = 0.0
    #     cou_vs = len(sort_list) - 1
    #     list_koeff = []
    #     if cou_vs == 1:
    #         p1co = me.vertices[sort_list[0]].co.copy()
    #         p3co = me.vertices[sort_list[1]].co.copy()
    #         p2co = (p1co + p3co) / 2
    #         sum_length = (p3co - p1co).length
    #         # list_length = [sum_length / 2, sum_length]
    #         list_koeff = [0.5, 0.5]
    #         values = [p1co, p2co, p3co]
    #     else:
    #         for sl in range(cou_vs):
    #             subb = me.vertices[sort_list[sl + 1]].co - me.vertices[sort_list[sl]].co
    #             sum_length += subb.length
    #             list_length.append(subb.length)
    #
    #         for sl in range(cou_vs):
    #             tmp = list_length[sl] / sum_length
    #             list_koeff.append(tmp)
    #
    #         values = [me.vertices[i].co.copy() for i in sort_list]
    #
    #     n = len(values) - 1
    #     bezier = [Segment() for _ in range(n)]
    #
    #     step_ = STEP - 1
    #     new_vts = []
    #
    #     if not dist:
    #         r = sum_length / (step_)
    #     else:
    #         r = dist
    #         step_ = 1e+6
    #
    #     pi_ = 0
    #     delta = 0.001
    #     for i in range(n):
    #         if i == n - 1: pi_ = 1
    #
    #         tl = list_koeff[i - pi_]
    #         tr = list_koeff[i + 1 - pi_]
    #         tt = tl / (tl + tr)
    #
    #         bezier[i].points[0] = values[i - pi_]
    #         b = values[i + 1 - pi_]
    #         bezier[i].points[2] = values[i + 2 - pi_]
    #         bezier[i].calc_p1(tt, b)
    #         bezier[i].points[3] = b
    #
    #     for j in range(4):
    #         segment = bezier[0]
    #         Pc = segment.points[0].copy()
    #         t = 0
    #         i = 0
    #         ii = 0
    #         iii = 0
    #         pi_ = 0
    #         i_virtual = 0
    #         dr = 0
    #         old_point = me.vertices[extreme_vs[0]].co.copy()
    #         while i < len(bezier):
    #             ii += 1
    #             segment = bezier[i]
    #             if i == len(bezier) - 1: pi_ = 1
    #
    #             if (Pc - segment.points[3 - pi_]).length < r:
    #                 t = 0 if i < len(bezier) - 2 else t
    #                 i += 1
    #                 if i_virtual < step_: i_virtual += 1
    #                 if i == len(bezier) and j == 3:
    #                     t, b = getTBSegment(segment, Pc, t, r, delta)
    #                     if len(new_vts) < step_: new_vts.append(b.copy())
    #                 continue
    #
    #             t, b = getTBSegment(segment, Pc, t, r, delta)
    #             Pc = b
    #             if i_virtual < step_ + 1:
    #                 # Pc1 = Pc.copy()
    #                 i_virtual += 1
    #
    #             if j == 3:
    #                 if len(new_vts) < step_: new_vts.append(b.copy())
    #
    #             iii += 1
    #             dr += (old_point - Pc).length
    #             old_point = Pc.copy()
    #
    #         r = dr / iii
    #         if dist:
    #             r = dist
    #
    #         new_vts.insert(0, me.vertices[extreme_vs[0]].co)
    #
    #         # В списке new_vts имеем координаты новых вершин
    #         edit_mode_out()
    #         lv_for_del.extend([bm.verts[vi] for vi in sort_list])
    #         for v in new_vts[1:-1]:
    #             new_v = bm.verts.new(v)
    #             new_v.select = True
    #             bm_verts.append(new_v)
    #
    #         check_lukap(bm)
    #
    #         v0_insert = lv_for_del.pop(old_len_lfd)
    #         v1_insert = lv_for_del.pop(-1)
    #         if len(sort_list) == 2:
    #             edge = bm.edges.get([v0_insert, v1_insert], False)
    #             if edge: remove_edges.append(edge)
    #
    #         bm_verts.insert(old_len_bmv, v0_insert)
    #         bm_verts.append(v1_insert)
    #         bm_verts[old_len_bmv].select = True
    #         bm_verts[-1].select = True
    #         bm_edges = list(zip(bm_verts[old_len_bmv:-1], bm_verts[1 + old_len_bmv:]))
    #         old_len_lfd = len(lv_for_del)
    #         old_len_bmv = len(bm_verts)
    #
    #         for edge in bm_edges:
    #             if not bm.edges.get(edge, False):
    #                 ed_ = bm.edges.new(edge)
    #                 ed_.select = True
    #             else:
    #                 for i, re in enumerate(remove_edges):
    #                     if edge[0] in re.verts and edge[1] in re.verts:
    #                         remove_edges.pop(i)
    #                         break
    #
    #     check_lukap(bm)
    #     for e in remove_edges:
    #         bm.edges.remove(e)
    #
    #     for v in lv_for_del:
    #         if v in bm.verts:
    #             bm.verts.remove(v)
    #
    #     check_lukap(bm)
    #     bm.to_mesh(me)
    #     bm.free()
    #     edit_mode_in()
    #     return True
    #
    # def main_spline(context, mode, influe):
    #     verts = find_index_of_selected_vertex(me)
    #     cou_vs = len(verts) - 1
    #     if verts != None and cou_vs > 0:
    #         extreme_vs = find_extreme_select_verts(me, verts)
    #
    #         if len(extreme_vs) != 2:
    #             print_error('Single Loop only')
    #             print('Error: 01 simple_spline')
    #             return False
    #
    #         sort_list = find_all_connected_verts(me, extreme_vs[0], [])
    #         all_vts_sort_x = [me.vertices[i].co.x for i in sort_list]
    #         all_vts_sort_y = [me.vertices[i].co.y for i in sort_list]
    #         all_vts_sort_z = [me.vertices[i].co.z for i in sort_list]
    #
    #         max_p = [max(all_vts_sort_x), max(all_vts_sort_y), max(all_vts_sort_z)]
    #         min_p = [min(all_vts_sort_x), min(all_vts_sort_y), min(all_vts_sort_z)]
    #         diap_p = list(map(lambda a, b: a - b, max_p, min_p))
    #
    #         if len(sort_list) != len(verts):
    #             print_error('Incoherent loop')
    #             print('Error: 020 simple_spline')
    #             return False
    #
    #         list_length = []
    #         sum_length = 0.0
    #         for sl in range(cou_vs):
    #             subb = me.vertices[sort_list[sl + 1]].co - me.vertices[sort_list[sl]].co
    #             sum_length += subb.length
    #             list_length.append(sum_length)
    #
    #         list_koeff = []
    #         for sl in range(cou_vs):
    #             tmp = list_length[sl] / sum_length
    #             list_koeff.append(tmp)
    #
    #         bpy.ops.object.mode_set(mode='OBJECT')
    #         bm = bmesh.new()
    #         bm.from_mesh(me)
    #         check_lukap(bm)
    #
    #         pa_idx = bm_vert_active_get(bm)[0]
    #         if pa_idx == None:
    #             print_error('Active vert is not detected')
    #             print('Error: 030 simple_spline')
    #             return False
    #
    #         pa_sort = sort_list.index(pa_idx)
    #         if pa_sort == 0: pa_sort = 1
    #         pa_perc = list_koeff[pa_sort - 1]
    #         p0_ = me.vertices[sort_list[0]].co
    #         p1_ = me.vertices[pa_idx].co
    #         p2_ = me.vertices[sort_list[-1]].co
    #
    #         if mode[3]:
    #             l = len(list_koeff)
    #             d = 1 / l
    #             list_koeff = list(map(lambda n: d * n, list(range(1, l + 1))))
    #
    #         if mode[0]:
    #             all_vts_sort = [me.vertices[i].co.x for i in sort_list]
    #             p0 = p0_.x
    #             p1 = p1_.x - p0
    #             p2 = p2_.x - p0
    #
    #             t = pa_perc
    #             if p1 == 0 or p1 == p2:
    #                 new_vts = list(map(lambda t: p2 * t ** 2, list_koeff))
    #             else:
    #                 b = (p1 - pa_perc ** 2 * p2) / (2 * pa_perc * (1 - pa_perc) + 1e-8)
    #                 new_vts = list(map(lambda t: 2 * b * t * (1 - t) + p2 * t ** 2, list_koeff))
    #
    #             for idx in range(cou_vs):
    #                 me.vertices[sort_list[idx + 1]].co.x += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 1]].co.x) * influe
    #
    #         if mode[1]:
    #             all_vts_sort = [me.vertices[i].co.y for i in sort_list]
    #             p0 = p0_.y
    #             p1 = p1_.y - p0
    #             p2 = p2_.y - p0
    #
    #             b = (p1 - pa_perc ** 2 * p2) / (2 * pa_perc * (1 - pa_perc) + 1e-8)
    #             new_vts = list(map(lambda t: 2 * b * t * (1 - t) + p2 * t ** 2, list_koeff))
    #
    #             for idx in range(cou_vs):
    #                 me.vertices[sort_list[idx + 1]].co.y += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 1]].co.y) * influe
    #
    #         if mode[2]:
    #             all_vts_sort = [me.vertices[i].co.z for i in sort_list]
    #             p0 = p0_.z
    #             p1 = p1_.z - p0
    #             p2 = p2_.z - p0
    #
    #             b = (p1 - pa_perc ** 2 * p2) / (2 * pa_perc * (1 - pa_perc) + 1e-8)
    #             new_vts = list(map(lambda t: 2 * b * t * (1 - t) + p2 * t ** 2, list_koeff))
    #
    #             for idx in range(cou_vs):
    #                 me.vertices[sort_list[idx + 1]].co.z += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 1]].co.z) * influe
    #
    #         me.update()
    #         bm.free()
    #
    #         bpy.ops.object.mode_set(mode='EDIT')
    #
    #     return True
    #
    # def main_B_spline(context, mode, influe):
    #     global steps_smoose
    #     bpy.ops.object.mode_set(mode='OBJECT')
    #     bpy.ops.object.mode_set(mode='EDIT')
    #
    #     obj = bpy.context.active_object
    #     me = obj.data
    #
    #     verts = find_index_of_selected_vertex(me)
    #     cou_vs = len(verts) - 1
    #     if verts != None and cou_vs > 0:
    #         extreme_vs = find_extreme_select_verts(me, verts)
    #
    #         if len(extreme_vs) != 2:
    #             print_error('Single Loop only')
    #             print('Error: 01 B_spline')
    #             return False
    #
    #         sort_list = find_all_connected_verts(me, extreme_vs[0], [])
    #         all_vts_sort_x = [me.vertices[i].co.x for i in sort_list]
    #         all_vts_sort_y = [me.vertices[i].co.y for i in sort_list]
    #         all_vts_sort_z = [me.vertices[i].co.z for i in sort_list]
    #
    #         max_p = [max(all_vts_sort_x), max(all_vts_sort_y), max(all_vts_sort_z)]
    #         min_p = [min(all_vts_sort_x), min(all_vts_sort_y), min(all_vts_sort_z)]
    #         diap_p = list(map(lambda a, b: a - b, max_p, min_p))
    #
    #         if len(sort_list) != len(verts):
    #             print_error('Incoherent loop')
    #             print('Error: 020 B_spline')
    #             return False
    #
    #         list_length = []
    #         sum_length = 0.0
    #         for sl in range(cou_vs - 2):
    #             subb = me.vertices[sort_list[sl + 2]].co - me.vertices[sort_list[sl + 1]].co
    #             sum_length += subb.length
    #             list_length.append(sum_length)
    #
    #         list_koeff = []
    #         for sl in range(cou_vs - 2):
    #             tmp = list_length[sl] / sum_length
    #             list_koeff.append(tmp)
    #
    #         bpy.ops.object.mode_set(mode='OBJECT')
    #         bm = bmesh.new()
    #         bm.from_mesh(me)
    #         check_lukap(bm)
    #
    #         pa_idx = bm_vert_active_get(bm)[0]
    #         if pa_idx == None:
    #             print_error('Active vert is not detected')
    #             print('Error: 030 B_spline')
    #             return False
    #
    #         pa_sort = sort_list.index(pa_idx)
    #         if pa_sort < 2: pa_sort = 2
    #         if pa_sort > len(sort_list) - 3: pa_sort = len(sort_list) - 3
    #         pa_idx = sort_list[pa_sort]
    #         pa_perc = list_koeff[pa_sort - 2]
    #         p0_ = me.vertices[sort_list[1]].co
    #         p1_ = me.vertices[pa_idx].co
    #         p2_ = me.vertices[sort_list[-2]].co
    #
    #         kn1_ = me.vertices[sort_list[0]].co
    #         kn2_ = me.vertices[sort_list[-1]].co
    #         nkn1_ = p1_ - kn1_ + p1_
    #         nkn2_ = p2_ - kn2_ + p2_
    #
    #         if mode[3]:
    #             l = len(list_koeff)
    #             d = 1 / l
    #             list_koeff = list(map(lambda n: d * n, list(range(1, l + 1))))
    #
    #         if mode[0]:
    #             all_vts_sort = [me.vertices[i].co.x for i in sort_list]
    #             p0 = p0_.x
    #             p1 = p1_.x - p0
    #             p2 = p2_.x - p0
    #             knot_1 = nkn1_.x - p0
    #             knot_2 = nkn2_.x - p0
    #
    #             t = pa_perc
    #             b = (p1 - (4 * knot_1 * t * (1 - t) ** 3) - (4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                     4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #             new_vts = list(
    #                 map(lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                         1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = [0] + new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 0
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #                     new_vts = list(map(
    #                         lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                 1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs - 2):
    #                 me.vertices[sort_list[idx + 2]].co.x += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 2]].co.x) * influe
    #
    #         if mode[1]:
    #             all_vts_sort = [me.vertices[i].co.y for i in sort_list]
    #             p0 = p0_.y
    #             p1 = p1_.y - p0
    #             p2 = p2_.y - p0
    #             knot_1 = nkn1_.y - p0
    #             knot_2 = nkn2_.y - p0
    #
    #             t = pa_perc
    #             b = (p1 - (4 * knot_1 * t * (1 - t) ** 3) - (4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                     4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #             new_vts = list(
    #                 map(lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                         1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = [0] + new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 0
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #                     new_vts = list(map(
    #                         lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                 1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs - 2):
    #                 me.vertices[sort_list[idx + 2]].co.y += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 2]].co.y) * influe
    #
    #         if mode[2]:
    #             all_vts_sort = [me.vertices[i].co.z for i in sort_list]
    #             p0 = p0_.z
    #             p1 = p1_.z - p0
    #             p2 = p2_.z - p0
    #             knot_1 = nkn1_.z - p0
    #             knot_2 = nkn2_.z - p0
    #
    #             t = pa_perc
    #             b = (p1 - (4 * knot_1 * t * (1 - t) ** 3) - (4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                     4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #             new_vts = list(
    #                 map(lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                         1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = [0] + new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 0
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #                     new_vts = list(map(
    #                         lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                 1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs - 2):
    #                 me.vertices[sort_list[idx + 2]].co.z += (new_vts[idx] + p0 - me.vertices[
    #                     sort_list[idx + 2]].co.z) * influe
    #
    #         me.update()
    #         bm.free()
    #
    #         bpy.ops.object.mode_set(mode='EDIT')
    #
    #     return True
    #
    # def main_B_spline_2(context, mode, influe):
    #     global steps_smoose
    #     bpy.ops.object.mode_set(mode='OBJECT')
    #     bpy.ops.object.mode_set(mode='EDIT')
    #
    #     obj = bpy.context.active_object
    #     me = obj.data
    #
    #     verts = find_index_of_selected_vertex(me)
    #     cou_vs = len(verts) - 1
    #     if verts != None and cou_vs > 0:
    #         extreme_vs = find_extreme_select_verts(me, verts)
    #
    #         if len(extreme_vs) != 2:
    #             print_error('Single Loop only')
    #             print('Error: 01 B_spline')
    #             return False
    #
    #         sort_list = find_all_connected_verts(me, extreme_vs[0], [])
    #         all_vts_sort_x = [me.vertices[i].co.x for i in sort_list]
    #         all_vts_sort_y = [me.vertices[i].co.y for i in sort_list]
    #         all_vts_sort_z = [me.vertices[i].co.z for i in sort_list]
    #
    #         max_p = [max(all_vts_sort_x), max(all_vts_sort_y), max(all_vts_sort_z)]
    #         min_p = [min(all_vts_sort_x), min(all_vts_sort_y), min(all_vts_sort_z)]
    #         diap_p = list(map(lambda a, b: a - b, max_p, min_p))
    #
    #         if len(sort_list) != len(verts):
    #             print_error('Incoherent loop')
    #             print('Error: 020 B_spline')
    #             return False
    #
    #         list_length = []
    #         sum_length = 0.0
    #         for sl in range(cou_vs):
    #             subb = me.vertices[sort_list[sl + 1]].co - me.vertices[sort_list[sl]].co
    #             sum_length += subb.length
    #             list_length.append(sum_length)
    #
    #         list_koeff = []
    #         for sl in range(cou_vs):
    #             tmp = list_length[sl] / sum_length
    #             list_koeff.append(tmp)
    #
    #         bpy.ops.object.mode_set(mode='OBJECT')
    #         bm = bmesh.new()
    #         bm.from_mesh(me)
    #         check_lukap(bm)
    #
    #         pa_idx = bm_vert_active_get(bm)[0]
    #         if pa_idx == None:
    #             print_error('Active vert is not detected')
    #             print('Error: 030 B_spline')
    #             return False
    #
    #         list_koeff = [0] + list_koeff
    #         pa_sort = sort_list.index(pa_idx)
    #         if pa_sort == 0:
    #             pa_perc = 0
    #             kn1_i = sort_list[0]
    #             kn2_i = sort_list[pa_sort + 1]
    #         elif pa_sort == len(sort_list) - 1:
    #             pa_perc = 1.0
    #             kn1_i = sort_list[pa_sort - 1]
    #             kn2_i = sort_list[-1]
    #         else:
    #             kn1_i = sort_list[pa_sort - 1]
    #             kn2_i = sort_list[pa_sort + 1]
    #             pa_perc = list_koeff[pa_sort]
    #
    #         kn1_ = me.vertices[kn1_i].co
    #         kn2_ = me.vertices[kn2_i].co
    #
    #         p0_ = me.vertices[sort_list[0]].co
    #         p1_ = me.vertices[pa_idx].co
    #         p2_ = me.vertices[sort_list[-1]].co
    #
    #         if mode[3]:
    #             l = len(list_koeff) - 1
    #             d = 1 / l
    #             list_koeff = list(map(lambda n: d * n, list(range(0, l + 1))))
    #
    #         if mode[0]:
    #             p0 = p0_.x
    #             p1 = p1_.x - p0
    #             p2 = p2_.x - p0
    #             knot_1 = kn1_.x - p0
    #             knot_2 = kn2_.x - p0
    #
    #             t = pa_perc
    #             if knot_1 == 0 and p1 != 0:
    #                 b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == 0:
    #                 new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             elif knot_2 == p2 and p1 != p2:
    #                 b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == p2:
    #                 new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             else:
    #                 b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                         4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(map(
    #                     lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                             1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 1e-8
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #
    #                     if knot_1 == 0 and p1 != 0:
    #                         b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == 0:
    #                         new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     elif knot_2 == p2 and p1 != p2:
    #                         b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == p2:
    #                         new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     else:
    #                         b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                                 4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(map(
    #                             lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                     1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs + 1):
    #                 me.vertices[sort_list[idx]].co.x += (new_vts[idx] + p0 - me.vertices[sort_list[idx]].co.x) * influe
    #
    #         if mode[1]:
    #             p0 = p0_.y
    #             p1 = p1_.y - p0
    #             p2 = p2_.y - p0
    #             knot_1 = kn1_.y - p0
    #             knot_2 = kn2_.y - p0
    #
    #             t = pa_perc
    #             if knot_1 == 0 and p1 != 0:
    #                 b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == 0:
    #                 new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             elif knot_2 == p2 and p1 != p2:
    #                 b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == p2:
    #                 new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             else:
    #                 b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                         4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(map(
    #                     lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                             1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 1e-8
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #
    #                     if knot_1 == 0 and p1 != 0:
    #                         b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == 0:
    #                         new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     elif knot_2 == p2 and p1 != p2:
    #                         b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == p2:
    #                         new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     else:
    #                         b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                                 4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(map(
    #                             lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                     1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs + 1):
    #                 me.vertices[sort_list[idx]].co.y += (new_vts[idx] + p0 - me.vertices[sort_list[idx]].co.y) * influe
    #
    #         if mode[2]:
    #             p0 = p0_.z
    #             p1 = p1_.z - p0
    #             p2 = p2_.z - p0
    #             knot_1 = kn1_.z - p0
    #             knot_2 = kn2_.z - p0
    #
    #             t = pa_perc
    #             if knot_1 == 0 and p1 != 0:
    #                 b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == 0:
    #                 new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             elif knot_2 == p2 and p1 != p2:
    #                 b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                 new_vts = list(
    #                     map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                         list_koeff))
    #             elif p1 == p2:
    #                 new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #             else:
    #                 b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                         4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                 new_vts = list(map(
    #                     lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                             1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     d = L / lp
    #                     l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                     l = list(map(lambda x: x / L, P))
    #
    #                     tmp = 1e-8
    #                     for i in range(lp):
    #                         tmp += l[i]
    #                         m = l_[i] / tmp
    #                         list_koeff[i] = m * list_koeff[i]
    #                     if knot_1 == 0 and p1 != 0:
    #                         b = (p1 - (3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3)) / (3 * t * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * b * t * (1 - t) ** 2 + 3 * knot_2 * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == 0:
    #                         new_vts = list(map(lambda t: 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     elif knot_2 == p2 and p1 != p2:
    #                         b = (p1 - (3 * knot_1 * t * (1 - t) ** 2 + p2 * t ** 3)) / (3 * t ** 2 * (1 - t) + 1e-8)
    #                         new_vts = list(
    #                             map(lambda t: 3 * knot_1 * t * (1 - t) ** 2 + 3 * b * t ** 2 * (1 - t) + p2 * t ** 3,
    #                                 list_koeff))
    #                     elif p1 == p2:
    #                         new_vts = list(map(lambda t: 2 * knot_1 * t * (1 - t) + p2 * t ** 2, list_koeff))
    #                     else:
    #                         b = (p1 - (4 * knot_1 * t * (1 - t) ** 3 + 4 * t ** 3 * (1 - t) * knot_2 + p2 * t ** 4)) / (
    #                                 4 * t ** 2 * (1 - t) ** 2 + 1e-8)
    #                         new_vts = list(map(
    #                             lambda t: 4 * knot_1 * t * (1 - t) ** 3 + 4 * b * t ** 2 * (1 - t) ** 2 + 4 * t ** 3 * (
    #                                     1 - t) * knot_2 + p2 * t ** 4, list_koeff))
    #
    #             for idx in range(cou_vs + 1):
    #                 me.vertices[sort_list[idx]].co.z += (new_vts[idx] + p0 - me.vertices[sort_list[idx]].co.z) * influe
    #
    #         me.update()
    #         bm.free()
    #
    #         bpy.ops.object.mode_set(mode='EDIT')
    #
    #     return True
    #
    # def main_Basier_mid(context, mode, influe):
    #     global steps_smoose
    #     bpy.ops.object.mode_set(mode='OBJECT')
    #     bpy.ops.object.mode_set(mode='EDIT')
    #
    #     obj = bpy.context.active_object
    #     me = obj.data
    #
    #     verts = find_index_of_selected_vertex(me)
    #     cou_vs = len(verts) - 1
    #     if verts != None and cou_vs > 0:
    #         extreme_vs = find_extreme_select_verts(me, verts)
    #
    #         if len(extreme_vs) != 2:
    #             print_error('Single Loop only')
    #             print('Error: 01 Basier_mid')
    #             return False
    #
    #         sort_list = find_all_connected_verts(me, extreme_vs[0], [])
    #         all_vts_sort_x = [me.vertices[i].co.x for i in sort_list]
    #         all_vts_sort_y = [me.vertices[i].co.y for i in sort_list]
    #         all_vts_sort_z = [me.vertices[i].co.z for i in sort_list]
    #
    #         max_p = [max(all_vts_sort_x), max(all_vts_sort_y), max(all_vts_sort_z)]
    #         min_p = [min(all_vts_sort_x), min(all_vts_sort_y), min(all_vts_sort_z)]
    #         diap_p = list(map(lambda a, b: a - b, max_p, min_p))
    #
    #         if len(sort_list) != len(verts):
    #             print_error('Incoherent loop')
    #             print('Error: 020 Basier_mid')
    #             return False
    #
    #         bpy.ops.object.mode_set(mode='OBJECT')
    #         bm = bmesh.new()
    #         bm.from_mesh(me)
    #         check_lukap(bm)
    #
    #         pa_idx = bm_vert_active_get(bm)[0]
    #         if pa_idx == None:
    #             bm.free()
    #             print_error('Active vert is not detected')
    #             print('Error: 030 Basier_mid')
    #             return False
    #
    #         pa_sort = sort_list.index(pa_idx)
    #
    #         list_length_a = []
    #         list_length_b = []
    #         sum_length_a = 0.0
    #         sum_length_b = 0.0
    #         for sl in range(pa_sort - 1):
    #             subb = me.vertices[sort_list[sl + 1]].co - me.vertices[sort_list[sl]].co
    #             sum_length_a += subb.length
    #             list_length_a.append(sum_length_a)
    #         for sl in range(cou_vs - pa_sort - 1):
    #             subb = me.vertices[sort_list[sl + 2 + pa_sort]].co - me.vertices[sort_list[sl + 1 + pa_sort]].co
    #             sum_length_b += subb.length
    #             list_length_b.append(sum_length_b)
    #
    #         list_koeff_a = []
    #         list_koeff_b = []
    #         for sl in range(len(list_length_a)):
    #             tmp = list_length_a[sl] / sum_length_a
    #             list_koeff_a.append(tmp)
    #         for sl in range(len(list_length_b)):
    #             tmp = list_length_b[sl] / sum_length_b
    #             list_koeff_b.append(tmp)
    #
    #         list_koeff_a = [0] + list_koeff_a
    #         list_koeff_b = [0] + list_koeff_b
    #
    #         if pa_sort == 0:
    #             kn1_i = sort_list[0]
    #             kn2_i = sort_list[pa_sort + 1]
    #         elif pa_sort == len(sort_list) - 1:
    #             kn1_i = sort_list[pa_sort - 1]
    #             kn2_i = sort_list[-1]
    #         else:
    #             kn1_i = sort_list[pa_sort - 1]
    #             kn2_i = sort_list[pa_sort + 1]
    #
    #         nkn1_ = me.vertices[kn1_i].co
    #         nkn2_ = me.vertices[kn2_i].co
    #
    #         p0_ = me.vertices[sort_list[0]].co
    #         p1_ = me.vertices[pa_idx].co
    #         p2_ = me.vertices[sort_list[-1]].co
    #
    #         kn1_ = nkn1_ - p1_ + nkn1_
    #         kn2_ = nkn2_ - p1_ + nkn2_
    #
    #         if mode[3]:
    #             la = len(list_koeff_a) - 1
    #             lb = len(list_koeff_b) - 1
    #             if la == 0:
    #                 da = 0
    #             else:
    #                 da = 1 / la
    #
    #             if lb == 0:
    #                 db = 0
    #             else:
    #                 db = 1 / lb
    #
    #             list_koeff_a = list(map(lambda n: da * n, list(range(0, la + 1))))
    #             list_koeff_b = list(map(lambda n: db * n, list(range(0, lb + 1))))
    #
    #         if mode[0]:
    #             p0 = p0_.x
    #             p1 = p1_.x - p0
    #             p2 = p2_.x - p0
    #             knot_1 = kn1_.x - p0
    #             knot_2 = kn2_.x - p0
    #             pA = nkn1_.x - p0
    #             pB = nkn2_.x - p0
    #             nkn1 = nkn1_.x - p0
    #             nkn2 = nkn2_.x - p0
    #
    #             if nkn1 == 0 or p1 == 0:
    #                 new_vts_a = []
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #             elif nkn2 == p2 or p1 == p2:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = []
    #             else:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts_a
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_a[i] = m * list_koeff_a[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #                     new_vts_ = new_vts_b
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_b[i] = m * list_koeff_b[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #             if new_vts_a:
    #                 for idx in range(pa_sort):
    #                     me.vertices[sort_list[idx]].co.x += (new_vts_a[idx] + p0 - me.vertices[
    #                         sort_list[idx]].co.x) * influe
    #             if new_vts_b:
    #                 for idx in range(cou_vs - pa_sort):
    #                     me.vertices[sort_list[idx + pa_sort + 1]].co.x += (new_vts_b[idx] + p0 - \
    #                                                                        me.vertices[
    #                                                                            sort_list[
    #                                                                                idx + pa_sort + 1]].co.x) * influe
    #
    #         if mode[1]:
    #             p0 = p0_.y
    #             p1 = p1_.y - p0
    #             p2 = p2_.y - p0
    #             knot_1 = kn1_.y - p0
    #             knot_2 = kn2_.y - p0
    #             pA = nkn1_.y - p0
    #             pB = nkn2_.y - p0
    #             nkn1 = nkn1_.y - p0
    #             nkn2 = nkn2_.y - p0
    #
    #             if nkn1 == 0 or p1 == 0:
    #                 new_vts_a = []
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #             elif nkn2 == p2 or p1 == p2:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = []
    #             else:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts_a
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_a[i] = m * list_koeff_a[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #                     new_vts_ = new_vts_b
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_b[i] = m * list_koeff_b[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #             if new_vts_a:
    #                 for idx in range(pa_sort):
    #                     me.vertices[sort_list[idx]].co.y += (new_vts_a[idx] + p0 - me.vertices[
    #                         sort_list[idx]].co.y) * influe
    #             if new_vts_b:
    #                 for idx in range(cou_vs - pa_sort):
    #                     me.vertices[sort_list[idx + pa_sort + 1]].co.y += (new_vts_b[idx] + p0 - \
    #                                                                        me.vertices[
    #                                                                            sort_list[
    #                                                                                idx + pa_sort + 1]].co.y) * influe
    #
    #         if mode[2]:
    #             p0 = p0_.z
    #             p1 = p1_.z - p0
    #             p2 = p2_.z - p0
    #             knot_1 = kn1_.z - p0
    #             knot_2 = kn2_.z - p0
    #             pA = nkn1_.z - p0
    #             pB = nkn2_.z - p0
    #             nkn1 = nkn1_.z - p0
    #             nkn2 = nkn2_.z - p0
    #
    #             if nkn1 == 0 or p1 == 0:
    #                 new_vts_a = []
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #             elif nkn2 == p2 or p1 == p2:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = []
    #             else:
    #                 new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                 new_vts_b = list(
    #                     map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2, list_koeff_b))
    #
    #             if mode[3]:
    #                 for c in range(steps_smoose):
    #                     new_vts_ = new_vts_a
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_a[i] = m * list_koeff_a[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #                     new_vts_ = new_vts_b
    #                     V = [vi for vi in new_vts_]
    #                     P = list(map(lambda x, y: abs(y - x), V[:-1], V[1:]))
    #                     L = sum(P)
    #                     lp = len(P)
    #                     if lp > 0:
    #                         d = L / lp
    #                         l_ = list(map(lambda y: d * y / L, list(range(1, lp + 1))))
    #                         l = list(map(lambda x: x / L, P))
    #
    #                         tmp = 1e-8
    #                         for i in range(lp):
    #                             tmp += l[i]
    #                             m = l_[i] / tmp
    #                             list_koeff_b[i] = m * list_koeff_b[i]
    #                         if nkn1 == 0 or p1 == 0:
    #                             new_vts_a = []
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #                         elif nkn2 == p2 or p1 == p2:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = []
    #                         else:
    #                             new_vts_a = list(map(lambda t: 2 * knot_1 * t * (1 - t) + pA * t ** 2, list_koeff_a))
    #                             new_vts_b = list(
    #                                 map(lambda t: pB * (1 - t) ** 2 + 2 * knot_2 * t * (1 - t) + p2 * t ** 2,
    #                                     list_koeff_b))
    #
    #             if new_vts_a:
    #                 for idx in range(pa_sort):
    #                     me.vertices[sort_list[idx]].co.z += (new_vts_a[idx] + p0 - me.vertices[
    #                         sort_list[idx]].co.z) * influe
    #             if new_vts_b:
    #                 for idx in range(cou_vs - pa_sort):
    #                     me.vertices[sort_list[idx + pa_sort + 1]].co.z += (new_vts_b[idx] + p0 - \
    #                                                                        me.vertices[
    #                                                                            sort_list[
    #                                                                                idx + pa_sort + 1]].co.z) * influe
    #
    #         me.update()
    #         bm.free()
    #
    #         bpy.ops.object.mode_set(mode='EDIT')
    #
    #     return True
    pass

def loopResolve(STEP, dist=None):
    def getTBSegment(segment, Pc, T, R, D):
        kk = (1 - T) * 0.5
        t = kk + T
        k_extr = 0
        b = Vector()
        for cycle in range(100):
            segment.calc(t, b)
            d_ = (b - Pc).length - R

            if abs(d_) <= D: return (t, b)

            if kk == k_extr:
                k = -0.5 if d_ > 0 else 0.5
            else:
                k = -1 if d_ > 0 else 1
                k_extr = kk

            kk *= k
            t += kk
            kk = abs(kk)
        return (t, b)

    edit_mode_out()
    edit_mode_in()

    obj = bpy.context.active_object
    me = obj.data

    verts = find_index_of_selected_vertex(me)

    segments_2d = find_all_segments(me, 3)
    if not segments_2d: return False
    # Запускаем 2д-перестроение по сплайну
    edit_mode_out()
    bm = bmesh.new()
    bm.from_mesh(me)
    check_lukap(bm)
    edit_mode_in()

    lv_for_del = []
    old_len_lfd = 0
    old_len_bmv = 0
    bm_verts = []
    remove_edges = []
    set_verts = set(verts)
    act_vert = bm_vert_active_get(bm)[0]
    for i, sort_list_ in enumerate(segments_2d):
        _is_loop = False
        if len(sort_list_) == 2:
            extreme_vs = sort_list_
        else:
            extreme_vs = find_extreme_select_verts(me, sort_list_)
            if not extreme_vs:
                _is_loop = True
                _loc_idx = sort_list_.index(act_vert)
                _sort_list_ = sort_list_[_loc_idx:] + sort_list_[:_loc_idx]
                sort_list_ = _sort_list_

                len_sort_list_ = len(sort_list_)
                _sub_segment_1 = sort_list_[:len_sort_list_ // 2 + 1]
                _sub_segment_2 = sort_list_[len_sort_list_ // 2:] + [sort_list_[0]]
                segments_2d[i] = _sub_segment_1
                segments_2d.insert(i + 1, _sub_segment_2)
                sort_list_ = _sub_segment_1
                if len(sort_list_) == 2:
                    extreme_vs = sort_list_
                else:
                    extreme_vs = find_extreme_select_verts(me, sort_list_)

        if _is_loop:
            sort_list = sort_list_
        else:
            bl_ = list(set(sort_list_) ^ set_verts)
            sort_list = find_all_connected_verts(me, extreme_vs[0], bl_)

        list_length = []
        sum_length = 0.0
        cou_vs = len(sort_list) - 1
        list_koeff = []
        if cou_vs == 1:
            p1co = me.vertices[sort_list[0]].co.copy()
            p3co = me.vertices[sort_list[1]].co.copy()
            p2co = (p1co + p3co) / 2
            sum_length = (p3co - p1co).length
            # list_length = [sum_length / 2, sum_length]
            list_koeff = [0.5, 0.5]
            values = [p1co, p2co, p3co]
        else:
            for sl in range(cou_vs):
                subb = me.vertices[sort_list[sl + 1]].co - me.vertices[sort_list[sl]].co
                sum_length += subb.length
                list_length.append(subb.length)

            for sl in range(cou_vs):
                tmp = list_length[sl] / sum_length
                list_koeff.append(tmp)

            values = [me.vertices[i].co.copy() for i in sort_list]

        n = len(values) - 1
        bezier = [Segment() for _ in range(n)]

        step_ = STEP - 1
        new_vts = []

        if not dist:
            r = sum_length / (step_)
        else:
            r = dist
            step_ = 1e+6

        pi_ = 0
        delta = 0.001
        for i in range(n):
            if i == n - 1: pi_ = 1

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
            Pc = segment.points[0].copy()
            t = 0
            i = 0
            ii = 0
            iii = 0
            pi_ = 0
            i_virtual = 0
            dr = 0
            old_point = me.vertices[extreme_vs[0]].co.copy()
            while i < len(bezier):
                ii += 1
                segment = bezier[i]
                if i == len(bezier) - 1: pi_ = 1

                if (Pc - segment.points[3 - pi_]).length < r:
                    t = 0 if i < len(bezier) - 2 else t
                    i += 1
                    if i_virtual < step_: i_virtual += 1
                    if i == len(bezier) and j == 3:
                        t, b = getTBSegment(segment, Pc, t, r, delta)
                        if len(new_vts) < step_: new_vts.append(b.copy())
                    continue

                t, b = getTBSegment(segment, Pc, t, r, delta)
                Pc = b
                if i_virtual < step_ + 1:
                    # Pc1 = Pc.copy()
                    i_virtual += 1

                if j == 3:
                    if len(new_vts) < step_: new_vts.append(b.copy())

                iii += 1
                dr += (old_point - Pc).length
                old_point = Pc.copy()

            r = dr / iii
            if dist:
                r = dist

        new_vts.insert(0, me.vertices[extreme_vs[0]].co)

        # В списке new_vts имеем координаты новых вершин
        edit_mode_out()
        lv_for_del.extend([bm.verts[vi] for vi in sort_list])
        for v in new_vts[1:-1]:
            new_v = bm.verts.new(v)
            new_v.select = True
            bm_verts.append(new_v)

        check_lukap(bm)

        v0_insert = lv_for_del.pop(old_len_lfd)
        v1_insert = lv_for_del.pop(-1)
        if len(sort_list) == 2:
            edge = bm.edges.get([v0_insert, v1_insert], False)
            if edge: remove_edges.append(edge)

        bm_verts.insert(old_len_bmv, v0_insert)
        bm_verts.append(v1_insert)
        bm_verts[old_len_bmv].select = True
        bm_verts[-1].select = True
        bm_edges = list(zip(bm_verts[old_len_bmv:-1], bm_verts[1 + old_len_bmv:]))
        old_len_lfd = len(lv_for_del)
        old_len_bmv = len(bm_verts)

        for edge in bm_edges:
            if not bm.edges.get(edge, False):
                ed_ = bm.edges.new(edge)
                ed_.select = True
            else:
                for i, re in enumerate(remove_edges):
                    if edge[0] in re.verts and edge[1] in re.verts:
                        remove_edges.pop(i)
                        break

    check_lukap(bm)
    for e in remove_edges:
        bm.edges.remove(e)

    for v in lv_for_del:
        if v in bm.verts:
            bm.verts.remove(v)

    check_lukap(bm)
    bm.to_mesh(me)
    bm.free()
    edit_mode_in()
    return True

def length_line(a, b):
    """Длина линии между двумя точками"""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def main_spline(verts, influe=1, relation=True):
    cou_vs = len(verts) - 1
    sort_list = verts
    if verts != None and cou_vs > 0:
        list_length = []
        sum_length = 0.0
        for sl in range(cou_vs):
            p2 = sort_list[sl + 1]
            p1 = sort_list[sl]
            sum_length += length_line(p2, p1)
            list_length.append(sum_length)

        list_koeff = []
        for sl in range(cou_vs):
            tmp = list_length[sl] / sum_length
            list_koeff.append(tmp)

        pa_idx = verts[0]
        if pa_idx == None:
            print('Active vert is not detected')
            print('Error: 030 simple_spline')
            return False

        pa_sort = sort_list.index(pa_idx)
        if pa_sort == 0:
            pa_sort = 1
        pa_perc = list_koeff[pa_sort - 1]
        p0_ = sort_list[0]
        p1_ = pa_idx
        p2_ = sort_list[-1]

        if relation:
            l = len(list_koeff)
            d = 1 / l
            list_koeff = list(map(lambda n: d * n, list(range(1, l + 1))))

        p0 = p0_.x
        p1 = p1_.x - p0
        p2 = p2_.x - p0

        if p1 == 0 or p1 == p2:
            new_vts = list(map(lambda t: p2 * t ** 2, list_koeff))
        else:
            b = (p1 - pa_perc ** 2 * p2) / (2 * pa_perc * (1 - pa_perc) + 1e-8)
            new_vts = list(map(lambda t: 2 * b * t * (1 - t) + p2 * t ** 2, list_koeff))

        for idx in range(cou_vs):
            sort_list[idx + 1].x += (new_vts[idx] + p0 - sort_list[idx + 1].x) * influe

        p0 = p0_.y
        p1 = p1_.y - p0
        p2 = p2_.y - p0

        b = (p1 - pa_perc ** 2 * p2) / (2 * pa_perc * (1 - pa_perc) + 1e-8)
        new_vts = list(map(lambda t: 2 * b * t * (1 - t) + p2 * t ** 2, list_koeff))

        for idx in range(cou_vs):
            sort_list[idx + 1].y += (new_vts[idx] + p0 - sort_list[idx + 1].y) * influe


def test_main_spline():
    verts = [
        [160, 249], [158, 325], [201, 396], [268, 470],
        [347, 467], [412, 425], [457, 369], [495, 284],
    ]
    print(*verts)

    points = []
    for vert in verts:
        points.append(sd.Point(vert[0], vert[1]))

    main_spline(points)
    print(*([p.x, p.y] for p in points))


if __name__ == '__main__':
    test_main_spline()
