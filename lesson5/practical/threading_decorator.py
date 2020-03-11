from threading import Thread, _counter, Event
import time


class MyOwnThread(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.args = args
        self.target = target
        self.group = group
        self.kwargs = kwargs

    def run(self):
        print(f'{self.getName()} started {self.target.__name__}{self.args}')
        super().run()
        print(f'{self.getName()} finished {self.target.__name__}{self.args}')


def my_own_decorator(thread_name, is_daemon=False):
    def actual_decorator(func):
        def wrapper(*args):

            thread = MyOwnThread(target=func, args=args, daemon=is_daemon, name=f'{thread_name}-{_counter()}')
            thread.start()

        return wrapper

    return actual_decorator


@my_own_decorator('my_own_func', is_daemon=True)
def my_func(*args):
    print(*args)
    time.sleep(3)


if __name__ == '__main__':
    my_func('print this')
    my_func('print this2')
