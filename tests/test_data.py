from modules.v_mathutils import VtVector

"""
This is just the test data from Blender, converted into Python format.
Tests only use the `tilt_45`, because of ages of work not shown here.
"""


def fetch(array, index):
    """
    :param array: the full array of data
    :param index: 0, 1, 2, for the index of the three values you want
    :return: array[2*index], array[2*index+1], array[2*index+2]
    :return: back, up, front values of triangle[index]
    """
    twindex = 2*index
    return array[twindex:twindex+3]


flat_45 = [
    VtVector((0.000, 0.000, 0.000)),  # back[0]
    VtVector((0.000, 0.000, 0.500)),  # up[0]
    VtVector((0.500, 0.000, 0.000)),  # front[0] = back[1]]
    VtVector((0.500, -0.354, 0.354)),  # up[1]
    VtVector((1.000, 0.000, 0.000)),   # front[1] = back[2]
    VtVector((1.000, -0.500, 0.000)),
    VtVector((1.500, 0.000, 0.000)),
    VtVector((1.500, -0.354, -0.354)),
    VtVector((2.000, 0.000, 0.000)),
    VtVector((2.000, 0.000, -0.500)),
    VtVector((2.500, 0.000, 0.000)),
    VtVector((2.500, 0.354, -0.354)),
    VtVector((3.000, 0.000, 0.000)),
    VtVector((3.000, 0.500, 0.000)),
    VtVector((3.500, 0.000, 0.000)),
    VtVector((3.500, 0.354, 0.354)),
    VtVector((4.000, 0.000, 0.000)),
    VtVector((4.000, 0.000, 0.500)),
    VtVector((4.500, 0.000, 0.000))]
tilt_45 = [
    VtVector((0.000, 0.000, 0.000)),
    VtVector((0.250, 0.000, 0.433)),
    VtVector((0.375, -0.250, -0.217)),
    VtVector((0.399, -0.556, 0.178)),
    VtVector((0.750, -0.500, -0.433)),
    VtVector((0.533, -0.933, -0.308)),
    VtVector((1.125, -0.750, -0.650)),
    VtVector((0.795, -1.056, -0.867)),
    VtVector((1.500, -1.000, -0.866)),
    VtVector((1.250, -1.000, -1.299)),
    VtVector((1.875, -1.250, -1.083)),
    VtVector((1.851, -0.944, -1.477)),
    VtVector((2.250, -1.500, -1.299)),
    VtVector((2.467, -1.067, -1.424)),
    VtVector((2.625, -1.750, -1.516)),
    VtVector((2.955, -1.444, -1.298)),
    VtVector((3.000, -2.000, -1.732)),
    VtVector((3.250, -2.000, -1.299)),
    VtVector((3.375, -2.250, -1.949))]

