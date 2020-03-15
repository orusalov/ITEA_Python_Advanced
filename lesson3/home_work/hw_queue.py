""" from queue import Queue
implements some methods as in mentioned above class
"""


class PutError(Exception):
    pass


class OwnQueue:

    def __init__(self, maxsize=0):
        self.my_queue = []
        self.maxsize = maxsize

    def qsize(self):
        return len(self.my_queue)

    def empty(self):
        return not bool(self.my_queue)

    def full(self):
        return self.maxsize and self.qsize() == self.maxsize

    def put(self, item):
        if self.maxsize and self.full():
            raise PutError('You can''t put into queue more elements then maxsize')

        self.my_queue.append(item)

    def get(self):
        return self.my_queue.pop(0)

    def put_nowait(self, item):
        return self.put(item)

    def get_nowait(self):
        return self.get()

    def __str__(self):
        return str(self.my_queue)


queue = OwnQueue(4)

print(queue.empty())

try:
    for item in [3, 4, 5, 6, 1, 2]:
        queue.put(item)
except PutError as err:
    print(err)

print(queue.full())

print(queue)

print(queue.get())
print(queue)

print(queue.get())
print(queue)

queue.put('asdasd')
print(queue)

print(queue.get())
print(queue)

print(queue.qsize())
print(queue.empty())

print(queue.full())
