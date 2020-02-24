N = int(input('Insert N: '))

my_list = list(range(N))

for i in my_list:

    # 0 not even
    if not (i % 2 or i == 0) :
        print(i)
