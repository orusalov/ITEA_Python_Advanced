class Phone:

    mobile_type = 'Common Phone'


    def __init__(self, model, imei):

        self.model = model
        self.imei = imei
        print(self.mobile_type)


    def call(self, to):

        print(f"OK, I'm calling {to} from {self.model}")



phone = Phone('Nokia', '097230947029387409872314')

print(phone.mobile_type)
phone.call('+380632103807')

phone.mobile_type = 'Not common'
print(phone.mobile_type)

phone2 = Phone('Siemens', '297590824375982347509847')
phone2.call('+380632103779')
print(phone2.mobile_type)
print(Phone.mobile_type)
Phone.mobile_type = 'lkjaslkdjalksjd'
print(Phone.mobile_type)