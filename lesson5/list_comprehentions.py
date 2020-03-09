import time

result_list = []

start_time = time.time()
for i in range(100000):
    result_list.append(i)
end_loop = time.time() - start_time


start_compr = time.time()
result_list_2 = [i for i in range(100000) if not i % 2]

end_compr = time.time() - start_compr

print(end_loop, end_compr)

a = [1, 2, 3, 4]
b = [5, 6, 7, 8]

result_dict = {k:v for k, v in zip(a, b)}
print(result_dict)


