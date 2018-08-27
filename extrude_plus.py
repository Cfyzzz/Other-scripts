import math

import bpy
from mathutils import Vector, Matrix
from bpy_extras import view3d_utils

bl_info = {
    "name": "Extrud Bay Distance",
    "location": "View3D > Add > Mesh > Extrud Bay Distance",
    "description": "chet",
    "author": "Vladislav Kindushov",
    "version": (0, 1),
    "blender": (2, 7, 9),
    "category": "Mesh",
}


class ExtrudBayDistance(bpy.types.Operator):
    """Border Occlusion selection """
    bl_idname = "view3d.extrud_bay_distance"
    bl_label = "Extrud Bay Distance"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        draw_radius(self)
        # print("draw radius")
        return

    def modal(self, context, event):
        # if event.type in ('MOUSEX', 'MOUSEY'):
        #     context.active_object.location = self.main_position
        #     if self.is_set_dist:
        #         v1 = bpy.context.scene.cursor_location.copy()
        #         v2 = self.main_position
        #         self.dist = (v1 - v2).length
        #         draw_radius(self)
        #     else:
        #         # bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
        #         v1 = bpy.context.scene.cursor_location.copy()
        #         v2 = self.main_position
        #         dist = (v1 - v2).length
        #
        #         if round(dist, 1) >= 0.3:
        #             bpy.ops.mesh.dupli_extrude_cursor('INVOKE_DEFAULT', rotate_source=False)
        #             self.main_position = bpy.context.scene.cursor_location.copy()

        # if event.type == 'WHEELDOWNMOUSE':
        #     self.steps += 1
        #     self.execute(context)
        #     if not context.scene['cheredator']:
        #         self.steps -= 1
        # elif event.type == 'WHEELUPMOUSE':
        #     self.steps = max(self.steps - 1, 0)
        #     self.execute(context)
        if event.type == 'LEFTMOUSE' and self.is_set_dist:
            v1 = bpy.context.scene.cursor_location.copy()
            v2 = self.main_position
            self.dist = (v1 - v2).length
            self.is_set_dist = False
            self.execute(context)

        elif event.type == 'RIGHTMOUSE':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        elif event.type in {'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # bpy.ops.view3d.snap_cursor_to_selected()
        self.main_position = bpy.context.scene.cursor_location.copy()
        # view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.region_data, self.main_position, True)
        # context.window_manager.modal_handler_add(self)
        self.is_set_dist = True
        self.dist = 1

        ars = (self,)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_radius, ars, 'WINDOW', 'POST_VIEW')
        # self.execute(context)

        # self.set_dist()
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def draw_radius(self):
    obj = bpy.context.active_object
    number_sides = 10
    angle_step = 2 * math.pi / number_sides

    self.dist = 5
    data_verts = []
    for ns in range(number_sides):
        angle = angle_step * ns
        co = Vector((math.sin(angle) * self.dist,
                     math.cos(angle) * self.dist,
                    0))
        # co += self.main_position
        data_verts.append(co)

    draw_point_line_gl(obj.matrix_world, data_verts)
    return True




def draw_point_line_gl(data_matrix, data_vector):
    from bgl import glVertex3f, glPointSize, glLineStipple, \
        glLineWidth, glBegin, glEnd, GL_POINTS, GL_LINES, \
        glEnable, glDisable, GL_BLEND, glColor4f, GL_LINE_STRIP, GL_LINE_STIPPLE

    # draw_point_line_gl(obj.matrix_world, data_verts)

    glLineWidth(1.0)
    glEnable(GL_BLEND)
    # points
    glPointSize(6.0)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glBegin(GL_POINTS)
    for vert in data_vector:
        vec_corrected = data_matrix * vert
        glVertex3f(*vec_corrected)
    glEnd()

    # lines
    glLineWidth(3.0)
    glBegin(GL_LINE_STRIP)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    for i, vector in enumerate(data_vector):
        glVertex3f(*data_matrix * data_vector[i])
    glEnd()

    # restore opengl defaults
    glDisable(GL_BLEND)
    glLineWidth(1.0)
    glColor4f(0.0, 0.0, 0.0, 1.0)


# def cheredator_fantom(self):
#     step = self.steps
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bpy.ops.object.mode_set(mode='EDIT')
#
#     obj = bpy.context.active_object
#     me = obj.data
#
#     verts = find_index_of_selected_vertex(me)
#     active = None
#     if verts != None:
#         extreme_vs = find_extreme_select_verts(me, verts)
#         if extreme_vs == []:
#             bm = bmesh.new()
#             bm.from_mesh(me)
#             check_lukap(bm)
#             active = bm_vert_active_get(bm)[0]
#             extreme_vs = [active, active]
#             bm.free()
#         elif len(extreme_vs) != 2:
#             print_error2('Single Loop only', '01 cheredator_fantom')
#             return False
#         sort_list = find_all_connected_verts(me, extreme_vs[0], [])
#
#         if len(sort_list) != len(verts) and not active:
#             print_error2('Incoherent loop', '02 cheredator_fantom')
#             return False
#
#         if len(sort_list) < 3:
#             print_error2('Should be greater than two vertices', '03 cheredator_fantom')
#             return False
#
#         work_list = sort_list[1:-1]
#         if self.steps > len(work_list):
#             self.steps = len(work_list)
#
#         bpy.ops.mesh.select_mode(type='VERT')
#
#         most = False
#         data_verts = []
#         step_tmp = 0
#         for i in work_list:
#             step_tmp += 1
#             if step_tmp >= step:
#                 most = True
#                 step_tmp = 0
#             if most:
#                 data_verts.append(me.vertices[i].co)
#                 most = False
#
#         data_verts.insert(0, me.vertices[extreme_vs[0]].co)
#         data_verts.append(me.vertices[extreme_vs[1]].co)
#         draw_point_line_gl(obj.matrix_world, data_verts)
#     return True


def register():
    bpy.utils.register_class(ExtrudBayDistance)


def unregister():
    bpy.utils.unregister_class(ExtrudBayDistance)

if __name__ == "__main__":
    register()
