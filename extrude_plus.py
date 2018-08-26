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

    def modal(self, context, event):
        # if event.type == 'MOUSEMOVE':
        bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
        v1 = bpy.context.scene.cursor_location.copy()
        v2 = self.mainPosition
        dist = (v1 - v2).length
        print(round(dist, 1))
        if round(dist, 1) >= 0.3:
            bpy.ops.mesh.dupli_extrude_cursor('INVOKE_DEFAULT', rotate_source=False)
            self.mainPosition = bpy.context.scene.cursor_location.copy()

        if event.type == 'RIGHTMOUSE':
            return {'FINISHED'}
        if event.type in {'ESC'}:
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            bpy.ops.view3d.snap_cursor_to_selected()
            self.mainPosition = bpy.context.scene.cursor_location.copy()
            view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.region_data, self.mainPosition, True)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "is't 3dview")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ExtrudBayDistance)


def unregister():
    bpy.utils.unregister_class(ExtrudBayDistance)


if __name__ == "__main__":
    register()
