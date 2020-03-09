class ComplexNumbers:

    def __init__(self, rational=0, irrational=0):
        self.rational = rational
        self.irrational = irrational

    def __str__(self):
        return f'{self.rational} {"-" if self.irrational < 0 else "+"} {f"abs(self.irrational)i if self.irrational !=0"}'


cn = ComplexNumbers(1,-1)
print(cn)
