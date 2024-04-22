import os
from v_mathutils import VtVector  # use in Blender if you like
from vtfilewriter import VtFileWriter

import bpy
from bpy.types import Operator
from bpy.types import Panel
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty


def make_elements(name):
    home = os.path.expanduser('~')
    working = os.path.join(home, 'PycharmProjects', 'coaster',  'coasterobjects')
    filepath = os.path.join(working, name + '.blend')
    directory = os.path.join(filepath, 'Object')
    filename = name
    return filepath, directory, filename

# def make_elements(name):
#     working = os.getcwd()  # comment next line, should still work for DS
#     working = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects'
#     filepath = os.path.join(working, name + '.blend')
#     directory = os.path.join(filepath, 'Object')
#     filename = name
#     return filepath, directory, filename


class RCG_OT_importObject(Operator):
    """ Add an object from a premade blender file """
    bl_idname = "rcg.importobject"
    bl_label = "Size"
    bl_options = {"REGISTER", "UNDO"}

    rcg_file: bpy.props.StringProperty(name="Default Value")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        if self.rcg_file != "":
            name = self.rcg_file
        else:
            name = "track05"
            self.report({"WARNING"}, "defaulting to " + name)
        self.report({"INFO"}, "adding " + name)
        filepath, directory, filename = make_elements(name)
        bpy.ops.wm.append(filepath=filepath,
                          directory=directory,
                          filename=filename)
        track05 = bpy.data.objects[name]
        track05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = track05
        return {'FINISHED'}


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
                line_stripped = line\
                    .replace('<', '')\
                    .replace('>', '')\
                    .replace(' ', '')
                coordinates = line_stripped.strip().split(',')
                # Convert coordinates to floats and create a Vector
                vertex = VtVector((float(coordinates[0]), float(coordinates[1]), float(coordinates[2])))
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
            line_stripped = line\
                .replace('<', '')\
                .replace('>', '')\
                .replace(' ', '')\
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
    nurbs_path.resolution_u = 2

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
        # Define the function to read coordinates from the text file

        # File path containing the coordinates
        #        file_path = "C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/nurbs.txt"

        # Read coordinates from the file
        #        coordinates = read_coordinates(file_path)

        # Create a NURBS path using the coordinates
        #        nurbs_path_object = create_nurbs_path(coordinates)
        return {'FINISHED'}


class RCG_OT_addarray(Operator):
    """ Set the render properties """
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
    """ Set the render properties """
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
    """ Set the render properties """
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

class RCG_OT_addcolumn(Operator):
    bl_idname = "rcg.addcolumn"
    bl_label = "Add Column"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def say_info(self, msg):
        self.report({"INFO"}, msg)

    def execute(self, context):
        obj = bpy.context.object
        if obj is None or obj.type != "MESH":
            return {'CANCELLED'}
        root_collection = self.set_rcg_collection_active()
        fins = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        vertices = fins.data.vertices
        verts = vertices.values()
        pos_up_pairs = [verts[i:i+2] for i in range(0, len(verts), 2)]
        every_tenth_pair = pos_up_pairs[::10]
        for pair in every_tenth_pair:
            self.place_column(pair)
        bpy.context.view_layer.active_layer_collection = root_collection
        return {'FINISHED'}

    def place_column(self, pos_up_pair):
        position_vert = pos_up_pair[0]
        pos_co = position_vert.co
        z_size = pos_co.z
        bpy.ops.mesh.primitive_cylinder_add(
            location=(pos_co.x,pos_co.y, pos_co.z - z_size / 2),
            vertices=6,
            radius=0.04,
            depth=z_size,
            end_fill_type='NOTHING',
            enter_editmode=False)
        ob = bpy.context.object
        ob.name = 'Support'
        bpy.ops.object.shade_smooth()
        # x_size, y_size, _old_z = ob.dimensions
        # ob.dimensions = [x_size/10, y_size/10, z_size]

    def set_rcg_collection_active(self):
        root_collection = bpy.context.view_layer.layer_collection.children[0]
        columns = bpy.data.collections.new("RCG Supports")
        scene = bpy.context.scene
        scene.collection.children.link(columns)
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
            "RCG Supports"]
        return root_collection


class RCG_OT_apply(Operator):
    """ Set the render properties """
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
    """ Set the render properties """
    bl_idname = "rcg.export"
    bl_label = "Export"
    bl_options = {"REGISTER", "UNDO"}

    rcg_abs: bpy.props.BoolProperty(name="abs")
    rcg_bank: bpy.props.BoolProperty(name="bank")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return {'CANCELLED'}

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
        col = self.layout.column(align=True)
        col.label(text="Add/Create track curve", icon='CURVE_DATA')
        col.operator("rcg.inputempties")
        col.operator("rcg.inputnurbspath")
        col.operator("curve.primitive_bezier_curve_add", text="Create Bezier Curve")
        col.operator("curve.primitive_nurbs_path_add", text="Create Path Curve")
        col.label(text="Add a track", icon='ANIM')
        row = col.row()
        op05 = row.operator("rcg.importobject", text="0.5m")
        op05.rcg_file = "track05"
        op05 = row.operator("rcg.importobject", text="1.0m")
        op05.rcg_file = "track10"
        op05 = row.operator("rcg.importobject", text="2.0m")
        op05.rcg_file = "track20"
        col.label(text="Add an inverted track", icon='ANIM')
        row = col.row()
        row.operator("rcg.importobject", text="0.5m").rcg_file = "invtrack05"
        row.operator("rcg.importobject", text="1.0m").rcg_file = "invtrack10"
        row.operator("rcg.importobject", text="2.0m").rcg_file = "invtrack20"
        col.label(text="Add misc track", icon='ANIM')
        row = col.row()
        op05 = row.operator("rcg.importobject", text="Add 1m NG Track")
        op05.rcg_file = "ngtrack1"
        col.label(text="Add a track ruler", icon='ARROW_LEFTRIGHT')
        row = col.row()
        row.operator("rcg.importobject", text="0.5m").rcg_file = "trackruler05"
        row.operator("rcg.importobject", text="1.0m").rcg_file = "trackruler10"
        row.operator("rcg.importobject", text="2.0m").rcg_file = "trackruler20"
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
        col.label(text="Supports", icon='ANIM')
        col.operator("rcg.addcolumn")

    @staticmethod
    def make_two_arg_export_op(col, text, absolute, bank):
        op = col.operator("rcg.export", text=text)
        op.rcg_abs = absolute
        op.rcg_bank = bank


classes = [RCG_OT_addarray,
           RCG_OT_addbezcurve,
           RCG_OT_addcolumn,
           RCG_OT_addnurbscurve,
           RCG_OT_apply,
           RCG_OT_Export,
           RCG_OT_importObject,
           RCG_OT_inputempties,
           RCG_OT_inputnurbspath,
           RCG_PT_sidebar,
           SelectFileEmpties,
           SelectFileNurbs, ]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
