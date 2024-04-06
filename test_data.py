from mathutils import Vector


# all real code should now use mathutils
# this test checks the JR objects, which should no longer be needed.
# from mathutils import Vector - use this
# from v_vector import Vector - not this
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
    Vector((0.000,0.000,0.000)),  # back[0]
    Vector((0.000,0.000,0.500)),  # up[0]
    Vector((0.500,0.000,0.000)),  # front[0] = back[1]]
    Vector((0.500,-0.354,0.354)),  # up[1]
    Vector((1.000,0.000,0.000)),   # front[1] = back[2]
    Vector((1.000,-0.500,0.000)),
    Vector((1.500,0.000,0.000)),
    Vector((1.500,-0.354,-0.354)),
    Vector((2.000,0.000,0.000)),
    Vector((2.000,0.000,-0.500)),
    Vector((2.500,0.000,0.000)),
    Vector((2.500,0.354,-0.354)),
    Vector((3.000,0.000,0.000)),
    Vector((3.000,0.500,0.000)),
    Vector((3.500,0.000,0.000)),
    Vector((3.500,0.354,0.354)),
    Vector((4.000,0.000,0.000)),
    Vector((4.000,0.000,0.500)),
    Vector((4.500,0.000,0.000))]
tilt_45 = [
    Vector((0.000,0.000,0.000)),
    Vector((0.250,0.000,0.433)),
    Vector((0.375,-0.250,-0.217)),
    Vector((0.399,-0.556,0.178)),
    Vector((0.750,-0.500,-0.433)),
    Vector((0.533,-0.933,-0.308)),
    Vector((1.125,-0.750,-0.650)),
    Vector((0.795,-1.056,-0.867)),
    Vector((1.500,-1.000,-0.866)),
    Vector((1.250,-1.000,-1.299)),
    Vector((1.875,-1.250,-1.083)),
    Vector((1.851,-0.944,-1.477)),
    Vector((2.250,-1.500,-1.299)),
    Vector((2.467,-1.067,-1.424)),
    Vector((2.625,-1.750,-1.516)),
    Vector((2.955,-1.444,-1.298)),
    Vector((3.000,-2.000,-1.732)),
    Vector((3.250,-2.000,-1.299)),
    Vector((3.375,-2.250,-1.949))]

