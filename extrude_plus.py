import math
import bpy
from mathutils import Vector, Matrix

bl_info = {
    "name": "Extrud Bay Distance",
    "location": "View3D > Add > Mesh > Extrud Bay Distance",
    "description": "chet",
    "author": "Nedovizin Alexander, Vladislav Kindushov",
    "version": (0, 2),
    "blender": (2, 7, 9),
    "category": "Mesh",
}


class ExtrudBayDistance(bpy.types.Operator):
    """Border Occlusion selection """
    bl_idname = "view3d.extrud_bay_distance"
    bl_label = "Extrud Bay Distance"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        context.area.tag_redraw()
        bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
        if self.x != event.mouse_x or self.y != event.mouse_y or self.dist == 0:
            v1 = bpy.context.scene.cursor_location.copy()
            v2 = self.main_position
            self.x = event.mouse_x
            self.y = event.mouse_y
            dist = (v1 - v2).length
            if self.is_set_dist:
                self.dist = dist
                draw_radius(self)
            elif dist >= self.dist:
                bpy.ops.mesh.dupli_extrude_cursor('INVOKE_DEFAULT', rotate_source=False)
                self.main_position = bpy.context.scene.cursor_location.copy()

        if event.type == 'LEFTMOUSE' and self.is_set_dist:
            self.is_set_dist = False
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        elif event.type == 'RIGHTMOUSE':
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            except:
                pass
            return {'FINISHED'}
        elif event.type in {'ESC'}:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            except:
                pass
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        bpy.ops.view3d.snap_cursor_to_selected()
        self.main_position = bpy.context.scene.cursor_location.copy()
        self.is_set_dist = True
        self.dist = 0

        self.x = event.mouse_x
        self.y = event.mouse_y

        ars = (self,)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_radius, ars, 'WINDOW', 'POST_VIEW')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def draw_radius(self):
    number_sides = int(self.dist * 20) + 10
    angle_step = 2 * math.pi / number_sides
    data_verts = []

    vec_nativ = Vector((1, 0, 0))
    v1 = bpy.context.scene.cursor_location.copy()
    v2 = self.main_position
    vec_to = (v1 - v2).normalized()
    q_rot = vec_to.rotation_difference(vec_nativ).to_matrix().to_4x4()

    for ns in range(number_sides):
        angle = angle_step * ns
        co = Vector((math.sin(angle) * self.dist,
                     math.cos(angle) * self.dist,
                     0)) * q_rot
        co += self.main_position
        data_verts.append(co)
    data_verts.append(data_verts[0])

    draw_point_line_gl(Matrix(), data_verts)
    return True


def draw_point_line_gl(data_matrix, data_vector):
    from bgl import glVertex3f, glLineWidth, glBegin, glEnd, GL_POINTS, GL_LINES, \
        glDisable, GL_BLEND, glColor4f, GL_LINE_STRIP, GL_LINE_STIPPLE

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


def register():
    bpy.utils.register_class(ExtrudBayDistance)


def unregister():
    bpy.utils.unregister_class(ExtrudBayDistance)


if __name__ == "__main__":
    register()
