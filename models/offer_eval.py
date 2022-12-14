import gurobipy as gb
from gurobipy import GRB, quicksum

from objects.offer import Offer


# nel caso di quadratic, sostituire costVect con NormCostVect
class OfferEval:

    def __init__(self, offer: Offer, new_slot_times):
        self.p = gb.Model()
        self.p.modelSense = GRB.MINIMIZE
        self.offer = offer
        self.eps = 0.0001
        self.slots = offer.slots_both
        self.new_slot_times = new_slot_times
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addVars([(i, j) for i in self.slots for j in self.slots], vtype=GRB.BINARY)

    def set_constraints(self):
        for i in self.slots:
            self.p.addConstr(quicksum(self.x[i, j] for j in self.slots) == 1, name="c1[%s]" % i)
            self.p.addConstr(quicksum(self.x[j, i] for j in self.slots) == 1, name="c2[%s]" % i)
        # for i in self.slots:  # elim same place
        #     self.p.addConstr(self.x[i, i] == 0, name="ce[%s]" % i)
        for flight in self.offer.flights_both:
            self.p.addConstr(quicksum(
                self.x[flight.slot, j] for j in self.slots if j.time < flight.eta) == 0,
                             name="c3[%s]" % flight)
        self.p.addConstr(quicksum(
            self.x[flight.slot, j] * flight.costVect[j.index] for flight in self.offer.flights_a for j in
            self.slots) <= quicksum(
            flight.costVect[flight.slot.index] for flight in self.offer.flights_a) - self.eps,
                         name="c4a")
        self.p.addConstr(quicksum(
            self.x[flight.slot, j] * flight.costVect[j.index] for flight in self.offer.flights_b for j in
            self.slots) <= quicksum(
            flight.costVect[flight.slot.index] for flight in self.offer.flights_b) - self.eps,
                         name="c4b")

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.x[flight.slot, j] * flight.costVect[j.index] for flight in self.offer.flights_both for j in
                     self.slots))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()
        status = self.p.Status
        if status == GRB.OPTIMAL:
            cost_reduction = sum(
                flight.costVect[flight.slot.index] for flight in self.offer.flights_both) - self.p.objVal
            self.offer.set_cost_reduction(cost_reduction)
            for flight in self.offer.flights_both:
                for j in self.slots:
                    if round(self.x[flight.slot, j].x) == 1:
                        self.offer.new_slots.append(j)
