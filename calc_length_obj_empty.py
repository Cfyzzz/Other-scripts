# -*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####   

bl_info = {
    "name": "Calc Length Object",
    "author": "Nedpvizin Alexander",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Make path along curve",
    "warning": "",
    "wiki_url": "",
    "category": "Add Curve"} 


import bpy, math
from mathutils import Vector, Quaternion, Matrix
from bpy.props import BoolProperty, FloatProperty, IntProperty, EnumProperty, \
    StringProperty

def radius_falloff(points, power = 1.0, tip = 'NO'):
    total_points = len(points)
    for i, point in enumerate(points):
        dist = i/(total_points-1)
        if tip == 'ONE':
            radius_weight = 1.0 - pow(dist, power)
        elif tip == 'DUAL':
            if dist >= 0.5:
                dist = (dist - 0.5) * 2.0
                radius_weight = 1.0 - pow(dist, power)
            else:
                dist = dist * 2.0
                radius_weight = pow(dist, 1/power)
        elif tip == 'NO':
            radius_weight = 1.0
        #print(dist, radius_weight)
        point.radius = radius_weight


def get_spline_points(spline):
    # Points for griffindor
    if spline.type == 'POLY':
        points = spline.points
    else:
        points = spline.bezier_points

    return points


def check_bevel_used_by_other_objects(scene, curve_obj):
    bevel_used = False
    for o in scene.objects:
        if (o.type == 'CURVE' and
            o != curve_obj and
            o.data.bevel_object == curve_obj.data.bevel_object):
            bevel_used = True

    return bevel_used


def get_point_rotation(scene, curve_obj, index=0, spline_index=0):

    # Get curve attributes
    curve_mat = curve_obj.matrix_world
    curve = curve_obj.data
    points = get_spline_points(curve.splines[spline_index])

    # new temp object to detect local x-axis and y-axis of first handle
    # Temp Bevel Object for temp curve
    temp_bevel_curve = bpy.data.curves.new('__temp_bevel', 'CURVE')
    temp_spline = temp_bevel_curve.splines.new('POLY')
    temp_spline.points.add(2)
    temp_spline.points[0].co = Vector((1.0, 0.0, 0.0, 1.0))
    temp_spline.points[1].co = Vector((0.0, 1.0, 0.0, 1.0))
    temp_bevel_obj = bpy.data.objects.new('__temp_bevel', temp_bevel_curve)
    scene.objects.link(temp_bevel_obj)
    # Temp Curve
    curve_copy = curve_obj.data.copy()
    curve_copy.use_fill_caps = False
    curve_copy.bevel_object = temp_bevel_obj
    temp_obj = bpy.data.objects.new('__temp', curve_copy)
    scene.objects.link(temp_obj)
    temp_obj.location = curve_obj.location
    temp_obj.rotation_mode = curve_obj.rotation_mode
    temp_obj.rotation_quaternion = curve_obj.rotation_quaternion
    temp_obj.rotation_euler = curve_obj.rotation_euler

    # Convert temp curve to mesh
    bpy.ops.object.select_all(action='DESELECT') # deselect all first
    scene.objects.active = temp_obj
    temp_obj.select = True
    bpy.ops.object.convert(target='MESH')

    offset = 0
    micro_offset = 0

    #cyclic check
    for i, spline in enumerate(curve.splines):
        if i > spline_index:
            break
        #ps = get_spline_points(spline)
        if i > 0:
            ps_count = len(get_spline_points(curve.splines[i-1]))
            offset += ps_count-1
        if spline.use_cyclic_u:
            offset += 1
        elif i > 0:
            micro_offset += 1

    #offset += spline_index * curve.resolution_u
    #print(offset)

    # get x-axis and y-axis of the first handle
    handle_x = temp_obj.data.vertices[curve.resolution_u * (index + offset) * 3 + micro_offset * 3].co
    handle_y = temp_obj.data.vertices[curve.resolution_u * (index + offset) * 3 + 1 + micro_offset * 3].co

    target_x = handle_x - points[index].co.xyz
    target_y = handle_y - points[index].co.xyz
    target_x.normalize()
    target_y.normalize()

    # delete temp objects
    temp_bevel_obj.select = True
    bpy.ops.object.delete()
    
    # Match bevel x-axis to handle x-axis
    bevel_x = Vector((1.0, 0.0, 0.0))
    target_x = curve_mat.to_3x3() * target_x
    rot_1 = bevel_x.rotation_difference(target_x)

    # Match bevel y-axis to handle y-axis
    bevel_y = rot_1.to_matrix() * Vector((0.0, 1.0, 0.0))
    target_y = curve_mat.to_3x3() * target_y
    rot_2 = bevel_y.rotation_difference(target_y)

    # Select curve object again
    scene.objects.active = curve_obj
    curve_obj.select = True

    return rot_2 * rot_1


