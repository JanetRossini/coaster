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