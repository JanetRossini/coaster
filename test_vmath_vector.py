import pytest

from v_vector import Vector


class TestVMathVector:

    def test_eq(self):
        v1 = Vector((1, 2, 3))
        v2 = Vector((1, 2, 3))
        v3 = Vector((2, 3, 4))
        assert v1 == v2
        assert v1 != v3

    def test_vector_add(self):
        v1 = Vector((1, 2, 3))
        v2 = Vector((10, 20, 30))
        sum = v1 + v2
        assert sum == Vector((11, 22, 33))

    def test_vector_sub_and_neg(self):
        v1 = Vector((1, 2, 3))
        v2 = Vector((11, 22, 33))
        assert v2 - v1 == Vector((10, 20, 30))

    def test_named_coordinates(self):
        v1 = Vector((1, 2, 3))
        assert v1.x == 1
        assert v1.y == 2
        assert v1.z == 3

    def test_normalized(self):
        v1 = Vector((1, 2, 3))
        vn = v1.normalized()
        assert vn.length == pytest.approx(1, abs=0.00001)
        assert vn.x == pytest.approx(0.27, abs=0.01)
        assert vn.y == pytest.approx(0.54, abs=0.01)
        assert vn.z == pytest.approx(0.80, abs=0.01)

    def test_scalar_mul(self):
        v1 = Vector((1, 2, 3))
        assert v1*3 == Vector((3, 6, 9))
        assert 2*v1 == Vector((2, 4, 6))

    def test_cross_product(self):
        v1 = Vector((1, 2, 3))
        v2 = Vector((2, 3, 4))
        v3 = v1.cross(v2)
        assert v3 == Vector((-1, 2, -1))
