class FacebookAuth:

    api_url = 'facebook.com/'

    def __init__(self, login, password):
        self._login = login
        self._password = password

    def __call__(self, *args, **kwargs):
        print('Object has been called')

    @staticmethod
    def validate(login, password):
        print(login, password)

    @classmethod
    def validate1(cls, login, password):
        print(cls.api_url)
        print(login, password)
    

FacebookAuth.validate('orusalov', 'orpass')



fb = FacebookAuth('zxc', 'qwe')

fb()