def get_point_position(curve_obj, index=0, spline_index=0):
    curve_mat = curve_obj.matrix_world
    curve = curve_obj.data
    points = get_spline_points(curve.splines[spline_index])
    return curve_mat * points[index].co.xyz


def get_proper_index_bevel_placement(curve_obj):
    """ Returns (spline index, point index) """
    idx = (0, 0)
    found = False

    for i, spline in enumerate(curve_obj.data.splines):
        points = get_spline_points(spline)
        # Prioritising radius of 1.0
        for j, point in enumerate(points):
            if point.radius == 1.0:
                idx = (i, j)
                found = True
                break
        if found:
            break

    # If still not found do another loop
    if not found:
        for i, spline in enumerate(curve_obj.data.splines):
            points = get_spline_points(spline)
            for j, point in enumerate(points):
                if point.radius <= 1.0 and point.radius >= 0.3:
                    temp_ps = get_spline_points(curve_obj.data.splines[idx[0]])
                    old_radius = temp_ps[idx[1]].radius
                    # get the biggest radius under 1.0
                    if point.radius > old_radius or old_radius > 1.0:
                        idx = (i, j)
    
    #print(idx)
    return idx



class KG_Panel(bpy.types.Panel):
    """Calc Length Object Panel"""
    bl_label = "Calc Length Object"
    bl_idname = "SCENE_PT_CLO"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None  

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lt = bpy.context.window_manager.gk_manager 
        
        c2 = layout.column(align=True)
        if context.mode == 'OBJECT':
            if lt.display_position:  
                c2.prop(lt, "display_position", text="Позиционирование", icon='DOWNARROW_HLT')
            else:
                c2.prop(lt, "display_position", text="Позиционирование", icon='RIGHTARROW')  
            if lt.display_position:  
                box = c2.row().box()
                #row = box.row()  
                #row.label('Позиционирование:')
                row = box.row(align=True)  
                row.operator('gk.behind_obj',text='Фон')
                row.operator('gk.before_obj',text='Изображение')
            
            c3 = c2.column()
            if lt.display_prof:  
                c3.prop(lt, "display_prof", text="Профиль", icon='DOWNARROW_HLT')
            else:
                c3.prop(lt, "display_prof", text="Профиль", icon='RIGHTARROW')  
            if lt.display_prof:  
                box = c2.row().box()
                col_top = box.column(align=True)
                #row = col_top.row(align=True)
                #row.label("Профиль:")
                row = col_top.row(align=True)
                row.prop(lt,'prof_width',text='Ширина')
                row = col_top.row(align=True)
                row.prop(lt,'prof_length',text='Длина')
                c = col_top.column()
                c.separator()
                c = col_top.column()
                c.prop(lt,'shape',text='Форма')
                c.separator()
                c = col_top.column()
                c.operator("gkcurve.new_beveled_curve", text='Новая кривая')
                box1 = c.box()
                c1 = box1.column()
                c1.label(text="Редактировать профиль:")
                c1.operator("gkcurve.add_bevel_to_curve", text='Заменить')
                c1.operator("gkcurve.edit_bevel_curve", text='Редкатировать')
                c1.operator("gkcurve.hide_bevel_objects", text='Скрыть')
                c1.prop(lt,'prof_bevel', text='Фаска')
        elif context.mode =='EDIT_CURVE':
            c2.operator("gkcurve.finish_edit_bevel")
        
        #mat = context.active_object.active_material 
        #c2.template_preview(mat, show_buttons=False, preview_id="gk.bigpreview")
        
        c3 = c2.column()
        if lt.display_primitives:  
            c3.prop(lt, "display_primitives", text="Примитивы", icon='DOWNARROW_HLT')
        else:
            c3.prop(lt, "display_primitives", text="Примитивы", icon='RIGHTARROW')  
        if lt.display_primitives:  
            box = c2.row().box()
            col = box.column(align=True)
            #row = col_top.row(align=True)
            #row.label("Профиль:")
            #col = col_top.column(align=True)
            col.operator('mesh.primitive_cube_add',text='Куб', icon='MESH_CUBE')
            col.operator('mesh.primitive_uv_sphere_add',text='Сфера', icon='MESH_UVSPHERE')
            col.operator('mesh.primitive_cylinder_add',text='Цилиндр', icon='MESH_CYLINDER')
            col.operator('mesh.primitive_cone_add',text='Конус', icon='MESH_CONE')
            col.operator('mesh.primitive_torus_add',text='Тор', icon='MESH_TORUS')
        
        c3 = c2.column()
        if lt.display_views:  
            c3.prop(lt, "display_views", text="Настройка вида", icon='DOWNARROW_HLT')
        else:
            c3.prop(lt, "display_views", text="Настройка вида", icon='RIGHTARROW')  
        if lt.display_views:  
            box = c2.row().box()
            col_top = box.column(align=True)
            col3 = col_top.column_flow(columns=3)   
            col_fb = col3.column()
            col_lr = col3.column()
            col_tb = col3.column()
            self.addSetter([['view3d.viewnumpad','спереди','FRONT'], \
                ['view3d.viewnumpad','сзади','BACK']],col_fb,'')
            self.addSetter([['view3d.viewnumpad','слева','LEFT'], \
                ['view3d.viewnumpad','справа','RIGHT']],col_lr,'')
            self.addSetter([['view3d.viewnumpad','сверху','TOP'], \
                ['view3d.viewnumpad','снизу','BOTTOM']],col_tb,'')
            
            col_top.operator('gk.cursor2center')
            
        c3 = c2.column()
        if lt.display_drawing:  
            c3.prop(lt, "display_drawing", text="Чертёж", icon='DOWNARROW_HLT')
        else:
            c3.prop(lt, "display_drawing", text="Чертёж", icon='RIGHTARROW')  
        if lt.display_drawing:  
            box = c2.row().box()
            col_top = box.column(align=True)
            row = col_top.row()
            row.alignment='CENTER'
            row.label("Сгенерировать чертёж")
            col3 = col_top.column_flow(columns=3)   
            col_fb = col3.column()
            col_lr = col3.column()
            col_tb = col3.column()
            self.addSetter([['gk.cam2view','спереди','FRONT'], \
                ['gk.cam2view','сзади','BACK']],col_fb,'')
            self.addSetter([['gk.cam2view','слева','LEFT'], \
                ['gk.cam2view','справа','RIGHT']],col_lr,'')
            self.addSetter([['gk.cam2view','сверху','TOP'], \
                ['gk.cam2view','снизу','BOTTOM']],col_tb,'')
            
            col_top.operator('gk.cam2view',text="Произвольный вид").type='USER'
            
        c3 = c2.column()
        if lt.display_cam:  
            c3.prop(lt, "display_cam", text="Настройка камеры", icon='DOWNARROW_HLT')
        else:
            c3.prop(lt, "display_cam", text="Настройка камеры", icon='RIGHTARROW')  
        if lt.display_cam:  
            box = c2.row().box()
            col_top = box.column(align=True)
            col_top.operator('gk.cam2front')
            row = col_top.row(align=True)
            row.operator('gk.camortho')
            row.operator('gk.campersp')
            col_top = box.column(align=True)
            col_top.operator('gk.cam2front',text='Ready to print')
            col_top.operator('gk.cam2front',text='Render')
            
            
            
        
    def addSetter(self, control, col_layer, label):
        if label:
            row_layer = col_layer.row()
            row_layer.alignment='CENTER'
            row_layer.label(label)
        row_layer = col_layer.row()
        for c in control:
            # c[0] - operator; c[1] - text; c[2] - type (options)
            row_layer = row_layer.column(align=True)
            op = row_layer.operator(c[0],text=c[1])
            if c[2]: op.type=c[2]
            



