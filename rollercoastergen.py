from math import atan2, degrees, ceil
from mathutils import Vector, Quaternion  # use in Blender if you like

from vtfilewriter import VtFileWriter

""" from v_vector import Vector  # remove if you use mathutils
from v_quaternion import Quaternion  # remove if you use mathutils """


class Vehicle:
    """
    Vehicle class represents a vehicle solely in terms of its
    forward direction and upward direction, both normalized.
    Normal creation is by providing the vectors
    back - world position of rear
    up - world position of top of tail of vehicle
    front = world position of front of vehicle
 
    given an export from blender:
     u
    |\
    | \
    |  \
    b---f
 
    Theory of Operation:
 
    The private methods `_new_vehicle_without_yaw` and `_new_vehicle_without_pitch`
    return, well, a new vehicle, derived from the receiver, with yaw or pitch removed.
    Both these methods create a Quaternion with the appropriate rotation and apply it
    to the receiver's forward and upward to get the values for a new vehicle with
    yaw or pitch removed.
 
    The private method `_new_vehicle_with_roll_only` returns a vehicle
    with both yaw and pitch removed.
 
    The public method `roll_degrees` returns the desired roll angle, counterclockwise from vertical.
    `roll_degrees` uses the private method `roll_angle` which returns the arc-tangent
    of the receiver's upward.z and upward.y.
 
    `roll_degrees` returns 90 degrees minus the roll_angle of the vehicle with roll only,
    because that's the counterclockwise angle from vertical.
    (That is, it's adjusted to be what I think we want. We can adjust differently if need be.)
 
    Internally the sequence of operation is:
    1. Create the vehicle from input
    2. Ask it for roll_degrees, which will
    3. Transform the original to one without yaw
    4. Transform the yaw-less one to one also without pitch
    5. Ask that one for roll_angle
    6. Convert and return the desired angle in degrees
 
    This may seem odd. The idea is to have the Vehicle object be immutable:
    Once created, a Vehicle never changes. Instead, we get a new one that
    has been adjusted for no yaw or no pitch. This is thought by the people
    who think things to be a good way to design objects, so that they never change.
 
    Note:
        Because the vehicle is just represented by its forward and upward
        direction vectors, we can create a new one with desired forward and upward
        by Vehicle(zero_vector, upward, forward). The __init__ just works out to
        retain the provided upward and forward. Nifty, once you get over it.
 
    Note:
        For reasons that I cannot quite explain, the yaw removal uses the
        negative of the arc-tangent, and the pitch uses the positive.
        This is what it took to make it work. I cannot quite visualize why.
        (Later: I think it has to do with whether Y goes into the screen or out.)
 
    Note:
        I'm going to put the back, up, front members back into the class.
        I want them for better testing. JR: 2023-10-21
 
    Note:
        I'm going to extract methods to get the two desired quaternions, for two reasons:
        First, because I want to use them in my program that draws the pictures.
        Second, because the methods that create them have kind of a two-phase aspect,
        creating the quaternion and then applying it. Creating with a separate method
        will express that duality better. JR: 2023-10-21
    """

    def __init__(self, back, up, front):
        self.back = back
        self.up = up
        self.front = front
        self.forward = (front - back).normalized()
        self.upward = (up - back).normalized()

    def roll_degrees(self):
        angle = self._new_vehicle_with_roll_only()._roll_angle()
        angle_deg = 90 - degrees(angle)
        if angle_deg < 0:
            return 360 + angle_deg
        else:
            return angle_deg

    def _new_vehicle_without_yaw(self):
        remove_yaw = self._yaw_quaternion()
        new_forward = remove_yaw @ self.forward
        new_upward = remove_yaw @ self.upward
        return Vehicle(Vector((0, 0, 0)), new_upward, new_forward)

    def _yaw_quaternion(self):
        z_axis = Vector((0, 0, 1))
        rise = self.forward.y
        run = self.forward.x
        angle = atan2(rise, run)
        remove_yaw = Quaternion(z_axis, -angle)
        return remove_yaw

    def _new_vehicle_without_pitch(self):
        remove_pitch = self._pitch_quaternion()
        new_forward = remove_pitch @ self.forward
        new_upward = remove_pitch @ self.upward
        return Vehicle(Vector((0, 0, 0)), new_upward, new_forward)

    def _pitch_quaternion(self):
        """
        Only valid when applied to a vehicle whose yaw is already removed.
        I cannot explain this but I can demonstrate it. - JR
        :return:
        """
        y_axis = Vector((0, 1, 0))
        rise = self.forward.z
        run = self.forward.x
        angle = atan2(rise, run)
        remove_pitch = Quaternion(y_axis, angle)
        return remove_pitch

    def _new_vehicle_with_roll_only(self):
        """
        Note that the rotations have to be applied in order, one after the other.
        Computing both quaternions at the beginning will not work.
        """
        return self._new_vehicle_without_yaw()._new_vehicle_without_pitch()

    def _roll_angle(self):
        return atan2(self.upward.z, self.upward.y)


