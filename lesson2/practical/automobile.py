class Car:
    def __init__(self, year, make, acceleration_speed):
        self.__year_model = year
        self.__make = make
        self.speed = 0
        self.__acceleration_speed = acceleration_speed

    def set_year_model(self, year):
        self.__year_model = year

    def set_make(self, make):
        self.__make = make

    def get_year_model(self):
        return self.__year_model

    def get_make(self):
        return self.__make

    def get_speed(self):
        return self.speed

    #methods
    def accelerate(self):
        self.speed += self.__acceleration_speed

    def brake(self):
        self.speed -= self.__acceleration_speed

    def get_speed(self):
        return self.speed


class Sedan(Car):

    def __init__(self, year, make, is_electro):
        super().__init__( year, make, 10)

        self._is_electro = is_electro


class Truck(Car):

    initial_acceleration = 5

    def __init__(self, year, make, weight):
        super().__init__(year, make, self.initial_acceleration)
        self.loaded = False
        self.__initial_weight = weight
        self.weight = self.__initial_weight

    def load_truck(self):
        self.loaded = True
        self.weight = 100500

    def unload_truck(self):
        self.loaded = False
        self.weight = self.__initial_weight

    def brake(self):
        if self.loaded:
            self.speed -= self.initial_acceleration/2
        else:
            super().brake()


truck = Truck(2005, 'IVECO', 560)
truck.accelerate()
truck.accelerate()
print(truck.get_speed())
truck.brake()
print(truck.get_speed())
truck.load_truck()
truck.brake()
print(truck.get_speed())
