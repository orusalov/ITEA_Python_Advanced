import mongoengine as me
me.connect('Tickets')


class Passenger(me.Document):
    name = me.StringField(min_length=1)
    surname = me.StringField(min_length=1)
    trip = me.ReferenceField('Trip') # Можно передавать класс строкой, так как Монго сам поймет к какому классу обратитсья

    def __str__(self):
        return f'{self.name}'


class Bus(me.Document):
    model_ = me.StringField(min_length=1)
    seats = me.IntField(min_value=4)

    def __str__(self):
        return f'{self.model}'


class Trip(me.Document):
    destination = me.StringField(min_length=2, max_length=512)
    price = me.FloatField(min_value=0)
    bus = me.ReferenceField(Bus)

    @property
    def bus_model(self):
        return self.bus.model

    def get_passengers(self):
        return Passenger.objects(trip=self)

    def __str__(self):
        return f'{self.destination}'


if __name__ == '__main__':

    bus = Bus(model_='BMW', seats=14).save()

    trip = Trip(destination='USA', price=1000,bus=bus).save()

    ps = Passenger(
        name='John',
        surname='Doe',
        trip=trip
    ).save()