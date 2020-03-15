import hw_queue


class OwnStack(hw_queue.OwnQueue):

    def get(self):
        return self.my_queue.pop()


stack = OwnStack()

for item in [3, 4, 5, 6, 1, 2]:
    stack.put(item)

print(stack)

print(stack.get())
print(stack)

print(stack.get())
print(stack)

stack.put('asdasd')
print(stack)

print(stack.get())
print(stack)
