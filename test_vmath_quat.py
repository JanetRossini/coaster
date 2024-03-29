from math import radians

import pytest

from v_quaternion import Quaternion
from v_vector import Vector


class TestVMathQuaternion:

    def test_create(self):
        axis = Vector((1, 0, 0))
        q = Quaternion(axis, radians(90))

    def test_vec_mul(self):
        v = Vector((1, 2, 3))
        axis = Vector((0, 1, 0))
        quat = Quaternion(axis, radians(90))
        v2 = quat@v
        assert v2.x == pytest.approx(3, abs=0.001)
        assert v2.y == pytest.approx(2, abs=0.001)
        assert v2.z == pytest.approx(-1, abs=0.001)

    def test_slerp(self):
        axis = Vector((1, 2, 3))
        q1 = Quaternion(axis, 0)
        q2 = Quaternion(axis, radians(90))
        q3 = q1.slerp(q2, 0.5)
        # Quaternion(0.924, 0.102, 0.205, 0.307) != 0
        # value borrowed from test of mathutils slerp.
        assert q3.w == pytest.approx(0.924, abs=0.001)
        assert q3.x == pytest.approx(0.102, abs=0.001)
        assert q3.y == pytest.approx(0.205, abs=0.001)
        assert q3.z == pytest.approx(0.307, abs=0.001)

    def test_error(self):
        with pytest.raises(TypeError) as info:
            q1 = Quaternion(1, 2, 3, 4, "hello")
        assert "Object cannot be initialized from (1, 2, 3, 4, 'hello')" in str(info.value)

