class Dec:

    def __init__(self, func):

        self.f = func

    def __call__(self, *args, **kwargs):
        print(f'wrapping function {self.f.__name__}')
        self.f()



@Dec
def test():
    print('hello')


test()