from enum import Enum


class Impacts(Enum):
    PHYSICAL = 'Physical'
    MENTAL = 'Mental'
    ENERGY = 'Energy'
    HEAT = 'Heat'
    COLD = 'Cold'
    LIGHT = 'Light'
    DARKNESS = 'Darkness'

    def to_django_choice(self):
        return self.value, self.name

    @classmethod
    def choices(cls):
        return [impact.to_django_choice() for impact in cls]

    def __str__(self):
        return self.value
