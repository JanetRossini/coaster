import os.path
from math import atan2, radians, ceil
import pytest

from modules.v_mathutils import VtVector, VtQuaternion

from test_data import tilt_45, fetch
from modules.vtfilewriter import VtFileWriter, Vehicle


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
        forward = VtVector((1, 1, 1)).normalized()
        # top view is x horizontal, y vertical
        z_axis = VtVector((0, 0, 1))
        rise = forward.y
        run = forward.x
        angle = atan2(rise, run)
        remove_yaw = VtQuaternion.axis_angle(z_axis, -angle)
        f_no_yaw = remove_yaw@forward
        assert f_no_yaw.y == pytest.approx(0, abs=0.001)

    def test_remove_pitch(self):
        """
        Test my theory of pitch removal.
        Valuable because we do not negate the angle here.
        """
        # pitch is rotation around y, uses z and x
        # we want z == 0
        forward = VtVector((1, 2, 3)).normalized()
        # side view is y horizontal, z vertical
        y_axis = VtVector((0, 1, 0))
        rise = forward.z
        run = forward.x
        angle = atan2(rise, run)
        remove_pitch = VtQuaternion.axis_angle(y_axis, angle)  # why not -?
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
        back = VtVector((1.234, 2.345, 3.456))
        roll = 129.0
        result = f"<{back.x:.3f}, {back.y:.3f}, {back.z:.3f}, {roll:.0f}>\n"
        assert result == "<1.234, 2.345, 3.456, 129>\n"

    def test_real_cross(self):
        v1 = VtVector((1, 2, 3))
        v2 = VtVector((2, 3, 4))
        v3 = v1.cross(v2)
        assert v3 == VtVector((-1, 2, -1))

    def test_real_quat(self):
        v = VtVector((1, 2, 3))
        axis = VtVector((0, 1, 0))
        quat = VtQuaternion.axis_angle(axis, radians(90))
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

    def test_big_string(self):
        program = """
//LSD_500_0
get_data() {
   // do something;
}
"""
        assert program == "\n//LSD_500_0\nget_data() {\n   // do something;\n}\n"

    def test_format_string(self):
        file_number = 3
        script_number = f"integer SCRIPT_NUMBER = {file_number};\n"
        assert script_number == "integer SCRIPT_NUMBER = 3;\n"

    def test_fold(self):
        s = list(range(10))
        n = 4
        l = [str(e) for e in s]
        l1 = [",".join(l[i:i + n]) for i in range(0, len(s), n)]
        l2 = ",\n".join(l1)
        result = f"list data = [\n{l2}\n];"
        assert result == 'list data = [\n0,1,2,3,\n4,5,6,7,\n8,9\n];'

    # @pytest.mark.skip("can't link up")
    def test_write_files(self):
        vectors = tilt_45
        verts = [Co(vector) for vector in vectors]
        filepath = os.path.expanduser("~/Desktop")
        size = 4
        writer = VtFileWriter(verts, filepath, "test", size)
        writer.write_files("ignored", False, True)
        # writer.make_output()  # uncomment to look at things
        # assert False


class Co:
    def __init__(self, vector):
        self.co = vector

    def __repr__(self):
        v = self.co
        return f"<{v.x}, {v.y}, {v.z}>"
