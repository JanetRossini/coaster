from math import atan2

import pytest
from mathutils import Vector, Quaternion


class TestCoaster:

    def test_hookup(self):
        assert 2+2 == 4

    def test_remove_yaw(self):
        # yaw is rotation around z, uses y and x
        forward = Vector((1, 1, 1)).normalized()
        # had to install mathutils for Vector to be recognized
        # top view is x horizontal, y vertical
        z_axis = Vector((0, 0, 1))
        rise = forward.y
        run = forward.x
        angle = atan2(rise, run)
        remove_yaw = Quaternion(z_axis, -angle)
        f_no_yaw = remove_yaw@forward
        assert f_no_yaw.y == pytest.approx(0, abs=0.001)

    def test_remove_pitch(self):
        # pitch is rotation around y, uses z and x
        forward = Vector((1, 1, 1)).normalized()
        # side view is y horizontal, z vertical
        y_axis = Vector((0, 1, 0))
        rise = forward.x
        run = forward.z
        angle = atan2(rise, run)
        remove_pitch = Quaternion(y_axis, -angle)
        f_no_pitch = remove_pitch@forward
        assert f_no_pitch.z == pytest.approx(0, abs=0.001)

    def test_vehicle(self):
        pass

