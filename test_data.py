from mathutils import Vector


def fetch(array, index):
    # utility function to fetch data from array
    twindex = 2*index
    return array[twindex:twindex+3]
    # return array[twindex], array[twindex+1], array[twindex+3]


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
    Vector((4.500,0.000,0.000)),]
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
    Vector((3.375,-2.250,-1.949)),]

