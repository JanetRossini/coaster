import os

from utils import make_pairs, make_elements, activate_object_by_name, project_data_path
from v_mathutils import VtVector
from vtfilewriter import VtFileWriter

import bpy
from bpy_types import Operator
from bpy_types import Panel
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty


class RCG_OT_importfromfile(bpy.types.Operator):
    "Add object from file"
    bl_idname = "rcg.importfromfile"
    bl_label = "Import"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = '*.blend'
    filter_glob: StringProperty(default="*.blend", options={'HIDDEN'})
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        self.directory = project_data_path()
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        self.report({"INFO"}, "file path " + addon_dir)
        file_path = self.filepath
        directory = os.path.join(file_path, 'Object')
        _path, file_with_ext = os.path.split(file_path)
        filename, _ext = os.path.splitext(file_with_ext)
        self.report({"INFO"}, "adding " + file_path)
        bpy.ops.wm.append(filepath=file_path,
                          directory=directory,
                          filename=filename)
        item = bpy.data.objects[filename]
        item.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = item
        return {"FINISHED"}


class SelectFileEmpties(bpy.types.Operator, ImportHelper):
    """Select a text file"""
    bl_idname = "custom.select_empties"
    bl_label = "Select File Empties"

    filename_ext = ".txt"

    filter_glob: StringProperty(default="*.txt", options={'HIDDEN'})

    def execute(self, context):
        file_path = self.filepath

        vertices = []
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line into coordinates
                line_stripped = line \
                    .replace('<', '') \
                    .replace('>', '') \
                    .replace(' ', '')
                coordinates = line_stripped.strip().split(',')
                # Convert coordinates to floats and create a Vector
                vertex = (float(coordinates[0]), float(coordinates[1]), float(coordinates[2]))
                vertices.append(vertex)

            #            # Create empties at each vertex
            for i, vertex in enumerate(vertices):
                #            # Create a new empty
                bpy.ops.object.empty_add(location=vertex)
                # Rename the empty
                empty = bpy.context.object
                empty.name = f"Empty_{i}"

        return {'FINISHED'}


class RCG_OT_inputempties(Operator):
    """ Input a series of empties from a text file """
    bl_idname = "rcg.inputempties"
    bl_label = "Input Empties from file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.custom.select_empties('INVOKE_DEFAULT')
        return {'FINISHED'}


def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            line_stripped = line \
                .replace('<', '') \
                .replace('>', '') \
                .replace(' ', '') \
                .replace(',', ' ')
            # Assuming coordinates are separated by space
            coords = line_stripped.strip().split()
            if len(coords) >= 3:  # Ensure there are at least x, y, and z coordinates
                coordinates.append(tuple(map(float, coords)))
    return coordinates


class SelectFileNurbs(bpy.types.Operator, ImportHelper):
    """Select a text file"""
    bl_idname = "custom.select_nurbs"
    bl_label = "Select File Empties"

    filename_ext = ".txt"

    filter_glob: StringProperty(default="*.txt", options={'HIDDEN'})

    def execute(self, context):
        file_path = self.filepath
        coordinates = read_coordinates(file_path)
        create_nurbs_path(coordinates)
        return {'FINISHED'}


def create_nurbs_path(coordinates):
    nurbs_path = bpy.data.curves.new(name="NurbsPath", type='CURVE')
    nurbs_path.dimensions = '3D'
    nurbs_path.resolution_u = 32

    spline = nurbs_path.splines.new('NURBS')
    spline.points.add(len(coordinates) - 1)  # Add points for each coordinate

    for i, coord in enumerate(coordinates):
        x, y, z = coord
        spline.points[i].co = (x, y, z, 1)  # Use homogeneous coordinates

    obj = bpy.data.objects.new("NurbsPath", nurbs_path)
    bpy.context.collection.objects.link(obj)

    return obj


class RCG_OT_inputnurbspath(Operator):
    """ Input a nurbs path from a text file """
    bl_idname = "rcg.inputnurbspath"
    bl_label = "Input Nurbs Path from file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.custom.select_nurbs('INVOKE_DEFAULT')
        return {'FINISHED'}


