import gurobipy as gb
from gurobipy import GRB, quicksum


# nel caso di quadratic, sostituire costVect con NormCostVect
class OfferEval:

    def __init__(self, offer, new_slot_times):
        self.p = gb.Model()
        self.p.modelSense = GRB.MINIMIZE
        self.offer = offer
        self.eps = 0.01
        self.indexes = offer.indexes_both
        self.new_slot_times = new_slot_times
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addVars([(i, j) for i in self.indexes for j in self.indexes], vtype=GRB.BINARY)

    def set_constraints(self):
        for i in self.indexes:
            self.p.addConstr(quicksum(self.x[i, j] for j in self.indexes) == 1, name="c1[%s]" % i)
            self.p.addConstr(quicksum(self.x[j, i] for j in self.indexes) == 1, name="c2[%s]" % i)
        for i in self.indexes:  # elim same place
            self.p.addConstr(self.x[i, i] == 0, name="ce[%s]" % i)
        for flight in self.offer.flights_both:
            self.p.addConstr(quicksum(
                self.x[flight.index, j] for j in self.indexes if self.new_slot_times[j] < flight.eta) == 0,
                             name="c3[%s]" % flight)
        self.p.addConstr(quicksum(
            self.x[flight.index, j] * flight.costVect[j] for flight in self.offer.flights_a for j in
            self.indexes) <= quicksum(
            flight.costVect[flight.index] for flight in self.offer.flights_a) - self.eps,
                         name="c4a")
        self.p.addConstr(quicksum(
            self.x[flight.index, j] * flight.costVect[j] for flight in self.offer.flights_b for j in
            self.indexes) <= quicksum(
            flight.costVect[flight.index] for flight in self.offer.flights_b) - self.eps,
                         name="c4b")

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.x[flight.index, j] * flight.costVect[j] for flight in self.offer.flights_both for j in
                     self.indexes))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()
        status = self.p.Status
        if status == GRB.OPTIMAL:
            cost_reduction = sum(
                flight.costVect[flight.index] for flight in self.offer.flights_both) - self.p.objVal
            self.offer.set_cost_reduction(cost_reduction)
            for flight in self.offer.flights_both:
                for j in self.indexes:
                    if round(self.x[flight.index, j].x) == 1:
                        self.offer.new_indexes.append(j)
