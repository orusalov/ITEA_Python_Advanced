import abc

class MyMetaClass(type):
    def __new__(mcls, name, base, attrs):
        print(mcls, name, base, attrs)
        return super().__new__(mcls, name, base, attrs)


class ClassName(metaclass=MyMetaClass):
    """docstring for ClassName"""
    print(123)
    def __init__(self, arg):
        self.arg = arg

print(ClassName)