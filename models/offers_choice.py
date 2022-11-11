import gurobipy as gb
import numpy as np
from gurobipy import GRB, quicksum


class OffersChoice:

    def __init__(self, offers_list):
        self.p = gb.Model()
        self.p.modelSense = GRB.MAXIMIZE
        self.offers = offers_list
        self.num_offers = len(self.offers)
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addMVar((self.num_offers,), vtype=GRB.BINARY)
        self.M = np.zeros((self.num_offers, self.num_offers))
        for i in range(self.num_offers):
            for j in range(i):
                self.M[i, j] = self.M[j, i] = self.offers[i].is_incompatible_with(self.offers[j])
        self.ones = np.ones(self.num_offers)

    def set_constraints(self):
        self.p.addConstr(self.M @ self.x <= (self.ones - self.x) * self.num_offers, name="c")

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.offers[i].cost_reduction * self.x[i] for i in range(self.num_offers)))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()
        print("objVal: ", self.p.ObjVal)
        print("Optimal offers: ")
        for i in range(self.num_offers):
            if round(self.x[i].x) == 1:
                print(self.offers[i], self.offers[i].cost_reduction, "implies:")
                for j in range(len(self.offers[i].flights_both)):
                    print("The flight ", self.offers[i].flights_both[j], "(points earlier-later",
                          self.offers[i].flights_both[j].earlier_points, self.offers[i].flights_both[j].later_points,
                          ")",
                          " is switched with index", self.offers[i].new_indexes[j])
