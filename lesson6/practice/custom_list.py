class CustomList:
    def __init__(self, *args):
        self._current_length, self._iterator_index = 0, 0
        self._current_index_generator = self._indexing()
        for arg in args:
            self.__setitem__(None, arg)

    def pop(self):

        return_value = self[-1]
        del self[-1]
        return return_value

    def append(self, value):
        self.__setitem__(None, value)

    def insert(self, index):
        for atr in self[index::-1]:
            pass


    def remove(self):
        pass

    def clear(self):
        pass

    def __setitem__(self, index, value):
        if index is None:
            index = next(self._current_index_generator)

        setattr(self, f'_attr_{index}', value)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._attr_slice(index.start,index.stop,index.step)

        if -self._current_length <= index < 0:
            index = self._current_length + index
        elif index < 0:
            raise IndexError('CustomList index out of range')

        return getattr(self, f'_attr_{index}')

    def _indexing(self):
        while True:
            self._current_length += 1
            yield self._current_length - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._iterator_index < self._current_length:
            self._iterator_index += 1
            return self[self._iterator_index - 1]

        self._iterator_index = 0
        raise StopIteration()

    def _attr_slice(self, start, end, step):
        if step < 0:
            current_index = -1 if not start else start
            end = -self._current_length - 1 if not end else end
        elif step > 0:
            current_index = 0 if not start else start
            end = self._current_length - 1 if not end else end

        step = 1 if not step else step

        if current_index < 0:
            current_index = self._current_length + current_index

        if end < 0:
            end = self._current_length + end

        return_val = CustomList()

        if end > current_index:
            low_marg = current_index
            high_marg = end - 1
        elif end < current_index:
            low_marg = end + 1
            high_marg = current_index
        else:
            return return_val

        low_marg = 0 if low_marg < 0 else low_marg
        high_marg = len(self) - 1 if high_marg >= len(self) else high_marg


        while low_marg <= current_index <= high_marg:
            return_val.__setitem__(None,self[current_index])
            current_index += step

        return return_val

    def __delitem__(self, key):
        if -self._current_length <= key < 0:
            key = self._current_length + key
        elif key < 0:
            raise IndexError('CustomList index out of range')

        k = key
        for atr in self[key + 1:]:
            self[k] = atr
            k += 1

        self._current_length -= 1
        delattr(self, f'_attr_{self._current_length}')

    def __len__(self):
        return self._current_length

    def __str__(self):
        els = ', '.join(self)
        return_str = f'{self.__class__.__name__}({els})'
        return return_str




cust_list = CustomList('z','x','c', 'v')

print(cust_list)

for atr in cust_list:
    print(atr)

cl1 = cust_list[-10::-1]

print(cl1)

for atr in cl1:
    print(atr)

#
# print(cust_list[-2])
#
# del cust_list[1]
#
# for atr in cust_list:
#     print(atr)

lis = ['q','w','e','r','t','y']
del lis[4:]
print(lis)

print(lis[7:9])