class ComplexNumbers:

    def __init__(self, rational=0, irrational=0):
        self.rational = rational
        self.irrational = irrational

    def __str__(self):
        return f'{self.rational} {"-" if self.irrational < 0 else "+"} \
{str(abs(self.irrational))+"i" if self.irrational !=0 else None}'

    def __pos__(self):
        return self

    def __neg__(self):
        return ComplexNumbers(-self.rational, -self.irrational)

    def __add__(self, other):

        if isinstance(other, (int, float)):
            return ComplexNumbers(self.rational + other, self.irrational)
        elif isinstance(other, ComplexNumbers):
            return ComplexNumbers(self.rational + other.rational, self.irrational + other.irrational)
        else:
            raise TypeError('expected int, float or ComplexNumbers')

    def __sub__(self, other):

        if isinstance(other, (int, float)):
            return ComplexNumbers(self.rational - other, self.irrational)
        elif isinstance(other, ComplexNumbers):
            return ComplexNumbers(self.rational - other.rational, self.irrational - other.irrational)
        else:
            raise TypeError('expected int, float or ComplexNumbers')

    def __mul__(self, other):

        if isinstance(other, (int, float)):
            return ComplexNumbers(self.rational * other, self.irrational * other)
        elif isinstance(other, ComplexNumbers):
            return ComplexNumbers(self.rational * other.rational - self.irrational * other.irrational,
                                  self.rational * other.irrational + self.irrational * other.rational)
        else:
            raise TypeError('expected int, float or ComplexNumbers')

    def __truediv__(self, other):

        if isinstance(other, (int, float)):
            return ComplexNumbers(self.rational / other, self.irrational / other)
        elif isinstance(other, ComplexNumbers):
            mul = self * ComplexNumbers(other.rational, -other.irrational)
            div = other.irrational ** 2 + other.irrational ** 2
            return mul / div
        else:
            raise TypeError('expected int, float or ComplexNumbers')

    def __pow__(self, power, modulo=None):

        result = self
        for _ in range(power):
            result *= self

        return result



print(ComplexNumbers(5, 7) + 2)
print(ComplexNumbers(5, 7) + 2.5)
print(ComplexNumbers(5, 7) + ComplexNumbers(3, 9))
print(ComplexNumbers(5, 7) - 2)
print(ComplexNumbers(5, 7) - 2.5)
print(ComplexNumbers(5, 7) - ComplexNumbers(3, 9))
print(ComplexNumbers(5, 7) * 2)
print(ComplexNumbers(5, 7) * 2.5)
print(ComplexNumbers(5, 7) * ComplexNumbers(3, 9))
print(ComplexNumbers(5, 7) / 2)
print(ComplexNumbers(5, 7) / 2.5)
print(ComplexNumbers(5, 7) / ComplexNumbers(3, 9))
print(-ComplexNumbers(5, 7))
print(+ComplexNumbers(5, 7))
print(ComplexNumbers(5, 7) ** 3)