class RCG_OT_addarray(Operator):
    """ Add ARRAY Modifier """
    bl_idname = "rcg.addarray"
    bl_label = "Add ARRAY Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 20
        bpy.context.object.modifiers["Array"].use_merge_vertices = True
        bpy.context.object.modifiers["Array"].constant_offset_displace[0] = 1
        bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0
        bpy.context.object.modifiers["Array"].fit_type = 'FIXED_COUNT'
        return {'FINISHED'}


class RCG_OT_addbezcurve(Operator):
    """ Add BEZIER Modifier """
    bl_idname = "rcg.addbezcurve"
    bl_label = "Add BEZIER Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.ops.object.modifier_set_active(modifier="Curve")
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["BezierCurve"]

        return {'FINISHED'}


class RCG_OT_addnurbscurve(Operator):
    """ Add NURBS Modifier """
    bl_idname = "rcg.addnurbscurve"
    bl_label = "Add NURBS Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.modifier_add(type='CURVE')
        bpy.ops.object.modifier_set_active(modifier="Curve")
        bpy.context.object.modifiers["Curve"].object = bpy.data.objects["NurbsPath"]

        return {'FINISHED'}


class RCG_OT_createbeziercurve(Operator):
        """ Create a BEZIER path """
        bl_idname = "rcg.createbeziercurve"
        bl_label = "Create BEZIER Path"
        bl_options = {"REGISTER", "UNDO"}

        @classmethod
        def poll(cls, context):
            return context.mode == "OBJECT"

        def execute(self, context):
            bpy.ops.curve.primitive_bezier_curve_add(radius=1, location=(0, 0, 0))
            bpy.context.object.data.resolution_u = 32

            return {'FINISHED'}


class RCG_OT_createnurbscurve(Operator):
        """ Create a NURBS path """
        bl_idname = "rcg.createnurbscurve"
        bl_label = "Create NURBS Path"
        bl_options = {"REGISTER", "UNDO"}

        @classmethod
        def poll(cls, context):
            return context.mode == "OBJECT"

        def execute(self, context):
            bpy.ops.curve.primitive_nurbs_path_add(radius=1, location=(0, 0, 0))
            bpy.context.object.data.resolution_u = 32

            return {'FINISHED'}


class RCGSettings(bpy.types.PropertyGroup):
    offset_distance: bpy.props.FloatProperty(
        name="Offset Distance",
        description="Distance (meters) from path to rail center.",
        default=0.15,
        min=0.0,
        max=1.0,
        step=0.1
    )

    column_spacing: bpy.props.IntProperty(
        name="Support Spacing",
        description="Number of fins between supports",
        default=10,
        min=5,
        max=15,
        step=1
    )

    column_diameter: bpy.props.FloatProperty(
        name="Support Diameter",
        description="What can I say? Diameter of the support.",
        default=0.08,
        min=0.08,
        max=0.32,
        step=0.1
    )


