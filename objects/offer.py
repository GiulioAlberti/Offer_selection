import numpy as np

from objects.airline import Airline


class Offer:

    def __init__(self, number, airline_a: Airline, airline_b: Airline, a_couple, b_couple):
        self.name = str(number) + airline_a.name + airline_b.name
        self.airline_a = airline_a
        self.airline_b = airline_b
        self.a_couple = a_couple
        self.b_couple = b_couple

        self.flights_a = np.array([a_couple.fl_one, a_couple.fl_two])
        self.flights_b = np.array([b_couple.fl_one, b_couple.fl_two])
        self.indexes_a = np.array([flight.index for flight in self.flights_a])
        self.indexes_b = np.array([flight.index for flight in self.flights_b])
        self.flights_both = np.concatenate((self.flights_a, self.flights_b))
        self.indexes_both = np.concatenate((self.indexes_a, self.indexes_b))
        self.cost_reduction = None
        self.new_indexes = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def is_incompatible_with(self, other_offer):
        output = 0
        for flight in self.flights_both:
            if flight in other_offer.flights_both:
                output = 1
        return output

    def set_cost_reduction(self, value):
        self.cost_reduction = value

    def select_couples(self):
        self.a_couple.select_in_solution()
        self.b_couple.select_in_solution()
