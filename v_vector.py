from math import sqrt


class Vector:
    def __init__(self, seq):
        self.seq = tuple(seq)
        if len(self.seq) != 3:
            raise TypeError('only 3D Vectors supported.')

    def __repr__(self):
        return f"v_Vector({self.seq})"

    def __eq__(self, vector):
        return self.seq == vector.seq

    def __add__(self, vector):
        s_seq = self.seq
        v_seq = vector.seq
        top_range = range(0, max(len(s_seq), len(v_seq)))
        seq = (s_seq[i] + v_seq[i] for i in top_range)
        return Vector(seq)

    def __neg__(self):
        seq = (-c for c in self.seq)
        return Vector(seq)

    def __sub__(self, vector):
        return self + -vector

    def __mul__(self, scalar):  # self * scalar
        seq = (scalar * coord for coord in self.seq)
        return Vector(seq)

    def __rmul__(self, scalar):  # scalar * self
        return self*scalar

    @property
    def x(self):
        return self.seq[0]

    @property
    def y(self):
        return self.seq[1]

    @property
    def z(self):
        return self.seq[2]

    @property
    def length(self):
        x = self.x
        y = self.y
        z = self.z
        return sqrt(x*x + y*y + z*z)

    def normalized(self):
        length = self.length
        return Vector((self.x/length, self.y/length, self.z/length))

    def cross(self, b):
        ax, ay, az = self.seq
        bx, by, bz = b.seq
        cx = ay*bz - az*by
        cy = az*bx - ax*bz
        cz = ax*by - ay*bx
        return Vector((cx, cy, cz))

