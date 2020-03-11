import time
from threading import  Thread
from multiprocessing import Process

def sleeping(time_to_sleep):
    time.sleep(time_to_sleep)
    print('I woke up')


# start = time.time()
# sleeping(2)
# sleeping(3)
#
# print(time.time() - start)
#
#
# t = Thread(target=sleeping, args=(2,))
# t2 = Thread(target=sleeping, args=(3,))
#
# start = time.time()
#
# t.start()
# t2.start()
# t.join()
# t2.join()
#
# print(time.time() - start)


def calculate(n):

    a  = []
    for i in range(n):
        a.append(i)


start = time.time()

calculate(100000)
calculate(100000)

print(time.time() - start)



t = Thread(target=calculate, args=(1000000,))
t2 = Thread(target=calculate, args=(1000000,))

start = time.time()

t.start()
t2.start()

print(t.is_alive())
print(t.getName())

t.join()
t2.join()

print(time.time() - start)

# t = Process(target=calculate, args=(100000,))
# t2 = Process(target=calculate, args=(100000,))
#
# start = time.time()
#
# t.start()
# t2.start()
# t.join()
# t2.join()
#
# print(time.time() - start)


a = []
def calculate(i):
    global a
    a.append(i)

list_of_threads = [Thread(target=calculate, args = (i,)) for i in range(10000)]

for thread in list_of_threads:
    thread.start()

time.sleep(1)

print(a)

