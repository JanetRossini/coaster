from math import atan2

import pytest
from mathutils import Vector, Quaternion

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
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        yaw_removed = vehicle._new_vehicle_without_yaw()
        assert yaw_removed.forward.y == pytest.approx(0, abs=0.001)

    def test_vehicle_pitch(self):
        """
        Same thing, for pitch
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        pitch_removed = vehicle._new_vehicle_without_pitch()
        assert pitch_removed.forward.z == pytest.approx(0, abs=0.001)

    def test_vehicle_with_roll_only(self):
        """
        Drive out combining yaw and pitch to return roll only.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        roll_only = vehicle._new_vehicle_with_roll_only()
        assert roll_only.forward.y == pytest.approx(0, abs=0.001)
        assert roll_only.forward.z == pytest.approx(0, abs=0.001)

    def test_roll(self):
        """
        Drive out the roll calculation.
        """
        back, up, front = fetch(tilt_45, 0)
        vehicle = Vehicle(back, up, front)
        roll_degrees = vehicle.roll_degrees()
        assert roll_degrees == pytest.approx(16.1, abs=0.1)

    def test_all_roll(self):
        """
        Grand finale, all values are -45 apart, starting oddly.
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





