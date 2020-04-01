class CustomListIter:

    def __init__(self, cust_list):
        self._instance = cust_list
        self._iterator_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._iterator_index < len(self._instance):
            self._iterator_index += 1
            return self._instance[self._iterator_index - 1]

        self._iterator_index = 0
        raise StopIteration()


class CustomList:
    def __init__(self, *args):
        self._current_length = 0
        self._current_index_generator = self._indexing()
        self._cust_listt_attr_prefix = '_attr_cust_list_'
        for arg in args:
            self.__setitem__(None, arg)

    def pop(self, index=-1):

        return_value = self[index]
        del self[index]
        return return_value

    def append(self, object):
        self.__setitem__(None, object)

    def insert(self, index, object):
        idx_rng = range(len(self[index:]))
        self.append(object)
        for idx in idx_rng:
            self[-idx - 1], self[-idx - 2] = self[-idx - 2], self[-idx - 1]

    def remove(self, object):
        for i in range(len(self)):
            if self[i] == object:
                del self[i]
                break

    def clear(self):
        for i in range(len(self)):
            del self[-1]

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f'sum allowed only for two {self.__class__.__name__} instances')

        return_list = self[0:]

        for el in other:
            return_list.append(el)

        return return_list

    def __setitem__(self, index, value):
        if index is None:
            index = next(self._current_index_generator)

        if index < -len(self) or index > len(self) - 1:
            raise IndexError(f'{self.__class__.__name__} index out of range')
        elif index < 0:
            index = len(self) + index

        setattr(self, f'{self._cust_listt_attr_prefix}{index}', value)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._attr_slice(index.start, index.stop, index.step)

        if index < -len(self) or index > len(self) - 1:
            raise IndexError(f'{self.__class__.__name__} index out of range')
        elif index < 0:
            index = len(self) + index

        return getattr(self, f'{self._cust_listt_attr_prefix}{index}')

    def __delitem__(self, key):
        if key < -len(self) or key > len(self) - 1:
            raise IndexError(f'{self.__class__.__name__} index out of range')
        elif key < 0:
            key = len(self) + key

        k = key
        for atr in self[key + 1:]:
            self[k] = atr
            k += 1

        self._current_length -= 1
        delattr(self, f'{self._cust_listt_attr_prefix}{self._current_length}')

    def _indexing(self):
        while True:
            self._current_length += 1
            yield self._current_length - 1

    def __iter__(self):
        return CustomListIter(self)

    def _attr_slice(self, start, end, step):
        if step is None:
            step = 1
        elif step == 0:
            raise ValueError('slice step cannot be zero')

        return_val = CustomList()

        if step < 0:
            if start is None:
                current_index = len(self) - 1
            elif start < -len(self):
                return return_val
            elif start < 0:
                current_index = len(self) + start
            elif start >= len(self) - 1:
                current_index = len(self) - 1
            elif start >= 0:
                current_index = start

            if end is None:
                end = 0
            elif end < -len(self):
                end = 0
            elif end < 0:
                end = len(self) + end + 1
            elif end >= len(self) - 1:
                return return_val
            elif end >= 0:
                end = end + 1

            if end > current_index:
                return return_val

        elif step > 0:
            if start is None:
                current_index = 0
            elif start >= len(self):
                return return_val
            elif start >= 0:
                current_index = start
            elif start < -len(self):
                current_index = 0
            elif start < 0:
                current_index = len(self) + start

            if end is None:
                end = len(self) - 1
            elif end >= len(self):
                end = len(self) - 1
            elif end >= 0:
                end = end - 1
            elif end < -len(self):
                return return_val
            elif end < 0:
                end = len(self) + end - 1

            if end < current_index:
                return return_val

        low_marg = min(current_index, end)
        high_marg = max(current_index, end)

        while low_marg <= current_index <= high_marg:
            return_val.__setitem__(None, self[current_index])
            current_index += step

        return return_val

    def __len__(self):
        return self._current_length

    def __str__(self):
        list_str = CustomList()

        sign = "'"
        for val in self:
            list_str.append(f"{f'{sign}{val}{sign}' if isinstance(val, str) else str(val)}")
        els = ', '.join(list_str)
        return_str = f'{self.__class__.__name__}({els})'
        return return_str


if __name__ == '__main__':
    cust_list = CustomList('z', 'x', 'c', 'v', 'b')
    cust_list2 = CustomList('a', 'b', 'c', 'd')

    lis = ['z', 'x', 'c', 'v', 'b']
    lis2 = ['a', 'b', 'c', 'd']

    print(cust_list)
    print(lis)

    cL3 = cust_list + cust_list2
    print(cL3)
    print(lis + lis2)
    cL3.append('qwe')
    print(cL3)
    cL3.remove('b')
    print(cL3)
    cL3.insert(3, 'qqq')
    print(cL3)
    cL3.insert(-3, 'zzzz')
    print(cL3)
    print(cL3.pop())
    print(cL3)
    print(cL3.pop(-6))
    print(cL3)
    print(cL3.pop(1))
    print(cL3)
    print(cL3[1],cL3[-4])
    print(cL3[::-2])
    print(cL3[1:100])
    print(cL3.clear())
    print(cL3)
    print(cL3[0])

