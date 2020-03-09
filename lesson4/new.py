class Point:
    def __new__(cls, *args, **kwargs):
        point_obj = super().__new__(cls)
        point_obj._x = args[0]
        return point_obj

    def __init__(self, z):

        self._z = z

p = Point(1)

print(p._x)
print(p._z)