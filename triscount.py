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
    bpy.types.Scene.triscount_render = BoolProperty(name="Count Render",
                                                    description="Tris count render or preview",
                                                    default = False)

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
        row.prop(scene, "triscount_render")
        row = layout.row()
        if len(objs) == 1:
            row.label(text="1 Objects selected", icon='OBJECT_DATA')
        else:
            row.label(text=us(len(objs)) + " Objects selected", icon='OBJECT_DATA')

        if len(objs) > 0:
            dataCols = []
            row = layout.row()
            dataCols.append(row.column(align=True))  # name
            dataCols.append(row.column(align=True))  # Tris
            dataCols.append(row.column(align=True))  # mo.Tris

            total_tris = []
            sum_tris, sum_modtris = 0, 0
            for o in objs:
                bm = bmesh.new()
                bm.from_object(object=o, scene=scene, deform=True, render=scene.triscount_render)
                tris = 0
                for p in o.data.polygons:
                    tris += len(p.vertices) - 2

                mod_tris = 0
                for p in bm.faces:
                    mod_tris += len(p.verts) - 2

                total_tris.append((o.name, tris, mod_tris))
                sum_tris += tris
                sum_modtris += mod_tris

                bm.free()

            tris_sorted = sorted(total_tris, key=itemgetter(1), reverse=True)[:scene.display_limit]

            headRow = dataCols[0].row()
            headRow.label(text="Name")
            headRow = dataCols[1].row()
            headRow.label(text="(Tris)")
            headRow = dataCols[2].row()
            headRow.label(text="(mod.)")

            for trises in tris_sorted:
                detailRow = dataCols[0].row()
                detailRow.label(text=trises[0])
                detailRow = dataCols[1].row()
                detailRow.label(text=us(trises[1]))
                detailRow = dataCols[2].row()
                detailRow.label(text="*" + us(trises[2]))

            totRow = dataCols[0].row()
            box = totRow.box().row()
            box.label(text="Total:")
            totRow = dataCols[1].row()
            box = totRow.box().row()
            box.label(text=us(sum_tris))
            totRow = dataCols[2].row()
            box = totRow.box().row()
            box.label(text=us(sum_modtris))


def register():
    bpy.utils.register_class(TrisCountUI)


def unregister():
    bpy.utils.unregister_class(TrisCountUI)


if __name__ == "__main__":
    register()
