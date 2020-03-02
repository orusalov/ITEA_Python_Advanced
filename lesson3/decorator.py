"""Создать декоратор с аргументами. Который будет вызывать функцию,
определенное кол-во раз, будет выводить кол-во времени
затраченного на выполнение данной функции и её название."""
from time import time
from random import randint


def my_own_decorator(call_number=1):

    def actual_decorator(func):

        def wrapper(*args):

            result = []

            for i in range(call_number):

                initial_time = time()
                result.append(func())
                time_execute = time() - initial_time
                print(f'Function {func.__name__}() executed {i+1} time in {time_execute}')

            return result

        return wrapper

    return actual_decorator


@my_own_decorator(5)
def hi_my_func():

    print("hi")
    return randint(1,100)


print(hi_my_func())