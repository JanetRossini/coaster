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
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalized(self):
        norm = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return Vector((self.x/norm, self.y/norm, self.z/norm))
