class Phone:

    __mobile_type = 'Common Phone'


    def __init__(self, model, imei, mobile_type):

        self.model = model
        self.imei = imei
        self.__mobile_type = mobile_type


    def call(self, to):

        print(f"OK, I'm calling {to} from {self.model}")




class Mobile_Phone(Phone):

    def deliver_sm(self, message, to):

        print(f"OK, I'm sending message {message} to {to}")




class SatelitePhone(Phone):

    def call(self, satelite_coordinates, to):
        print(f'Calling {to} from {self.model} satelite: {satelite_coordinates}')


class Application:

    def __init__(self, name):
        self._name = name

    def start(self):
        print(f'application {self._name} started')


class SmartPhone(Mobile_Phone):

    def play_audio(self):
        print('played audio')

    def play_video(self):
        print('played video')

    def start_application(self, application_object):
        application_object.start()

phone1 = Phone('Siemens', '297590824375982347509847','first')
phone2 = Mobile_Phone('Siemens', '297590824375982347509847','kajshdd')

phone2.deliver_sm('1234','+380632103807')

satelite_phone = SatelitePhone('saturn','132412341234', 'sdfssdfgsdgf')

satelite_phone.call('23423.23,123123.123', '+380632103779')

