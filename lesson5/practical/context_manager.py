class MyOwnContextManager:

    def __init__(self, filename, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
        self.dict_with_ad_params = {
            'file': filename,
            'mode': mode,
            'buffering': buffering,
            'encoding': encoding,
            'errors': errors,
            'newline': newline,
            'closefd': closefd
        }
        self.dict_with_ad_params = dict(filter(lambda item: item[1] is not None, self.dict_with_ad_params.items()))

    def __enter__(self):
        self.file = open(
            **self.dict_with_ad_params
        )
        return self.file

    def __exit__(self, *args):
        self.file.close()


try:
    with MyOwnContextManager(filename='qwe123', mode='w') as f:
        f.write('line for us')
        f.write('asdasdasda', 234234)
except TypeError:
    f.write('zxczxczxczx')
    f.close()
