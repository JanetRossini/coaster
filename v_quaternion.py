from math import sin, cos, acos, sqrt
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
    Minimal Quaternion.
    Supports:
        -q1 (__neg__
        q1 + q2 (__add__)
        q1 - q2 (__sub__)
        scalar*q1 (__mul++ and __rmul__)
        q1*scalar
        q1 @ vector ( __matmul__)
    """
    def __init__(self, *args):
        if len(args) == 4:
            self.w = args[0]
            self.x = args[1]
            self.y = args[2]
            self.z = args[3]
        elif len(args) == 2:
            axis = args[0]
            angle = args[1]
            norm = axis.normalized()
            half = angle / 2
            sine = sin(half)
            self.x = norm.x*sine
            self.y = norm.y*sine
            self.z = norm.z*sine
            self.w = cos(half)
        elif len(args) == 1 and isinstance(args[0], Quaternion):
            q = args[0]
            self.w = q.w
            self.x = q.x
            self.y = q.y
            self.z = q.z
        else:
            raise TypeError("Object cannot be initialized from {}".format(args))

    @property
    def xyz(self):
        return Vector((self.x, self.y, self.z))

    def __add__(self, q):
        return Quaternion(self.w+q.w, self.x+q.x, self.y+q.y, self.z+q.z)

    def __neg__(self):
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __sub__(self, q):
        return self + (-q)

    def __mul__(self, scalar):
        return Quaternion(scalar * self.w, scalar * self.x, scalar * self.y, scalar * self.z)

    def __rmul__(self, scalar):
        return self*scalar

    def __matmul__(self, v):
        """
        t = 2 * cross(q.xyz, v)
        v' = v + q.w * t + cross(q.xyz, t)
        """
        if not isinstance(v, Vector):
            raise TypeError("Quaternion @ requires vector as second argument")
        xyz = self.xyz
        t = 2 * xyz.cross(v)
        return v + self.w * t + xyz.cross(t)

    def __repr__(self):
        return f"Quaternion({self.w:.3f}, {self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def _is_unit(self, tolerance=1E-14):
        return (1 - self._sum_of_squares()) < tolerance

    def _sum_of_squares(self):
        w, x, y, z = self.w, self.x, self.y, self.z
        sum_sq = w * w + x * x + y * y + z * z
        return sum_sq

    @property
    def _norm(self):
        return sqrt(self._sum_of_squares())

    def normalized(self):
        if self._is_unit():
            return self
        norm = self._norm
        inverse = 1.0/norm
        return inverse*self

    def dot(self,q):
        return self.w*q.w + self.x*q.x + self.y*q.y + self.z*q.z

    def slerp(self, other, frac):
        """
        Interpolate linearly between self and q2.
        Adapted from https://github.com/KieranWynn/pyquaternion/blob/master/pyquaternion/quaternion.py
        :param other: Quaternion
        :param frac: 0 <= frac <= 1
        :return: quaternion interpolated between self and q2

        theta = angle between q0 and q1
        num = q0*sin((1-t)*theta) + q1*sin(t*theta)
        den = sin(theta)
        slerp(q0, q1, t) = num/den

        where theta = acos(q0.dot(q1))
        But if dot > 0.9995: special deal untested
        """
        q0 = self.normalized()
        q1 = other.normalized()
        frac = min(max(frac, 0), 1)
        dot = q0.dot(q1)
        if dot < 0:
            q0 = -1*q0
            dot = -dot
        if dot > 0.9995:
            # UNTESTED!!
            qr = Quaternion(q0 + frac * (q1 - q0)).normalized()
            return qr
        theta_0 = acos(dot)
        sin_theta_0 = sin(theta_0)
        theta = theta_0*frac
        sin_theta = sin(theta)
        s0 = cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0
        qa = s0*q0
        qb = s1*q1
        qr = Quaternion(qa + qb).normalized()
        return qr


