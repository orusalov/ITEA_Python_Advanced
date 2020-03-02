for i in range(1,101):

    return_val = ''

    if not i % 3:
        return_val += 'Fizz'

    if not i % 5:
        return_val += 'Buzz'

    if not return_val:
        return_val = i

    print(return_val)
