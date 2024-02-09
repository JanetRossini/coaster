from math import sin, cos

from v_vector import Vector

"""
Rodrigues Formula [1]:

v' = v + 2 * r x (s * v + r x v) / m

where x represents the cross product, s and r are the scalar and vector parts of the quaternion, respectively,
and m is the sum of the squares of the components of the quaternion.

Faster way:
https://blog.molecular-matters.com/2013/05/24/a-faster-quaternion-vector-multiplication/

t = 2 * cross(q.xyz, v)
v' = v + q.w * t + cross(q.xyz, t)  

Also from https://www.johndcook.com/blog/2021/06/16/faster-quaternion-rotations/
he found it on molecular-matters.com :)

Also found this python code:
https://github.com/KieranWynn/pyquaternion/blob/master/pyquaternion/quaternion.py
This code appears to be a good example of what is *really* necessary to
implement quaternions or any such data type robustly. 
Our implementation here is not robust, just enough to give us what we need.
Might use it for slerp.
"""


class Quaternion:
    """
    Minimal Quaternion, only supports quat@vector and little else.
    """
    def __init__(self, axis, angle):
        norm = axis.normalized()
        half = angle / 2
        sine = sin(half)
        self.x = norm.x*sine
        self.y = norm.y*sine
        self.z = norm.z*sine
        self.w = cos(half)

    @property
    def xyz(self):
        return Vector((self.x, self.y, self.z))

    def __matmul__(self, v):
        """
        t = 2 * cross(q.xyz, v)
        v' = v + q.w * t + cross(q.xyz, t)
        """
        assert isinstance(v, Vector)
        xyz = self.xyz
        t = 2 * xyz.cross(v)
        return v + self.w * t + xyz.cross(t)
