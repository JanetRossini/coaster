import os

from mathutils import Vector

from utils import make_pairs, activate_object_by_partial_name, coaster_objects_in_path, coaster_scripts_out_path, \
    coaster_data_in_path
from vtfilewriter import VtFileWriter

import bpy
from bpy_types import Operator
from bpy_types import Panel
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty


class RCG_OT_importFromFile(bpy.types.Operator):
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
        self.directory = coaster_objects_in_path()
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


class RCG_OT_inputEmpties(Operator):
    """ Input a series of empties from a text file """
    bl_idname = "rcg.inputempties"
    bl_label = "Input Empties from file"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = '*.txt'
    filter_glob: StringProperty(default="*.txt", options={'HIDDEN'})
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        self.directory = coaster_data_in_path()
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

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



# Make this a method? No need to return object?
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


class RCG_OT_inputNurbsPath(Operator):
    """ Input a nurbs path from a text file """
    bl_idname = "rcg.inputnurbspath"
    bl_label = "Input Nurbs Path from file"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".txt"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    filter_glob: StringProperty(default="*.txt", options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        self.directory = coaster_data_in_path()
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        file_path = self.filepath
        coordinates = read_coordinates(file_path)
        create_nurbs_path(coordinates)
        return {'FINISHED'}


class RCG_OT_addArrayModifier(Operator):
    """ Add ARRAY Modifier """
    bl_idname = "rcg.addarray"
    bl_label = "Add ARRAY Modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.object.modifier_add(type='ARRAY')
        modifier = bpy.context.object.modifiers["Array"]
        modifier.count = 20
        modifier.use_merge_vertices = True
        modifier.constant_offset_displace = Vector((1.0, 0.0, 0.0))
        modifier.fit_type = 'FIXED_COUNT'
        return {'FINISHED'}


class RCG_OT_addBezierModifier(Operator):
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


class RCG_OT_addNurbsModifier(Operator):
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


class RCG_OT_createBezierCurve(Operator):
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


class RCG_OT_createNurbsCurve(Operator):
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


class RCG_OT_addSupport(Operator):
    """ Add support columns"""
    bl_idname = "rcg.addsupport"
    bl_label = "Add Supports"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def say_info(self, msg):
        self.report({"INFO"}, msg)

    def execute(self, context):
        ruler = activate_object_by_partial_name('ruler')
        if ruler is None or ruler.type != "MESH" or 'ruler' not in ruler.name:
            self.report({'ERROR'}, 'You seem to have no ruler.')
            return {'CANCELLED'}

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        every_nth_pair = self.get_support_positions(context, ruler)
        self.place_supports(every_nth_pair, context)
        return {'FINISHED'}

    def place_supports(self, every_nth_pair, context):
        offset_desired = context.scene.rcg_settings.offset_distance
        column_diameter = context.scene.rcg_settings.column_diameter
        saved_collection = self.set_rcg_collection_active()  # set to our collection
        for pair in every_nth_pair:
            self.place_support(pair, column_diameter, offset_desired)
        bpy.context.view_layer.active_layer_collection = saved_collection  # reset collection

    def get_support_positions(self, context, ruler):
        fins = ruler.evaluated_get(bpy.context.view_layer.depsgraph)
        vertices = fins.data.vertices
        pos_up_pairs = make_pairs(vertices)  # tested in test_file_writing.py
        column_spacing = context.scene.rcg_settings.column_spacing
        every_nth_pair = pos_up_pairs[::column_spacing]
        return every_nth_pair

    def place_support(self, pos_up_pair, diameter, offset_desired):
        pos_vec = self.get_position_vector(offset_desired, pos_up_pair)
        self.add_support(pos_vec, diameter)

    def add_support(self, pos_vec, diameter):
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

    def get_position_vector(self, offset_desired, pos_up_pair):
        position_vert = pos_up_pair[0]
        pos_vec = position_vert.co
        up_vec = pos_up_pair[1].co
        raw_offset = - (up_vec - pos_vec)
        mul = offset_desired / 0.5
        pos_vec = pos_vec + mul * raw_offset
        return pos_vec

    def set_rcg_collection_active(self):
        current_collection = bpy.context.view_layer.active_layer_collection
        support_collection = bpy.data.collections.new("RCG Supports")
        bpy.context.scene.collection.children.link(support_collection)
        bpy.context.view_layer.active_layer_collection \
            = bpy.context.view_layer.layer_collection.children["RCG Supports"]
        return current_collection


class RCG_OT_applyAllModifiers(Operator):
    """ Apply all modifiers """
    bl_idname = "rcg.applyallmodifiers"
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
        ruler = activate_object_by_partial_name('ruler')
        if ruler is None or ruler.type != "MESH" or 'ruler' not in ruler.name:
            self.report({'ERROR'}, 'You seem to have no ruler.')
            return {'CANCELLED'}
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Output geometry
        obj_eval = ruler.evaluated_get(bpy.context.view_layer.depsgraph)

        verts = obj_eval.data.vertices
        home = os.path.expanduser('~')
        filepath = coaster_scripts_out_path()
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
        settings = context.scene.rcg_settings
        col = self.layout.column(align=True)
        col.label(text="Add/Create track curve", icon='CURVE_DATA')
        col.operator("rcg.inputempties")
        col.operator("rcg.inputnurbspath")
        col.operator("rcg.createbeziercurve", text="Create Bezier Curve")
        col.operator("rcg.createnurbscurve", text="Create Path Curve")
        col.label(text="Import track object", icon='SNAP_VOLUME')
        col.operator("rcg.importfromfile", text="Select file")
        col.label(text="Add a modifier", icon='MODIFIER')
        col.operator("rcg.addarray")
        col.operator("rcg.addbezcurve")
        col.operator("rcg.addnurbscurve")
        col.operator("rcg.applyallmodifiers")
        col.label(text="Export Data", icon='EXPORT')
        self.make_two_arg_export_op(col, "Export Banked Path", False, True)
        self.make_two_arg_export_op(col, "Export Flat Path", False, False)
        self.make_two_arg_export_op(col, "Export Banked Path Abs", True, True)
        self.make_two_arg_export_op(col, "Export Flat Path Abs", True, False)
        col.label(text="Supports", icon='SNAP_VOLUME')
        col.operator("rcg.addsupport")
        col.prop(settings, "column_spacing")
        col.prop(settings, "column_diameter")
        col.prop(settings, "offset_distance")

    @staticmethod
    def make_two_arg_export_op(col, text, absolute, bank):
        op = col.operator("rcg.export", text=text)
        op.rcg_abs = absolute
        op.rcg_bank = bank


classes = [RCG_OT_addArrayModifier,
           RCG_OT_addBezierModifier,
           RCG_OT_addNurbsModifier,
           RCG_OT_addSupport,
           RCG_OT_applyAllModifiers,
           RCG_OT_createBezierCurve,
           RCG_OT_createNurbsCurve,
           RCG_OT_Export,
           RCG_OT_importFromFile,
           RCG_OT_inputEmpties,
           RCG_OT_inputNurbsPath,
           RCG_PT_sidebar,
           RCGSettings,
           ]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.rcg_settings = bpy.props.PointerProperty(type=RCGSettings)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
