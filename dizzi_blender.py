from math import atan2, degrees, ceil
from mathutils import Vector, Quaternion  # use in Blender if you like

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

file_path1 = 'C:/Users/Terry/PycharmProjects/blenderPython/track.blend'
inner_path1 = 'Object'
object_name1 = 'track'

file_path2 = 'C:/Users/Terry/PycharmProjects/blenderPython/invtrack.blend'
inner_path2 = 'Object'
object_name2 = 'invtrack'

file_path3 = 'C:/Users/Terry/PycharmProjects/blenderPython/trackruler.blend'
inner_path3 = 'Object'
object_name3 = 'trackruler'


class RCG_OT_addtrack(Operator):
    """ Add an object called Track from a specific file """
    bl_idname = "rcg.addtrackobject"
    bl_label = "Add normal track"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(
            filepath=os.path.join(file_path1, inner_path1, object_name1),
            directory=os.path.join(file_path1, inner_path1),
            filename=object_name1
        )
        track = bpy.data.objects["track"]
        track.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = track
        return {'FINISHED'}


class RCG_OT_addinvtrack(Operator):
    """ Add an object called InvTrack from a specific file """
    bl_idname = "rcg.addinvtrackobject"
    bl_label = "Add inverted track"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(
            filepath=os.path.join(file_path2, inner_path2, object_name2),
            directory=os.path.join(file_path2, inner_path2),
            filename=object_name2
        )
        invtrack = bpy.data.objects["invtrack"]
        invtrack.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = invtrack

        return {'FINISHED'}


class RCG_OT_addruler(Operator):
    """ Add an object called lineruler from a specific file """
    bl_idname = "rcg.addruler"
    bl_label = "Add Ruler"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        bpy.ops.wm.append(
            filepath=os.path.join(file_path3, inner_path3, object_name3),
            directory=os.path.join(file_path3, inner_path3),
            filename=object_name3
        )
        ruler = bpy.data.objects["trackruler"]
        ruler.select_set(state=True, view_layer=bpy.context.view_layer)
        bpy.context.view_layer.objects.active = ruler

        return {'FINISHED'}


class RCG_OT_addarray(Operator):
    """ Set the render properties """
    bl_idname = "rcg.addarray"
    bl_label = "Open ARRAY Modifier"
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
    bl_label = "Open BEZIER CURVE Modifier"
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
    bl_label = "Open NURBS CURVE Modifier"
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
    bl_label = "Export Banked Path Script"
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

        verts = obj_eval.data.vertices
        triples = [verts[i:i + 3] for i in range(0, len(verts) - 1, 2)]
        size = 800
        basename = "test_data"
        writer = VtFileWriter(verts, filepath, basename, size)
        writer.write_files()

        return {'FINISHED'}


class VtFileWriter:
    def __init__(self, vertices, path, base_name, size):
        self.vertices = vertices
        self.path = path
        self.base_name = base_name
        self.size = size

    def write_files(self):
        coords = tuple(v.co for v in self.vertices)
        triples = tuple(coords[i:i + 3] for i in range(0, len(coords) - 1, 2))
        all_lines = self.make_lines(triples)
        count = ceil(len(triples)/self.size)
        for file_number in range(count):
            start = file_number*self.size
            end = (file_number+1)*self.size
            lines = all_lines[start:end]
            name = [self.base_name, str(file_number)]
            file_name = "_".join(name) + ".lsl"
            full_path = os.path.join(self.path, file_name)
            with open(full_path, "w") as file:
                self.write_one_file(file_name, file_number, lines, start, file)
                print(f"File was written to {full_path}\n")

    def write_one_file(self, file_name, file_number, lines, start, file):
        from datetime import datetime
        now = datetime.now()
        file.write(f"// {file_name}\n")
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"// {time}\n")
        file.write("//     created by VtFileWriter\n")
        file.write("//     JR 20240113\n\n")
        file.write(f"integer SCRIPT_NUMBER = {file_number};\n")
        file.write(f"integer CHUNK_SIZE = {self.size};\n\n")
        file.write("list data = [\n")
        text = "\n,".join(lines)
        file.write(text)
        file.write("\n];\n")
        file.write(self.part_2)

    @staticmethod
    def make_lines(coordinate_triples):
        lines = []
        back_zero = coordinate_triples[0][0]
        for back, up, front in coordinate_triples:
            back_zeroed = back - back_zero
            roll = Vehicle(back, up, front).roll_degrees()
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    part_2 = """
write_data() {
    integer limit = llGetListLength(data);
    integer out_key = CHUNK_SIZE*SCRIPT_NUMBER;
    integer end_key = out_key + limit;
    llSay(0, llGetScriptName() + " writing " + (string) out_key + " up to " + (string) end_key);
    integer index;
    for (index = 0; index < limit; index++, out_key++) {
        llLinksetDataWrite("datakey"+(string) out_key,  llList2String( data , index));
    }
    llMessageLinked(LINK_THIS, SCRIPT_NUMBER + 1, "LOADING", NULL_KEY);
}

default {
    on_rez(integer start_param) {
        llResetScript();
    }

    state_entry() {
        if (SCRIPT_NUMBER == 0) {
            llLinksetDataReset();
            write_data();
        }
    }

    link_message(integer sender_num, integer num, string str, key id) {
        if (str != "LOADING") return;
        if (num != SCRIPT_NUMBER) return;
        write_data();
    }
}
"""


class RCG_PT_sidebar(Panel):
    """Sidebar"""
    bl_label = "Roller Coaster Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RollerCoaster"

    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text="Add a track curve")
        col.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE', text="Bezier Curve")
        col.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH', text="Path Curve")
        col.label(text="Add a track object")
        col.operator("rcg.addtrackobject")
        col.operator("rcg.addinvtrackobject")
        col.label(text="Add a track helper")
        col.operator("rcg.addruler")
        col.label(text="Add a modifier")
        col.operator("rcg.addarray")
        col.operator("rcg.addbezcurve")
        col.operator("rcg.addnurbscurve")
        col.operator("rcg.apply")
        col.label(text="Export Data")
        col.operator("rcg.expbank")


classes = [
    RCG_OT_addtrack,
    RCG_OT_addinvtrack,
    RCG_OT_addruler,
    RCG_OT_addarray,
    RCG_OT_addbezcurve,
    RCG_OT_addnurbscurve,
    RCG_OT_apply,
    RCG_OT_Exp_Banked_path,
    RCG_PT_sidebar,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()