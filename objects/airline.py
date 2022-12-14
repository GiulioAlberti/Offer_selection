from itertools import combinations

import numpy as np

from models.localoptim import LocalOptim
from objects.flights_couple import FlightsCouple
from utils.functions import sum_costs


class Airline:

    def __init__(self, name):
        self.name = name
        self.initial_costs = None
        self.final_costs = None
        self.reduction = None
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

    def make_flights_comb(self, number, cut):
        self.flights_couples = []
        self.flights_triples = []
        if number == 2:
            for i in range(len(self.flights)):
                for j in range(i + 1, len(self.flights)):
                    max_points = max(self.flights[i].earlier_points + self.flights[j].later_points,
                                     self.flights[i].later_points + self.flights[j].earlier_points)
                    if cut:
                        if max_points > 0:
                            self.flights_couples.append(FlightsCouple(self.flights[i], self.flights[j], max_points))
                    else:
                        self.flights_couples.append(FlightsCouple(self.flights[i], self.flights[j], max_points))

        elif number == 3:
            self.flights_triples = np.array(list(combinations(self.flights, number)))

    def optimise_own_flights(self):
        lo = LocalOptim(self.flights)
        lo.solve()
