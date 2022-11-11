from itertools import combinations

import numpy as np

from objects.functions import sum_costs


class Airline:

    def __init__(self, name):
        self.name = name
        self.initial_costs = None
        self.final_costs = None
        self.reduction = None
        self.reduction_percentage = None
        self.flights = []
        self.flights_couples = []
        self.flights_triples = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def compute_costs(self):
        self.initial_costs = sum_costs(self.flights)
        self.final_costs = sum_costs(self.flights, False)
        self.reduction = self.final_costs - self.initial_costs
        self.reduction_percentage = self.reduction / self.initial_costs

    def make_flights_comb(self, number):
        if number == 2:
            # self.flights_couples = np.array(list(combinations(self.flights, number)))
            for i in range(len(self.flights)):
                for j in range(i + 1, len(self.flights)):
                    max_points = max(self.flights[i].earlier_points + self.flights[j].later_points,
                                     self.flights[i].later_points + self.flights[j].earlier_points)
                    #if max_points > 10 and abs(self.flights[i].index - self.flights[j].index) < 30:
                    if True:
                        self.flights_couples.append((self.flights[i], self.flights[j]))
        elif number == 3:
            self.flights_triples = np.array(list(combinations(self.flights, number)))
