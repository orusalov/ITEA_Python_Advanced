from custom_list import CustomList


class CustomDictionary:
    def __init__(self, *args, **kwargs):
        self._current_length = 0
        self._cust_dict_attr_prefix = '_attr_cust_dict_'
        for arg in args:
            self.__setitem__(arg[0], arg[1])
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def items(self):
        dict_items = CustomList()
        for attr in dir(self):
            if attr.startswith(self._cust_dict_attr_prefix):
                key, val = getattr(self, attr)
                dict_items.append((key, val))

        return dict_items

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def keys(self):
        dict_items = CustomList()
        for key, val in self.items():
            dict_items.append(key)

        return dict_items

    def values(self):
        dict_items = CustomList()
        for key, val in self.items():
            dict_items.append(val)

        return dict_items

    def copy(self):
        return_dict = CustomDictionary()
        for k, v in self.items():
            return_dict[k] = v

        return return_dict

    def __add__(self, other):
        return_dict = self.copy()
        for k, v in other.items():
            return_dict[k] = v

        return return_dict

    def __setitem__(self, key, value):
        if key is None:
            raise KeyError(f'{self.__class__.__name__} key should not be None')

        if not hasattr(key, '__hash__'):
            raise TypeError(f'unhashable type: {type(key).__name__}')

        setattr(self, f'{self._cust_dict_attr_prefix}{key.__hash__()}', (key, value))
        self._current_length += 1

    def __getitem__(self, key):
        if key is None:
            raise KeyError(f'{self.__class__.__name__} key should not be None')

        if not hasattr(key, '__hash__'):
            raise TypeError(f'unhashable type: {type(key).__name__}')

        if hasattr(self, f'{self._cust_dict_attr_prefix}{key.__hash__()}'):
            attr = getattr(self, f'{self._cust_dict_attr_prefix}{key.__hash__()}')
        else:
            attr = None

        if attr is None or attr[0] != key:
            raise KeyError(f'{self.__class__.__name__} key {key} not found')
        if attr[0] == key:
            return attr[1]

    def __delitem__(self, key):

        atr = self[key]  # Just for raising exceptions from getitem

        delattr(self, f'{self._cust_dict_attr_prefix}{key.__hash__()}')
        self._current_length -= 1

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return self._current_length

    def __str__(self):
        dict_attrs = CustomList()
        for item in self.items():
            dict_attrs.append(str(item))

        els = ', '.join(dict_attrs)
        return_str = f'{self.__class__.__name__}({els})'
        return return_str


if __name__ == '__main__':
    cust_dict = CustomDictionary((1, 'qwe'), ('qwer', 4), new_one=435345)
    cust_dict2 = CustomDictionary(('new_one', 'last'), (234234, 'sdfsd'))
    v3 = cust_dict.get('asdasd')
    print(v3)

    print(cust_dict + cust_dict2)
    print((cust_dict + cust_dict2).items())
    print((cust_dict + cust_dict2).keys())
    print((cust_dict + cust_dict2).values())