class GK_OT_CameraPersp(bpy.types.Operator):
    """Установить камеру в перспективу"""
    bl_idname = "gk.campersp"
    bl_label = "Перспектива"
    bl_description = "Установить камеру в перспективу"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        cam_ob = bpy.context.scene.camera
        cam_ob.data.type='PERSP'
        return{'FINISHED'}  
        
        
class GK_OT_CameraOrtho(bpy.types.Operator):
    """Установить камеру в ортогональную проекцию"""
    bl_idname = "gk.camortho"
    bl_label = "Орто"
    bl_description = "Установить камеру в ортогональную проекцию"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        cam_ob = bpy.context.scene.camera
        cam_ob.data.type='ORTHO'
        return{'FINISHED'}           


class GK_OT_CameraToView(bpy.types.Operator):
    """Установить камеру в вид"""
    bl_idname = "gk.cam2view"
    bl_label = "Установка камеры"
    bl_description = "Установить камеру в вид"
    bl_options = {'REGISTER', 'UNDO'}
    
    type = StringProperty(name="type", default="FRONT")
    
    def execute(self, context):    
        bpy.ops.view3d.viewnumpad(type=self.type)    
        bpy.ops.view3d.camera_to_view()
        cam_ob = bpy.context.scene.camera
        cam_ob.data.type='ORTHO'
        mat_rot = Matrix.Rotation(math.pi/2, 4, 'X')
        cam_ob.matrix_world = Matrix()*mat_rot
        cam_ob.location = Vector((0,0,0))
        bpy.ops.view3d.camera_to_view_selected()
        cam_ob.location += Vector((0,-5,0))
        cam_ob.data.ortho_scale *= 1.2
        return{'FINISHED'}  


