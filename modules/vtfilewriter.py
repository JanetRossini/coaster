import os
from math import ceil, degrees, atan2
try:
    from v_mathutils import VtVector, VtQuaternion
except ModuleNotFoundError:
    from modules.v_mathutils import VtVector, VtQuaternion

# Somewhat nasty trick to deal with where Blender starts looking for things,
# while keeping our tests running.
# try:
#     from v_mathutils import Vector, Quaternion
# except ModuleNotFoundError:
#     from .v_mathutils import Vector, Quaternion


class VtFileWriter:
    def __init__(self, vertices, path, base_name, size):
        self.vertices = vertices
        self.path = path
        self.base_name = base_name
        self.size = size

    def write_files(self, name, abs, bank):
        vt_vectors = tuple(VtVector.from_vertex(v) for v in self.vertices)
        triples = tuple(vt_vectors[i:i + 3] for i in range(0, len(vt_vectors) - 1, 2))
        all_lines = self.make_lines(triples, abs, bank)
        count = ceil(len(triples)/self.size)
        for file_number in range(count):
            start = file_number*self.size
            end = (file_number+1)*self.size
            lines = all_lines[start:end]
            name = [self.base_name, str(file_number)]
            file_name = "_".join(name) + ".lsl"
            full_path = os.path.join(self.path, file_name)
            with open(full_path, "w") as file:
                self.write_one_file(file_name, file_number, count, lines, file)
                print(f"File was written to {full_path}\n")

    def write_one_file(self, file_name, file_number, file_count, lines, file):
        from datetime import datetime
        now = datetime.now()
        file.write(f"// {file_name}\n")
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"// {time}\n")
        file.write("//    created by VtFileWriter\n")
        file.write("//    JR 20240115 - inert, last sends LOADING_DONE\n")
        file.write("//    Script names do not matter.\n\n")
        file.write(f"integer SCRIPT_NUMBER = {file_number};\n")
        file.write(f"integer LAST_SCRIPT_NUMBER= {file_count-1};\n")
        file.write(f"integer CHUNK_SIZE = {self.size};\n\n")
        file.write("list data = [\n")
        text = "\n,".join(lines)
        file.write(text)
        file.write("\n];\n")
        file.write(self.fixed_part)

    @staticmethod
    def make_lines(coordinate_triples, absolute, bank):
        lines = []
        if absolute:
            back_zero = VtVector((0, 0, 0))
        else:
            back_zero = coordinate_triples[0][0]

        for back, up, front in coordinate_triples:
            back_zeroed = back - back_zero
            roll = Vehicle(back, up, front).roll_degrees() if bank else 0
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>"
            lines.append(output)
        return lines

    fixed_part = """
// nothing varies from here on down
 
write_data() {
    integer limit = llGetListLength(data);
    integer out_key = CHUNK_SIZE*SCRIPT_NUMBER;
    integer end_key = out_key + limit;
    llSay(0, llGetScriptName() + " writing " + (string) out_key + " up to " + (string) end_key);
    integer index;
    for (index = 0; index < limit; index++, out_key++) {
        llLinksetDataWrite("datakey"+(string) out_key,  llList2String( data , index));
    }
    if (SCRIPT_NUMBER == LAST_SCRIPT_NUMBER) {
        integer keyCount = llLinksetDataCountKeys(); 
        llSay(0, "SIGNALLING LOADING_DONE " + (string) keyCount);
        llMessageLinked(LINK_THIS, keyCount, "LOADING_DONE", NULL_KEY);
    } else {
        llMessageLinked(LINK_THIS, SCRIPT_NUMBER + 1, "LOADING", NULL_KEY);
    }
}
 
default {
    on_rez(integer start_param) {
        llResetScript();
    }
 
    state_entry() {
    }
 
    link_message(integer sender_num, integer num, string str, key id) {
        if (str != "LOADING") return;
        if (num != SCRIPT_NUMBER) return;
        if (SCRIPT_NUMBER == 0) {
            llLinksetDataReset();
            llSay(0, "SCRIPT 0 Resetting LSD");
        }
        write_data();
    }
}
"""


class Vehicle:
    def __init__(self, back, up, front):
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
        return Vehicle(VtVector((0, 0, 0)), new_upward, new_forward)

    def _yaw_quaternion(self):
        z_axis = VtVector((0, 0, 1))
        rise = self.forward.y
        run = self.forward.x
        angle = atan2(rise, run)
        remove_yaw = VtQuaternion.axis_angle(z_axis, -angle)
        return remove_yaw

    def _new_vehicle_without_pitch(self):
        remove_pitch = self._pitch_quaternion()
        new_forward = remove_pitch @ self.forward
        new_upward = remove_pitch @ self.upward
        return Vehicle(VtVector((0, 0, 0)), new_upward, new_forward)

    def _pitch_quaternion(self):
        """
        Only valid when applied to a vehicle whose yaw is already removed.
        I cannot explain this but I can demonstrate it. - JR
        :return:
        """
        y_axis = VtVector((0, 1, 0))
        rise = self.forward.z
        run = self.forward.x
        angle = atan2(rise, run)
        remove_pitch = VtQuaternion.axis_angle(y_axis, angle)
        return remove_pitch

    def _new_vehicle_with_roll_only(self):
        """
        Note that the rotations have to be applied in order, one after the other.
        Computing both quaternions at the beginning will not work.
        """
        return self._new_vehicle_without_yaw()._new_vehicle_without_pitch()

    def _roll_angle(self):
        return atan2(self.upward.z, self.upward.y)