import bpy
import os
from bpy.types import Operator
from bpy.types import Panel
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

file_track05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track05.blend'
inner_track05 = 'Object'
object_track05 = 'track05'

file_track10 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track10.blend'
inner_track10 = 'Object'
object_track10 = 'track10'

file_track20 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/track20.blend'
inner_track20 = 'Object'
object_track20 = 'track20'

file_invtrack05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/invtrack05.blend'
inner_invtrack05 = 'Object'
object_invtrack05 = 'invtrack05'

file_invtrack10 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/invtrack10.blend'
inner_invtrack10 = 'Object'
object_invtrack10 = 'invtrack10'

file_invtrack20 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/invtrack20.blend'
inner_invtrack20 = 'Object'
object_invtrack20 = 'invtrack20'

file_trackruler05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackruler05.blend'
inner_trackruler05 = 'Object'
object_trackruler05 = 'trackruler05'

file_trackruler10 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackruler10.blend'
inner_trackruler10 = 'Object'
object_trackruler10 = 'trackruler10'

file_trackruler20 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackruler20.blend'
inner_trackruler20 = 'Object'
object_trackruler20 = 'trackruler20'

file_trackflatruler05 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackflatruler05.blend'
inner_trackflatruler05 = 'Object'
object_trackflatruler05 = 'trackflatruler05'

file_trackflatruler10 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackflatruler10.blend'
inner_trackflatruler10 = 'Object'
object_trackflatruler10 = 'trackflatruler10'

file_trackflatruler20 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/trackflatruler20.blend'
inner_trackflatruler20 = 'Object'
object_trackflatruler20 = 'trackflatruler20'

file_ngtrack1 = 'C:/Users/Terry/PycharmProjects/blenderPython/coasterobjects/ngtrack1.blend'
inner_ngtrack1 = 'Object'
object_ngtrack1 = 'ngtrack1'


class RCG_OT_addtrack05(Operator):
    """ Add an object called Track05 from a specific file """
    bl_idname = "rcg.addtrackobject05"
    bl_label = "0.5m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_track05, inner_track05, object_track05),
            directory=os.path.join(file_track05, inner_track05), filename=object_track05)
        track05 = bpy.data.objects["track05"]
        track05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = track05
        return {'FINISHED'}


class RCG_OT_addtrack10(Operator):
    """ Add an object called Track10 from a specific file """
    bl_idname = "rcg.addtrackobject10"
    bl_label = "1.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_track10, inner_track10, object_track10),
            directory=os.path.join(file_track10, inner_track10), filename=object_track10)
        track10 = bpy.data.objects["track10"]
        track10.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = track10
        return {'FINISHED'}


class RCG_OT_addtrack20(Operator):
    """ Add an object called Track20 from a specific file """
    bl_idname = "rcg.addtrackobject20"
    bl_label = "2.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_track20, inner_track20, object_track20),
            directory=os.path.join(file_track20, inner_track20), filename=object_track20)
        track20 = bpy.data.objects["track20"]
        track20.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = track20
        return {'FINISHED'}


class RCG_OT_addinvtrack05(Operator):
    """ Add an object called InvTrack05 from a specific file """
    bl_idname = "rcg.addinvtrackobject05"
    bl_label = "0.5m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_invtrack05, inner_invtrack05, object_invtrack05),
            directory=os.path.join(file_invtrack05, inner_invtrack05), filename=object_invtrack05)
        invtrack05 = bpy.data.objects["invtrack05"]
        invtrack05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = invtrack05

        return {'FINISHED'}


class RCG_OT_addinvtrack10(Operator):
    """ Add an object called InvTrack10 from a specific file """
    bl_idname = "rcg.addinvtrackobject10"
    bl_label = "1.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_invtrack10, inner_invtrack10, object_invtrack10),
            directory=os.path.join(file_invtrack10, inner_invtrack10), filename=object_invtrack10)
        invtrack10 = bpy.data.objects["invtrack10"]
        invtrack10.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = invtrack10

        return {'FINISHED'}


