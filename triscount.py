bl_info = {
    "name": "Triscount",
    "description": "Some scripts 3D realtime workflow oriented",
    "author": "Vincent (Vinc3r) Lamy",
    "location": "3D view toolshelf - Addons tab",
    "category": "Mesh",
    'wiki_url': 'https://github.com/Vinc3r/BlenderScripts',
    'tracker_url': 'https://github.com/Vinc3r/BlenderScripts/issues',
}

import bpy
import bmesh
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

    calculate_modifier_verts = True
    display_limit = IntProperty(name="Display limit",
                                description="Maximum number of items to list",
                                default=5, min=2, max=20)

    def draw(self, context):
        layout = self.layout

        calculate_modifier_verts = True

        meshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        row = layout.row()
        if len(meshes) == 1:
            row.label(text="1 Objects selected", icon='OBJECT_DATA')
        else:
            row.label(text=us(len(meshes)) + " Objects selected", icon='OBJECT_DATA')
            # row = layout.row()
            # if len(meshes) > 10:
            #    row.label(text="Top %d mesh objects." % 10)
            # else:
            #    row.label(text="Top %d mesh objects." % len(meshes))

        totalTriInSelection = 0
        # row = layout.row()
        if len(meshes) > 0:
            dataCols = []
            row = layout.row()
            dataCols.append(row.column())  # name
            dataCols.append(row.column())  # verts
            dataCols.append(row.column())  # verts after modifiers
            dataCols.append(row.column())  # Tris

            topMeshes = [(o, o.name, len(o.data.vertices), len(o.data.edges), len(o.data.polygons)) for o in meshes]
            topMeshes = sorted(topMeshes, key=itemgetter(2), reverse=True)[:12]

            headRow = dataCols[0].row()
            headRow.label(text="Name")
            headRow = dataCols[1].row()
            headRow.label(text="Verts")
            headRow = dataCols[2].row()
            headRow.label(text="(mod.)")
            headRow = dataCols[3].row()
            headRow.label(text="(Tris)")

            for mo in topMeshes:
                detailRow = dataCols[0].row()
                detailRow.label(text=mo[1])
                detailRow = dataCols[1].row()
                detailRow.label(text=us(mo[2]))
                if calculate_modifier_verts == True:
                    detailRow = dataCols[2].row()
                    bm = bmesh.new()
                    bm.from_object(mo[0], context.scene)
                    detailRow.label(text="*" + us(len(bm.verts)))
                    bm.free()
                else:
                    detailRow.label(text=us(mo[2]))
                # detailRow = dataCols[3].row()
                # detailRow.label(text=us(mo[3]))

            vTotal = sum([len(o.data.vertices) for o in meshes])
            bmTotal = sum([len(o.data.vertices) for o in meshes])
            trisTotal = sum([len(o.data.vertices) for o in meshes])

            totRow = dataCols[0].row()
            totRow.label(text="Total:")
            totRow = dataCols[1].row()
            totRow.label(text=us(vTotal))
            totRow = dataCols[2].row()
            totRow.label(text=us(vTotal))
            totRow = dataCols[3].row()
            totRow.label(text=us(trisTotal))


def register():
    bpy.utils.register_class(TrisCountUI)


def unregister():
    bpy.utils.unregister_class(TrisCountUI)


if __name__ == "__main__":
    register()
