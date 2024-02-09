import os.path
from math import atan2, radians, ceil

import pytest

# from mathutils import Vector, Quaternion
from v_vector import Vector
from v_quaternion import Quaternion
from test_data import tilt_45, fetch
from vehicle import Vehicle


class TestCoasterVehicle:
    """
    This is the sequence of tests I wrote, one at a time,
    during the creation of the Vehicle class. Each one
    got me a step closer to what I wanted.

    It's worth noting that I have about a million lines
    of experimentation and nearly-working tests and code
    in another project. When I was sure I could get it right,
    I created this project to provide a decent package for
    what we need.

    I would not usually do all this commentary because my
    partner or team would be sitting together when we created
    all this, so they'd know what had happened. The comments
    can be ignored, or might raise questions or provide ideas
    about how I work.

    Basically, write one test to show that some idea works,
    make it work, repeat with another test.
    """

    def test_hookup(self):
        """
        just check to be sure the tests run.
        I usually start with this
        """
        assert 2+2 == 4

    def test_remove_yaw(self):
        """
        Test my theory of yaw removal via Quaternion
        Note that we negate the angle when we create the Quaternion.
        Note also quaternion@vector is multiplication. Surprised me too.
        """
        # yaw is rotation around z, uses y and x
        # we want y == 0
        forward = Vector((1, 1, 1)).normalized()
        # top view is x horizontal, y vertical
        z_axis = Vector((0, 0, 1))
        rise = forward.y
        run = forward.x
        angle = atan2(rise, run)
        remove_yaw = Quaternion(z_axis, -angle)
        f_no_yaw = remove_yaw@forward
        assert f_no_yaw.y == pytest.approx(0, abs=0.001)

    def test_remove_pitch(self):
        """
        Test my theory of pitch removal.
        Valuable because we do not negate the angle here.
        """
        # pitch is rotation around y, uses z and x
        # we want z == 0
        forward = Vector((1, 2, 3)).normalized()
        # side view is y horizontal, z vertical
        y_axis = Vector((0, 1, 0))
        rise = forward.z
        run = forward.x
        angle = atan2(rise, run)
        remove_pitch = Quaternion(y_axis, angle)  # why not -?
        f_no_pitch = remove_pitch@forward
        assert f_no_pitch.z == pytest.approx(0, abs=0.001)

    def test_vehicle_yaw(self):
        """
        I used this test to drive pushing the yaw quaternion to the class,
        and to drive creating the new vehicle without yaw.
        Removing yaw should zero the y value of the forward vector.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        yaw_removed = vehicle._new_vehicle_without_yaw()
        assert yaw_removed.forward.y == pytest.approx(0, abs=0.001)

    def test_vehicle_pitch(self):
        """
        Same thing, for pitch.
        Removing pitch should zero the z angle of the forward vector.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        pitch_removed = vehicle._new_vehicle_without_pitch()
        assert pitch_removed.forward.z == pytest.approx(0, abs=0.001)

    def test_vehicle_with_roll_only(self):
        """
        Drive out combining yaw and pitch to return roll only.
        Resulting vehicle should have both y and z zeroed.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        roll_only = vehicle._new_vehicle_with_roll_only()
        assert roll_only.forward.x == pytest.approx(1, abs=0.001)
        assert roll_only.forward.y == pytest.approx(0, abs=0.001)
        assert roll_only.forward.z == pytest.approx(0, abs=0.001)

    def test_roll(self):
        """
        Drive out the roll calculation.
        First data triangle is not vertical.
        Correct angle is 16.1 degrees counterclockwise as shown.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        roll_degrees = vehicle.roll_degrees()
        assert roll_degrees == pytest.approx(16.1, abs=0.1)

    def test_all_roll(self):
        """
        Grand finale, all values are -45 apart, starting oddly,
        because first one is counter-clockwise a bit but the rest
        go around clockwise.
        """
        prior = 0
        print()
        for i in range(0,9):
            vehicle = Vehicle(*fetch(tilt_45, i))
            roll_degrees = vehicle.roll_degrees()
            print(i, roll_degrees, roll_degrees - prior)
            if prior:
                diff = roll_degrees - prior
                assert diff == pytest.approx(-45, abs=0.1) or diff == pytest.approx(315, abs=0.1)
            prior = roll_degrees

    def test_all_roll_from_verts(self):
        prior = 0
        verts = tilt_45
        assert len(verts)%2 == 1  # must be odd
        triples = [verts[i:i+3] for i in range(0, len(verts)-1, 2)]
        for back, up, front in triples:
            print("one trip", back, up, front)
            roll = Vehicle(back, up, front).roll_degrees()
            if prior:
                diff = roll - prior
                assert diff == pytest.approx(-45, abs=0.1) or diff == pytest.approx(315, abs=0.1)
            prior = roll
        # assert False

    def test_format(self):
        back = Vector((1.234, 2.345, 3.456))
        roll = 129.0
        result = f"<{back.x:.3f}, {back.y:.3f}, {back.z:.3f}, {roll:.0f}>\n"
        assert result == "<1.234, 2.345, 3.456, 129>\n"

    def test_real_cross(self):
        v1 = Vector((1, 2,3))
        v2 = Vector((2, 3, 4))
        v3 = v1.cross(v2)
        assert v3 == Vector((-1, 2, -1))

    def test_real_quat(self):
        v = Vector((1, 2, 3))
        axis = Vector((0, 1, 0))
        quat = Quaternion(axis, radians(90))
        v2 = quat@v
        assert v2.x == pytest.approx(3, abs=0.001)
        assert v2.y == pytest.approx(2, abs=0.001)
        assert v2.z == pytest.approx(-1, abs=0.001)

    def test_partition(self):
        def make_chunks(items, size):
            i = 0
            while i < len(items):
                yield items[i:i + size]
                i += size

        trips = [(i, i + 1, i + 2) for i in range(0, 2000)]
        chunks = list(make_chunks(trips, 800))
        assert len(chunks) == 3
        assert len(chunks[0]) == 800
        assert len(chunks[1]) == 800
        assert len(chunks[2]) == 400

    def test_partition_comprehension(self):
        trips = [(i, i + 1, i + 2) for i in range(0, 2000)]
        size = 800
        number_of_slices = (len(trips) + size - 1) // size
        chunks = [trips[i*size:i*size+size] for i in range(number_of_slices)]
        assert len(chunks) == 3
        assert len(chunks[0]) == 800
        assert len(chunks[1]) == 800
        assert len(chunks[2]) == 400

    def test_make_filename(self):
        def make_filename(items):
            formatted = f"base/dizzi/triples{items[0]:03d}-{items[1]:03d}.txt"
            return formatted

        assert make_filename((0, 800)) == "base/dizzi/triples000-800.txt"

    def test_comp(self):
        size = 500
        count = ceil(1200/500)
        assert count == 3
        assert ceil(1000/500) == 2
        count = ceil(1200/500)
        assert count == 3
        slices = [(i*size, i*size+size) for i in range(0, count)]
        assert slices[0] == (0, 500)
        assert slices[1] == (500, 1000)
        assert slices[2] == (1000, 1500)

    def test_triples(self):
        size = 500
        triples = [(i, i + 1, i + 2) for i in range(0, 1200)]
        assert len(triples) == 1200
        assert triples[0] == (0, 1, 2)
        assert triples[1] == (1, 2, 3)
        number_of_slices = ceil(len(triples) / size)
        assert number_of_slices == 3
        slices = [triples[i * size:i * size + size] for i in range(0, number_of_slices)]
        assert len(slices[0]) == 500
        assert len(slices[1]) == 500
        assert len(slices[2]) == 200

    def test_triples_loop(self):
        size = 500
        triples = [(i, i + 1, i + 2) for i in range(0, 1200)]
        assert len(triples) == 1200
        assert triples[0] == (0, 1, 2)
        assert triples[1] == (1, 2, 3)
        number_of_slices = ceil(len(triples) / size)
        assert number_of_slices == 3
        slices = []
        for i in range(0, number_of_slices):
            start = i*size
            finish = i*size + size
            slices.append(triples[start:finish])
        assert len(slices[0]) == 500
        assert len(slices[1]) == 500
        assert len(slices[2]) == 200

    def test_write_files(self):
        vectors = tilt_45
        verts = [Co(vector) for vector in vectors]
        filepath = os.path.expanduser("~/Desktop")
        size = 4
        writer = VtFileWriter(verts, filepath, "test", size)
        writer.write_files()
        # writer.make_output()
        assert False