class RCG_OT_addinvtrack20(Operator):
    """ Add an object called InvTrack20 from a specific file """
    bl_idname = "rcg.addinvtrackobject20"
    bl_label = "2.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_invtrack20, inner_invtrack20, object_invtrack20),
            directory=os.path.join(file_invtrack20, inner_invtrack20), filename=object_invtrack20)
        invtrack20 = bpy.data.objects["invtrack20"]
        invtrack20.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = invtrack20

        return {'FINISHED'}


class RCG_OT_addngtrack1(Operator):
    """ Add an object called ngtrack1 from a specific file """
    bl_idname = "rcg.addngtrack1"
    bl_label = "Add 1m NG track"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_ngtrack1, inner_ngtrack1, object_ngtrack1),
            directory=os.path.join(file_ngtrack1, inner_ngtrack1), filename=object_ngtrack1)
        ngtrack1 = bpy.data.objects["ngtrack1"]
        ngtrack1.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = ngtrack1

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
                line_stripped = line.replace('<', '').replace('>', '').replace(' ', '')
                coordinates = line_stripped.strip().split(',')
                # Convert coordinates to floats and create a Vector
                vertex = Vector((float(coordinates[0]), float(coordinates[1]), float(coordinates[2])))
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
            line_stripped = line.replace('<', '').replace('>', '').replace(' ', '').replace(',', ' ')
            # Assuming coordinates are separated by space
            coords = line_stripped.strip().split()
            #            print(coords)
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

        # Read coordinates from the file
        coordinates = read_coordinates(file_path)
        #        print(coordinates)

        # Create a NURBS path using the coordinates
        nurbs_path_object = create_nurbs_path(coordinates)

        return {'FINISHED'}


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

    # Define the function to create a NURBS path


def create_nurbs_path(coordinates):
    # Create a new NURBS path
    nurbs_path = bpy.data.curves.new(name="NurbsPath", type='CURVE')
    nurbs_path.dimensions = '3D'
    nurbs_path.resolution_u = 2

    # Create a new spline
    spline = nurbs_path.splines.new('NURBS')
    spline.points.add(len(coordinates) - 1)  # Add points for each coordinate

    # Assign coordinates to the spline points
    for i, coord in enumerate(coordinates):
        x, y, z = coord
        spline.points[i].co = (x, y, z, 1)  # Use homogeneous coordinates

    # Create an object to hold the path
    obj = bpy.data.objects.new("NurbsPath", nurbs_path)
    bpy.context.collection.objects.link(obj)

    return obj


class RCG_OT_addruler05(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addruler05"
    bl_label = "0.5m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler05, inner_trackruler05, object_trackruler05),
            directory=os.path.join(file_trackruler05, inner_trackruler05), filename=object_trackruler05)
        trackruler05 = bpy.data.objects["trackruler05"]
        trackruler05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackruler05

        return {'FINISHED'}


class RCG_OT_addruler10(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addruler10"
    bl_label = "1.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler10, inner_trackruler10, object_trackruler10),
            directory=os.path.join(file_trackruler10, inner_trackruler10), filename=object_trackruler10)
        trackruler10 = bpy.data.objects["trackruler10"]
        trackruler10.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackruler10

        return {'FINISHED'}


class RCG_OT_addruler20(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addruler20"
    bl_label = "2.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackruler20, inner_trackruler20, object_trackruler20),
            directory=os.path.join(file_trackruler20, inner_trackruler20), filename=object_trackruler20)
        trackruler20 = bpy.data.objects["trackruler20"]
        trackruler20.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackruler20

        return {'FINISHED'}


class RCG_OT_addflatruler05(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addflatruler05"
    bl_label = "0.5m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackflatruler05, inner_trackflatruler05, object_trackflatruler05),
            directory=os.path.join(file_trackflatruler05, inner_trackflatruler05), filename=object_trackflatruler05)
        trackflatruler05 = bpy.data.objects["trackflatruler05"]
        trackflatruler05.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackflatruler05

        return {'FINISHED'}


class RCG_OT_addflatruler10(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addflatruler10"
    bl_label = "1.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackflatruler10, inner_trackflatruler10, object_trackflatruler10),
            directory=os.path.join(file_trackflatruler10, inner_trackflatruler10), filename=object_trackflatruler10)
        trackflatruler10 = bpy.data.objects["trackflatruler10"]
        trackflatruler10.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackflatruler10

        return {'FINISHED'}


