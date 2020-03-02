class Point:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z


    def __eq__(self, other):

        if (self.x == other.x and self.y == other.y and self.z == other.z):
            return True
        else:
            return False

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):

        if other.x * other.y * other.z == 0:
            raise ZeroDivisionError("None of the coordinates of the dividing point should be equal to 0")

        return Point(self.x / other.x, self.y / other.y, self.z / other.z)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'




point1 = Point(1, 2, 3)

print(-point1)
print(Point(3, 3, 3) * Point(0, 1, 2))
print(Point(3, 3, 3) + Point(0, 1, 2))
print(Point(3, 3, 3) - Point(0, 1, 2))
print(Point(3, 3, 3) / Point(1, 2, 3))
print(point1 * point1)

print(Point(3, 3, 3)/Point(0, 1, 2))