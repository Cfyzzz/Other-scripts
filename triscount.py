bl_info = {
    "name": "Triscount",
    "description": "Some scripts 3D realtime workflow oriented",
    "author": "Vincent (Vinc3r) Lamy, Nedovizin Alexander",
    "location": "3D view toolshelf - Addons tab",
    "category": "Mesh",
    'wiki_url': 'https://github.com/Vinc3r/BlenderScripts',
    'tracker_url': 'https://github.com/Vinc3r/BlenderScripts/issues',
}

import bpy, bmesh
from bpy.props import IntProperty, BoolProperty
from operator import itemgetter


def us(qty):
    """
    Convert qty to truncated string with unit suffixes.
    eg turn 12345678 into 12.3M
    """

    if qty < 1000:
        return str(qty)

    for suf in ['K', 'M', 'G', 'T', 'P', 'E']:
        qty /= 1000
        if qty < 1000:
            return "%3.1f%s" % (qty, suf)


class TrisCountUI(bpy.types.Panel):
    bl_label = "Triscount"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bpy.types.Scene.display_limit = IntProperty(name="Display limit",
                                description="Maximum number of items to list",
                                default=5, min=2, max=20)

    @classmethod
    def poll(cls, context):
        for region in context.area.regions:
            if region.type == "UI":
                return True
        else:
            return False

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        objs = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        row = layout.row()
        row.prop(scene, "display_limit")
        row = layout.row()
        if len(objs) == 1:
            row.label(text="1 Objects selected", icon='OBJECT_DATA')
        else:
            row.label(text=us(len(objs)) + " Objects selected", icon='OBJECT_DATA')

        if len(objs) > 0:
            dataCols = []
            row = layout.row()
            dataCols.append(row.column())  # name
            dataCols.append(row.column())  # Tris
            dataCols.append(row.column())  # mo.Tris

            total_tris = []
            bm = bmesh.new()
            for o in objs:
                bm.from_object(object=o,scene=scene,deform=True, render=True)
                tris = [(p.index) for p in o.data.polygons if len(p.vertices) == 3]
                mod_tris = [(p.index) for p in bm.faces if len(p.verts) == 3]
                total_tris.append((o.name, len(tris), len(mod_tris)))

            bm.free()
            tris_sorted = sorted(total_tris, key=itemgetter(1), reverse=True)[:scene.display_limit-1]

            headRow = dataCols[0].row()
            headRow.label(text="Name")
            headRow = dataCols[1].row()
            headRow.label(text="(Tris)")
            headRow = dataCols[2].row()
            headRow.label(text="(mod.)")

            sum_tris, sum_modtris = 0, 0
            for trises in tris_sorted:
                detailRow = dataCols[0].row()
                detailRow.label(text=trises[0])
                detailRow = dataCols[1].row()
                detailRow.label(text=us(trises[1]))
                detailRow = dataCols[2].row()
                detailRow.label(text="*" + us(trises[2]))

                sum_tris += trises[1]
                sum_modtris += trises[2]

            totRow = dataCols[0].row()
            totRow.label(text="Total:")
            totRow = dataCols[1].row()
            totRow.label(text=us(sum_tris))
            totRow = dataCols[2].row()
            totRow.label(text=us(sum_modtris))



def register():
    bpy.utils.register_class(TrisCountUI)


def unregister():
    bpy.utils.unregister_class(TrisCountUI)


if __name__ == "__main__":
    register()
