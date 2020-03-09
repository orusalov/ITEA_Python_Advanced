class OwnStack:

    def __init__(self):
        self.my_stack = []

    def push(self, *args):
        self.my_stack.extend(args)

    def pop(self):
        return self.my_stack.pop()

    def __str__(self):
        return str(list(reversed(self.my_stack)))


stack = OwnStack()
stack.push(3, 4, 5, 6, 1, 2)
print(stack)

print(stack.pop())
print(stack)

print(stack.pop())
print(stack)

stack.push('asdasd')
print(stack)

print(stack.pop())
print(stack)