class RCG_OT_addflatruler20(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addflatruler20"
    bl_label = "2.0m"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(filepath=os.path.join(file_trackflatruler20, inner_trackflatruler20, object_trackflatruler20),
            directory=os.path.join(file_trackflatruler20, inner_trackflatruler20), filename=object_trackflatruler20)
        trackflatruler20 = bpy.data.objects["trackflatruler20"]
        trackflatruler20.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = trackflatruler20

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


class RCG_OT_Exp_Banked_path(Operator):
    """ Set the render properties """
    bl_idname = "rcg.expbank"
    bl_label = "Export Banked Path"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/"

        abs = False
        bank = True
        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 500
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, abs, bank)

        return {'FINISHED'}


class RCG_OT_Exp_Flat_path(Operator):
    """ Set the render properties """
    bl_idname = "rcg.expflat"
    bl_label = "Export Flat Path"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/"

        abs = False
        bank = False
        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 500
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, abs, bank)

        return {'FINISHED'}


class RCG_OT_Exp_Banked_path_abs(Operator):
    """ Set the render properties """
    bl_idname = "rcg.expbankabs"
    bl_label = "Export Banked Path Abs"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/"

        abs = True
        bank = True
        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 500
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, abs, bank)

        return {'FINISHED'}


class RCG_OT_Exp_Flat_path_abs(Operator):
    """ Set the render properties """
    bl_idname = "rcg.expflatabs"
    bl_label = "Export Flat Path Abs"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # Put code here
        obj = bpy.context.object

        if obj is None or obj.type != "MESH":
            return

        # Output geometry
        obj_eval = obj.evaluated_get(bpy.context.view_layer.depsgraph)
        filepath = "C:/Users/Terry/PycharmProjects/blenderPython/"

        abs = True
        bank = False
        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 500
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files(basename, abs, bank)

        return {'FINISHED'}


# VtFileWriter begins here


class RCG_PT_sidebar(Panel):
    """Sidebar"""
    bl_label = "DIZZI COASTER GENERATOR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RollerCoaster"

    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text="Add/Create track curve", icon='CURVE_DATA')
        col.operator("rcg.inputempties")
        col.operator("rcg.inputnurbspath")
        col.operator("curve.primitive_bezier_curve_add", text="Create Bezier Curve")
        col.operator("curve.primitive_nurbs_path_add", text="Create Path Curve")
        col.label(text="Add a track", icon='ANIM')
        row = col.row()
        row.operator("rcg.addtrackobject05")
        row.operator("rcg.addtrackobject10")
        row.operator("rcg.addtrackobject20")
        col.label(text="Add an inverted track", icon='ANIM')
        row = col.row()
        row.operator("rcg.addinvtrackobject05")
        row.operator("rcg.addinvtrackobject10")
        row.operator("rcg.addinvtrackobject20")
        col.label(text="Add misc track", icon='ANIM')
        col.operator("rcg.addngtrack1")
        col.label(text="Add a track ruler", icon='ARROW_LEFTRIGHT')
        row = col.row()
        row.operator("rcg.addruler05")
        row.operator("rcg.addruler10")
        row.operator("rcg.addruler20")
        col.label(text="Add a modifier", icon='MODIFIER')
        col.operator("rcg.addarray")
        col.operator("rcg.addbezcurve")
        col.operator("rcg.addnurbscurve")
        col.operator("rcg.apply")
        col.label(text="Export Data", icon='EXPORT')
        col.operator("rcg.expbank")
        col.operator("rcg.expflat")
        col.operator("rcg.expbankabs")
        col.operator("rcg.expflatabs")


classes = [RCG_OT_inputempties, RCG_OT_inputnurbspath, RCG_OT_addtrack05, RCG_OT_addtrack10, RCG_OT_addtrack20,
    RCG_OT_addinvtrack05, RCG_OT_addinvtrack10, RCG_OT_addinvtrack20, RCG_OT_addngtrack1, RCG_OT_addflatruler05,
    RCG_OT_addflatruler10, RCG_OT_addflatruler20, RCG_OT_addruler05, RCG_OT_addruler10, RCG_OT_addruler20,
    RCG_OT_addarray, RCG_OT_addbezcurve, RCG_OT_addnurbscurve, RCG_OT_apply, RCG_OT_Exp_Banked_path,
    RCG_OT_Exp_Banked_path_abs, RCG_OT_Exp_Flat_path, RCG_OT_Exp_Flat_path_abs, RCG_PT_sidebar, SelectFileEmpties,
    SelectFileNurbs, ]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