class Co:
    def __init__(self, vector):
        self.co = vector

    def __repr__(self):
        v = self.co
        return f"<{v.x}, {v.y}, {v.z}>"


class VtFileWriter:
    def __init__(self, vertices, path, base_name, size):
        self.vertices = vertices
        self.path = path
        self.base_name = base_name
        self.size = size

    def write_files(self):
        coords = [v.co for v in self.vertices]
        triples = [coords[i:i + 3] for i in range(0, len(coords) - 1, 2)]
        all_lines = self.make_lines(triples)
        count = ceil(len(triples)/self.size)
        for file_number in range(count):
            start = file_number*self.size
            end = (file_number+1)*self.size
            lines = all_lines[start:end]
            file_name = self.base_name + str(file_number) + ".lsl"
            full_path = os.path.join(self.path, file_name)
            with open(full_path, "w") as file:
                self.write_one_file(lines, start, file)
                print(f"File was written to {full_path}\n")

    @staticmethod
    def write_one_file(lines, start, file):
        comma = ""
        file.write("list vectdata = [\n")
        for line in lines:
            file.write(comma + line)
            comma = ","
        file.write("];\n")
        file.write("\n")
        file.write("default\n")
        file.write("{\n")
        file.write("  state_entry()\n")
        file.write("  {\n")
        file.write("    integer length = llGetListLength(vectdata);\n")
        if start == 0:
            file.write("    llLinksetDataReset();\n")
        file.write(f"    integer outKey = {start};\n")
        file.write(f"    integer inKey = 0;\n")
        file.write("    integer limit = inKey + length;\n")
        file.write("    for(; inKey < limit; ++outKey, ++inKey) {\n")
        file.write('      llLinksetDataWrite("datakey"+(string)outKey,  llList2String( vectdata , inKey) );\n')
        file.write("    }\n")
        file.write("  }\n")
        file.write("}\n")

    @staticmethod
    def make_lines(coordinate_triples):
        lines = []
        back_zero = coordinate_triples[0][0]
        for back, up, front in coordinate_triples:
            back_zeroed = back - back_zero
            roll = Vehicle(back, up, front).roll_degrees()
            output = f"<{back_zeroed.x:.3f}, {back_zeroed.y:.3f}, {back_zeroed.z:.3f}, {roll:.0f}>\n"
            lines.append(output)
        return lines







