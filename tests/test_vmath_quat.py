from math import radians
import pytest
from modules.v_mathutils import VtQuaternion, VtVector


class TestVMathQuaternion:

    def test_create(self):
        axis = VtVector((1, 0, 0))
        q = VtQuaternion.axis_angle(axis, radians(90))

    def test_vec_mul(self):
        v = VtVector((1, 2, 3))
        axis = VtVector((0, 1, 0))
        quat = VtQuaternion.axis_angle(axis, radians(90))
        v2 = quat @ v
        assert v2.x == pytest.approx(3, abs=0.001)
        assert v2.y == pytest.approx(2, abs=0.001)
        assert v2.z == pytest.approx(-1, abs=0.001)

    def test_slerp(self):
        axis = VtVector((1, 2, 3))
        q1 = VtQuaternion.axis_angle(axis, 0)
        q2 = VtQuaternion.axis_angle(axis, radians(90))
        q3 = q1.slerp(q2, 0.5)
        # Quaternion(0.924, 0.102, 0.205, 0.307) != 0
        # value borrowed from test of mathutils slerp.
        assert q3.w == pytest.approx(0.924, abs=0.001)
        assert q3.x == pytest.approx(0.102, abs=0.001)
        assert q3.y == pytest.approx(0.205, abs=0.001)
        assert q3.z == pytest.approx(0.307, abs=0.001)

    def test_error(self):
        e1 = 'mathutils.Quaternion() takes at most 2 arguments (5 given)'
        e2 = "Object cannot be initialized from (1, 2, 3, 4, 'hello')"
        with pytest.raises(TypeError) as info:
            q1 = VtQuaternion(1, 2, 3, 4, "hello")
        assert e1 in str(info.value) or e2 in str(info.value)

    def test_quat_times_non_vector(self):
        axis = VtVector((0, 1, 0))
        quat = VtQuaternion.axis_angle(axis, radians(90))
        quat @ axis
        with pytest.raises(Exception):
            q = quat @ 21


    def test_quat_times_vector(self):
        def quat_x_vector(quat, vec):
            xyz = VtVector((quat.x, quat.y, quat.z))
            t = 2 * xyz.cross(vec)
            return vec + quat.w * t + xyz.cross(t)
        v = VtVector((1, 2, 3))
        axis = VtVector((0, 1, 0))
        quat = VtQuaternion.axis_angle(axis, radians(90))
        v2 = quat_x_vector(quat, v)
        assert v2.x == pytest.approx(3, abs=0.001)
        assert v2.y == pytest.approx(2, abs=0.001)
        assert v2.z == pytest.approx(-1, abs=0.001)