class RCG_OT_addcolumn(Operator):
    """ Add support columns"""
    bl_idname = "rcg.addcolumn"
    bl_label = "Add Supports"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def say_info(self, msg):
        self.report({"INFO"}, msg)

    def execute(self, context):
        offset_desired = context.scene.my_settings.offset_distance
        column_spacing = context.scene.my_settings.column_spacing
        column_diameter = context.scene.my_settings.column_diameter
        # self.say_info(f"Offset {offset_desired}")
        activate_object_by_name('ruler')
        obj = bpy.context.object
        if obj is None or obj.type != "MESH" or 'ruler' not in obj.name:
            self.report({'ERROR'}, 'You seem to have no ruler.')
            return {'CANCELLED'}
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        root_collection = self.set_rcg_collection_active()  # set to our collection
        fins = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        vertices = fins.data.vertices
        verts = vertices.values()
        pos_up_pairs = make_pairs(verts)  # tested in test_file_writing.py
        every_nth_pair = pos_up_pairs[::column_spacing]
        for pair in every_nth_pair:
            self.place_column(pair, column_diameter, offset_desired)
        bpy.context.view_layer.active_layer_collection = root_collection  # reset collection
        return {'FINISHED'}

    def place_column(self, pos_up_pair, diameter, offset_desired):
        position_vert = pos_up_pair[0]
        pos_vec = position_vert.co
        up_vec = pos_up_pair[1].co
        raw_offset = - (up_vec - pos_vec)
        mul = offset_desired / 0.5
        pos_vec = pos_vec + mul * raw_offset
        z_size = pos_vec.z
        bpy.ops.mesh.primitive_cylinder_add(
            location=(pos_vec.x, pos_vec.y, pos_vec.z - z_size / 2),
            vertices=6,
            radius=diameter / 2.0,
            depth=z_size,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        ob.name = 'Support'
        bpy.ops.object.shade_smooth()

    def set_rcg_collection_active(self):
        root_collection = bpy.context.view_layer.layer_collection.children[0]
        columns = bpy.data.collections.new("RCG Supports")
        scene = bpy.context.scene
        scene.collection.children.link(columns)
        bpy.context.view_layer.active_layer_collection \
            = bpy.context.view_layer.layer_collection.children["RCG Supports"]
        return root_collection


class RCG_OT_apply(Operator):
    """ Apply all modifiers """
    bl_idname = "rcg.apply"
    bl_label = "Apply All Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.modifier_apply(modifier="Array")
        bpy.ops.object.modifier_apply(modifier="Curve")

        return {'FINISHED'}


class RCG_OT_Export(Operator):
    """ Export """
    bl_idname = "rcg.export"
    bl_label = "Export"
    bl_options = {"REGISTER", "UNDO"}

    rcg_abs: bpy.props.BoolProperty(name="abs")
    rcg_bank: bpy.props.BoolProperty(name="bank")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        activate_object_by_name('ruler')
        obj = bpy.context.object
        if obj is None or obj.type != "MESH" or 'ruler' not in obj.name:
            self.report({'ERROR'}, 'You seem to have no ruler.')
            return {'CANCELLED'}
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)

        verts = obj_eval.data.vertices
        home = os.path.expanduser('~')
        filepath = os.path.join(home, 'coasterdata')
        basename = "test_data"
        size = 500
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, self.rcg_abs, self.rcg_bank)

        return {'FINISHED'}


class RCG_PT_sidebar(Panel):
    """Sidebar"""
    bl_label = "DIZZI COASTER GENERATOR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RollerCoaster"

    # noinspection SpellCheckingInspection
    def draw(self, context):
        settings = context.scene.my_settings
        col = self.layout.column(align=True)
        col.label(text="Add/Create track curve", icon='CURVE_DATA')
        col.operator("rcg.inputempties")
        col.operator("rcg.inputnurbspath")
        col.operator("rcg.createbeziercurve", text="Create Bezier Curve")
        col.operator("rcg.createnurbscurve", text="Create Path Curve")
        col.label(text="Import track object", icon='ANIM')
        col.operator("rcg.importfromfile", text="Select file")
        col.label(text="Add a modifier", icon='MODIFIER')
        col.operator("rcg.addarray")
        col.operator("rcg.addbezcurve")
        col.operator("rcg.addnurbscurve")
        col.operator("rcg.apply")
        col.label(text="Export Data", icon='EXPORT')
        self.make_two_arg_export_op(col, "Export Banked Path", False, True)
        self.make_two_arg_export_op(col, "Export Flat Path", False, False)
        self.make_two_arg_export_op(col, "Export Banked Path Abs", True, True)
        self.make_two_arg_export_op(col, "Export Flat Path Abs", True, False)
        col.label(text="Supports", icon='SNAP_VOLUME')
        col.operator("rcg.addcolumn")
        col.prop(settings, "column_spacing")
        col.prop(settings, "column_diameter")
        col.prop(settings, "offset_distance")

    @staticmethod
    def make_two_arg_export_op(col, text, absolute, bank):
        op = col.operator("rcg.export", text=text)
        op.rcg_abs = absolute
        op.rcg_bank = bank


classes = [ RCG_OT_addarray,
            RCG_OT_addbezcurve,
            RCG_OT_addcolumn,
            RCG_OT_addnurbscurve,
            RCG_OT_apply,
            RCG_OT_createbeziercurve,
            RCG_OT_createnurbscurve,
            RCG_OT_Export,
            RCG_OT_importfromfile,
            RCG_OT_inputempties,
            RCG_OT_inputnurbspath,
            RCG_PT_sidebar,
            RCGSettings,
            SelectFileEmpties,
            SelectFileNurbs, ]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_settings = bpy.props.PointerProperty(type=RCGSettings)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
