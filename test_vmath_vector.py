import pytest
from modules.v_mathutils import VtVector


class TestVMathVector:

    def test_vector_eq(self):
        v1 = VtVector((1, 2, 3))
        v2 = VtVector((1, 2, 3))
        v3 = VtVector((2, 3, 4))
        assert v1 == v2
        assert v1 != v3

    # works with mathutils, just not my stuff.
    # def test_vector_size(self):
    #     with pytest.raises(TypeError) as info:
    #         v1 = Vector((1, 2))
    #     with pytest.raises(TypeError) as info:
    #         v1 = Vector((1, 2, 3, 4))

    def test_vector_add(self):
        v1 = VtVector((1, 2, 3))
        v2 = VtVector((10, 20, 30))
        sum = v1 + v2
        assert sum == VtVector((11, 22, 33))

    def test_vector_length(self):
        v = VtVector((1, 2, 3))
        length_squared = 1 * 1 + 2 * 2 + 3 * 3
        assert v.length*v.length == pytest.approx(length_squared, abs=0.0001)

    def test_vector_sub_and_neg(self):
        v1 = VtVector((1, 2, 3))
        v2 = VtVector((11, 22, 33))
        assert v2 - v1 == VtVector((10, 20, 30))

    def test_named_coordinates(self):
        v1 = VtVector((1, 2, 3))
        assert v1.x == 1
        assert v1.y == 2
        assert v1.z == 3

    def test_normalized(self):
        v1 = VtVector((1, 2, 3))
        vn = v1.normalized()
        assert vn.length == pytest.approx(1, abs=0.00001)
        assert vn.x == pytest.approx(0.27, abs=0.01)
        assert vn.y == pytest.approx(0.54, abs=0.01)
        assert vn.z == pytest.approx(0.80, abs=0.01)

    def test_scalar_multiplication(self):
        v1 = VtVector((1, 2, 3))
        assert v1 * 3 == VtVector((3, 6, 9))
        assert 2 * v1 == VtVector((2, 4, 6))

    def test_cross_product(self):
        v1 = VtVector((1, 2, 3))
        v2 = VtVector((2, 3, 4))
        v3 = v1.cross(v2)
        assert v3 == VtVector((-1, 2, -1))

    # def test_array_add(self):
    #     import numpy as np
    #     a1 = np.array((1, 2, 3))
    #     a2 = np.array((3, 2, 1))
    #     a4 = np.array((4, 4, 4))
    #     a_sum = a1 + a2
    #     assert np.array_equal(a4, a_sum)

    # def test_mu_to_tuple(self):
    #     from mathutils import Vector
    #     v = Vector((1, 2, 3))
    #     x, y, z = v.to_tuple()
    #     assert x == 1
    #     assert y == 2
    #     assert z == 3

    # def test_vmu_to_tuple(self):
    #     from v_mathutils import Vector
    #     v = Vector((1, 2, 3))
    #     x, y, z = v.to_tuple()
    #     assert x == 1
    #     assert y == 2
    #     assert z == 3

