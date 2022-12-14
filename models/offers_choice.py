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
        self.sol = None

    def set_constraints(self):
        self.p.addConstr(self.M @ self.x <= (self.ones - self.x) * self.num_offers, name="c")

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.offers[i].cost_reduction * self.x[i] for i in range(self.num_offers)))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()
        self.sol = self.p.ObjVal
        print("objVal: ", self.sol)
        print("Optimal offers: ")
        for i in range(self.num_offers):
            if round(self.x[i].x) == 1:
                self.offers[i].select_couples()
                print(self.offers[i], "has a cost reduction of", self.offers[i].cost_reduction)
                self.offers[i].show_offer()
