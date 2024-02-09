from math import sqrt


class Vector:
    def __init__(self, seq):
        self.seq = seq

    def __repr__(self):
        return f"Vector({self.seq})"

    def __eq__(self, other):
        return self.seq == other.seq

    def __getitem__(self, item):
        return self.seq[item]

    def __add__(self, other):
        top_range = range(0, max(len(self.seq), len(other.seq)))
        seq = tuple(self[i] + other[i] for i in top_range)
        return Vector(seq)

    def __neg__(self):
        seq = tuple(-c for c in self.seq)
        return Vector(seq)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        seq = tuple(other*coord for coord in self.seq)
        return Vector(seq)

    def __rmul__(self, other):
        return self*other

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
        norm = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return Vector((self.x/norm, self.y/norm, self.z/norm))

    def cross(self, other):
        a1, a2, a3 = self.seq
        b1, b2, b3 = other.seq
        c1 = a2*b3 - a3*b2
        c2 = a3*b1 - a1*b3
        c3 = a1*b2 - a2*b1
        return Vector((c1, c2, c3))