class GK_OT_CameraToFront(bpy.types.Operator):
    """Установить камеру в теекущий вид"""
    bl_idname = "gk.cam2front"
    bl_label = "Установка камеры"
    bl_description = "Установить камеру в текущий вид"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        bpy.ops.view3d.viewnumpad(type='FRONT')    
        bpy.ops.view3d.camera_to_view()
        cam_ob = bpy.context.scene.camera
        cam_ob.data.type='ORTHO'
        mat_rot = Matrix.Rotation(math.pi/2, 4, 'X')
        cam_ob.matrix_world = Matrix()*mat_rot
        cam_ob.location = Vector((0,0,0))
        bpy.ops.view3d.camera_to_view_selected()
        cam_ob.location += Vector((0,-5,0))
        cam_ob.data.ortho_scale *= 1.2
        return{'FINISHED'}         
        
        
class GK_OT_CursorToCenter(bpy.types.Operator):
    """Установить 3D-Курсор в центр"""
    bl_idname = "gk.cursor2center"
    bl_label = "3D-Курсор в центр"
    bl_description = "Установить 3D-Курсор в центр"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        
        bpy.context.scene.cursor_location = Vector((0,0,0))
        return{'FINISHED'} 
        

class GK_HideBevelObjects(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "gkcurve.hide_bevel_objects"
    bl_label = "Hide Bevel Objects"
    bl_description = "Скрыть отредактированный профиль"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):

        scn = context.scene

        bevel_objs = list()

        for obj in scn.objects:
            if obj.type == 'CURVE' and obj.data.bevel_object and obj.data.bevel_object not in bevel_objs:
                bevel_objs.append(obj.data.bevel_object)
            if '_bevel' in obj.name and  obj not in bevel_objs:
                bevel_objs.append(obj)
        
        for obj in bevel_objs:
            # Change object's layer to only layer 19
            obj.layers[19] = True
            for i in range(19):
                obj.layers[i] = False
            # Hide objects
            #obj.hide = True
        
        return {'FINISHED'}

