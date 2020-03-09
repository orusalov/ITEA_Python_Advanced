class OwnQueue:

    def __init__(self):
        self.my_queue = []

    def enqueue(self, *args):
        self.my_queue.extend(args)

    def dequeue(self):
        return self.my_queue.pop(0)

    def __str__(self):
        return str(self.my_queue)


queue = OwnQueue()
queue.enqueue(3, 4, 5, 6, 1, 2)
print(queue)

print(queue.dequeue())
print(queue)

print(queue.dequeue())
print(queue)

queue.enqueue('asdasd')
print(queue)

print(queue.dequeue())
print(queue)