class GK_EditBevelCurve(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "gkcurve.edit_bevel_curve"
    bl_label = "Edit Bevel"
    bl_description = "Редактировать профиль кривой"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # check if curve is selected
        obj = context.active_object
        return context.mode == 'OBJECT' and obj and obj.type == 'CURVE' and obj.data.bevel_object

    def execute(self, context):

        scn = context.scene
        obj = context.active_object
        curve = obj.data
        bevel_obj = curve.bevel_object

        # hide all bevel objects around first
        bpy.ops.gkcurve.hide_bevel_objects()

        # duplicate bevel object if it's used by other object
        bevel_used = check_bevel_used_by_other_objects(scn, obj)
        if bevel_used:
            bevel_obj = bpy.data.objects.new(obj.name + '_bevel', bevel_obj.data.copy())
            scn.objects.link(bevel_obj)
            curve.bevel_object = bevel_obj

        idx = get_proper_index_bevel_placement(obj)
        bevel_rotation = get_point_rotation(scn, obj, index=idx[1], spline_index=idx[0])
        bevel_position = get_point_position(obj, index=idx[1], spline_index=idx[0])

        # Set object rotation and location
        bevel_obj.rotation_mode = 'QUATERNION'
        bevel_obj.rotation_quaternion = bevel_rotation
        bevel_obj.location = bevel_position

        # Show bevel object on active layer
        for i in range(20):
            bevel_obj.layers[i] = scn.layers[i]

        # Show object if hidden
        bevel_obj.hide = False

        bpy.ops.object.select_all(action='DESELECT')
        scn.objects.active = bevel_obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class GK_AddBevelToCurve(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "gkcurve.add_bevel_to_curve"
    bl_label = "Add/Override Bevel"
    bl_description = "Добавить или заменить профиль кривой"
    bl_options = {'REGISTER', 'UNDO'}

    shape = EnumProperty(
            name = "Shape",
            description="Use predefined shape of bevel", 
            items=(
                ('SQUARE', "Square", ""),
                ('HALFCIRCLE', "Half-Circle", ""),
                ('CIRCLE', "Circle", ""),
                ('TRIANGLE', "Triangle", ""),
                ), 
            default='TRIANGLE',
            )

    subsurf = BoolProperty(
            name="Use SubSurf Modifier",
            default=False,
            )

    scale_x = FloatProperty(
            name="Scale X (Bevel Object)",
            description="X scaling",
            min=0.1, max=10.0,
            default=1.0,
            step=0.3,
            precision=3
            )

    scale_y = FloatProperty(
            name="Scale Y (Bevel Object)",
            description="Y scaling",
            min=0.1, max=10.0,
            default=1.0,
            step=0.3,
            precision=3
            )

    rotation = FloatProperty(
            name="Rotate",
            description="Tilt rotation",
            unit='ROTATION',
            min=0.0, max=math.pi*2.0,
            default=0.0,
            )

    falloff = EnumProperty(
            name = "Radius Falloff",
            description="Falloff of beveled curve", 
            items=(
                ('DUALTIP', "Dual Tip", ""),
                ('ONETIP', "One Tip", ""),
                ('NOTIP', "No Tip", ""),
                ), 
            default='NOTIP',
            )

    #falloff_power = FloatProperty(
    #        name="Falloff Power",
    #        description="Power of the falloff",
    #        min=1.0, max=10.0,
    #        default=1.0,
    #        step=1.0,
    #        precision=2
    #        )

    #resolution = IntProperty(
    #        name="Resolution U",
    #        description="Resolution between points",
    #        min=1, max=64,
    #        default=12,
    #        step=1,
    #        )

    @classmethod
    def poll(cls, context):
        if not context.mode == 'OBJECT':
            return False
        # check if curve is selected
        obj = context.active_object
        scn = context.scene
        if obj and obj.type == 'CURVE':
            # Bevel object cannot use bevel too
            bevel_match = any(o for o in scn.objects if o.type == 'CURVE' and o.data.bevel_object == obj)
            if bevel_match:
                return False
            else:
                return True
        return False

    def execute(self, context):
        config = bpy.context.window_manager.gk_manager
        curve_obj = context.active_object
        scn = context.scene
        curve = curve_obj.data

        # Set resolution
        #curve.resolution_u = self.resolution
        #curve.render_resolution_u = self.resolution

        # First spline
        splines = curve_obj.data.splines
        points = get_spline_points(splines[0])

        if len(points) < 2:
            self.report({'ERROR'}, "Just one point wouldn't do it")
            return {'CANCELLED'}  
        
        if len(points) == 2 and self.falloff == 'DUALTIP':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.subdivide() #number_cuts=3)
            bpy.ops.object.editmode_toggle()
            # spline data changes, so it must be retreived again
            splines = curve_obj.data.splines
            points = get_spline_points(splines[0])

        # Spline setup
        for spline in splines:
            # Cardinal is better
            spline.tilt_interpolation = 'CARDINAL'
            spline.radius_interpolation = 'CARDINAL'

            ps = get_spline_points(spline)

            # Set tilt rotation
            for p in ps:
                p.tilt = self.rotation

            if self.falloff == 'ONETIP':
                radius_falloff(ps, tip='ONE')

            elif self.falloff == 'DUALTIP':
                radius_falloff(ps, tip='DUAL')

            elif self.falloff == 'NOTIP':
                radius_falloff(ps, tip='NO')


        # delete old bevel object if it's already there
        if curve.bevel_object:

            # Check if other object using this bevel object
            bevel_used = check_bevel_used_by_other_objects(scn, curve_obj)
            
            if not bevel_used:
                #delete old bevel object
                bevel_obj = curve.bevel_object
                bpy.ops.object.select_all(action='DESELECT')
                bevel_obj.select = True
                scn.objects.active = bevel_obj
                bpy.ops.object.delete()

                # Reselect curve_obj
                curve_obj.select = True
                scn.objects.active = curve_obj

        # point coords
        triangle_coords = [
                (-0.055, 0.0), (-0.06, 0.01),
                (-0.005, 0.1), (0.005, 0.1),
                (0.06, 0.01), (0.055, 0.0)]

        halfcircle_coords = [
                (-0.06, 0.0), (-0.06, 0.01),
                (-0.045, 0.07), (0.0, 0.1), (0.045, 0.07),
                (0.06, 0.01), (0.06, 0.0)]

        circle_coords = [
                (-0.036, 0.014), (-0.05, 0.05),
                (-0.036, 0.086), (0.0, 0.1), (0.036, 0.086),
                (0.05, 0.05), (0.036, 0.014)]

        square_coords = [
                (0.0, 0.04), (0.01, 0.05), 
                (0.09, 0.05), (0.1, 0.04), 
                (0.1, 0.0),
                (0.1, -0.04), (0.09, -0.05), 
                (0.01, -0.05), (0.0, -0.04)]

        if config.shape == 'TRIANGLE':
            coords = triangle_coords
        elif config.shape == 'HALFCIRCLE':
            coords = halfcircle_coords
        elif config.shape == 'CIRCLE':
            coords = circle_coords
        elif config.shape == 'SQUARE':
            coords = square_coords

        # new object and curve data
        bevel_curve = bpy.data.curves.new(curve_obj.name + '_bevel', 'CURVE')
        bevel_curve.dimensions = '3D'
        bevel_curve.resolution_u = 2
        bevel_curve.show_normal_face = False

        # add new spline and set it's points to bevel curve
        new_spline = bevel_curve.splines.new('POLY')
        new_spline.use_cyclic_u = True
        new_spline.points.add(len(coords))
        for i, co in enumerate(coords):
            new_spline.points[i].co = Vector((co[0], co[1], 0.0, 1.0))

        # Create new bevel object
        bevel_obj = bpy.data.objects.new(curve_obj.name + '_bevel', bevel_curve)
        scn.objects.link(bevel_obj)

        # add bevel to curve
        curve.bevel_object = bevel_obj
        curve.use_fill_caps = True
        
        # Scale the points
        #for spline in bevel_curve.splines:
        ps = get_spline_points(bevel_curve.splines[0])
        sum_x = 0.0
        sum_y = 0.0
        for p in ps:
            sum_x += p.co.x
            sum_y += p.co.y

        offset_x = sum_x / len(ps)
        offset_y = sum_y / len(ps)

        for p in ps:
            # offset to center the origins 
            p.co.x -= offset_x
            p.co.y -= offset_y

            # then scale
            p.co.x *= self.scale_x
            p.co.y *= self.scale_y
            
        if self.falloff == 'DUALTIP':
            midindex = int((len(points)-1)/2)
            bevel_rotation = get_point_rotation(scn, curve_obj, index=midindex)
            bevel_position = get_point_position(curve_obj, index=midindex)
        else: 
            bevel_rotation = get_point_rotation(scn, curve_obj)
            bevel_position = get_point_position(curve_obj)

        # Set object rotation and location
        bevel_obj.rotation_mode = 'QUATERNION'
        bevel_obj.rotation_quaternion = bevel_rotation
        bevel_obj.location = bevel_position

        # Send bevel object to layer 20
        bevel_obj.layers[19] = True
        for i in range(19):
            bevel_obj.layers[i] = False
        #bevel_obj.hide = True

        # Add/remove subsurf
        subsurf_found = False
        modifiers = curve_obj.modifiers
        for m in modifiers:
            if m.type == 'SUBSURF':
                subsurf_found = True
        
        if self.subsurf == False:
            if subsurf_found == True:
                for m in modifiers:
                    if m.type == 'SUBSURF':
                        bpy.ops.object.modifier_remove(modifier=m.name)

        if self.subsurf == True:
            if subsurf_found == False:
                bpy.ops.object.modifier_add(type='SUBSURF')

        return {'FINISHED'}
        
        
class GK_FinishEditBevel(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "gkcurve.finish_edit_bevel"
    bl_label = "Finish Edit Bevel"
    bl_description = "Finish edit bevel and back to object mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_CURVE' and not context.object.data.bevel_object

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        
        bevel_obj = context.active_object
        
        # Bring back bevel object to layer 19
        #bpy.ops.curve.hide_bevel_objects()
        bevel_obj.layers[19] = True
        for i in range(19):
            bevel_obj.layers[i] = False

        # Select curve object back
        for obj in context.scene.objects:
            if obj.type == 'CURVE' and obj.data.bevel_object and obj.data.bevel_object == bevel_obj:
                obj.select = True
                context.scene.objects.active = obj
        return {'FINISHED'}

class GK_NewBeveledCurve(bpy.types.Operator):
    """Nice Useful Tooltip"""
    bl_idname = "gkcurve.new_beveled_curve"
    bl_label = "New Beveled Curve"
    bl_description = "Создать новую кривую с профилем"
    bl_options = {'REGISTER', 'UNDO'}

    shape = EnumProperty(
            name = "Shape",
            description="Use predefined shape of bevel", 
            items=(
                ('SQUARE', "Square", ""),
                ('HALFCIRCLE', "Half-Circle", ""),
                ('CIRCLE', "Circle", ""),
                ('TRIANGLE', "Triangle", ""),
                ), 
            default='TRIANGLE',
            )

    subsurf = BoolProperty(
            name="Use SubSurf Modifier",
            default=False,
            )

    radius = FloatProperty(
            name="Size (Curve)",
            description="Size of the curve",
            min=0.1, max=10.0,
            default=1.0,
            step=0.3,
            precision=3
            )

    scale_x = FloatProperty(
            name="Scale X (Bevel Object)",
            description="X scaling",
            min=0.1, max=10.0,
            default=1.0,
            step=0.3,
            precision=3
            )

    scale_y = FloatProperty(
            name="Scale Y (Bevel Object)",
            description="Y scaling",
            min=0.1, max=10.0,
            default=1.0,
            step=0.3,
            precision=3
            )

    rotation = FloatProperty(
            name="Rotate",
            description="Tilt rotation",
            unit='ROTATION',
            min=0.0, max=math.pi*2.0,
            default=0.0,
            )

    falloff = EnumProperty(
            name = "Radius Falloff",
            description="Falloff of beveled curve", 
            items=(
                ('DUALTIP', "Dual Tip", ""),
                ('ONETIP', "One Tip", ""),
                ('NOTIP', "No Tip", ""),
                ), 
            default='NOTIP',
            )

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        config = bpy.context.window_manager.gk_manager
        bpy.ops.curve.primitive_bezier_curve_add(radius = self.radius)
        bpy.ops.gkcurve.add_bevel_to_curve(
            scale_x = self.scale_x,
            scale_y = self.scale_y,
            rotation = self.rotation,
            shape = config.shape,
            falloff = self.falloff,
            subsurf = self.subsurf)
        return {'FINISHED'}       
        


class GK_managerProps(bpy.types.PropertyGroup):   
    """
    Fake module like class
    bpy.context.window_manager.gk_manager
    """
    prof_width = FloatProperty(name="width", default=0.0, min=0)
    prof_length = FloatProperty(name="length", default=0.0, min=0)
    prof_coners = IntProperty(name="coners", default=4, min=3)
    prof_bevel = FloatProperty(name="bevel", default=0.0, min=0.0, precision=3, step=0.5)
    display_position = BoolProperty(name="display_position")
    display_prof = BoolProperty(name="display_prof")
    display_primitives = BoolProperty(name="display_primitives")
    display_views = BoolProperty(name="display_views")
    display_cam = BoolProperty(name="display_cam")
    display_drawing = BoolProperty(name="display_drawing")
    
    shape = EnumProperty(
            name = "Форма профиля",
            description="Предустановленный профиль", 
            items=(
                ('SQUARE', "Квадрат", ""),
                ('HALFCIRCLE', "Полукруг", ""),
                ('CIRCLE', "Круг", ""),
                ('TRIANGLE', "Треугольник", ""),
                ), 
            default='TRIANGLE',
            )
    


class GK_OT_BehindObj(bpy.types.Operator):
    """ Поместить за объект """

    bl_idname = "gk.behind_obj"
    bl_label = "Behind object"

    def execute(self, context):
        

        return{'FINISHED'} 


class GK_OT_BeforeObj(bpy.types.Operator):
    """ Поместить перед объектом """

    bl_idname = "gk.before_obj"
    bl_label = "Before object"

    def execute(self, context):
        

        return{'FINISHED'} 












# define classes for registration
classes = [KG_Panel, GK_OT_BehindObj, GK_OT_BeforeObj, GK_managerProps, \
GK_HideBevelObjects, GK_EditBevelCurve, GK_AddBevelToCurve, GK_FinishEditBevel, \
GK_NewBeveledCurve, GK_OT_CursorToCenter, GK_OT_CameraToFront, GK_OT_CameraOrtho, \
GK_OT_CameraPersp, GK_OT_CameraToView]


# registering and menu integration
def register():
    for c in classes:
        bpy.utils.register_class(c)    
    bpy.types.WindowManager.gk_manager = \
        bpy.props.PointerProperty(type = GK_managerProps) 
        
# unregistering and removing menus  
def unregister():    
    del bpy.types.WindowManager.gk_manager 
    for c in reversed(classes):  
        bpy.utils.unregister_class(c) 

if __name__ == "__main__":
    register() 
