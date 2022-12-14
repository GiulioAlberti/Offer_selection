import gurobipy as gb
from gurobipy import GRB, quicksum


class LocalOptim:

    def __init__(self, flights):
        self.p = gb.Model()
        self.p.modelSense = GRB.MINIMIZE
        self.flights = flights
        self.slots = [flight.slot for flight in self.flights]
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addVars([(flight.slot.index, j.index) for j in self.slots for flight in flights],
                                vtype=GRB.BINARY)

    def set_constraints(self):
        for flight in self.flights:
            self.p.addConstr(quicksum(self.x[flight.slot.index, j.index] for j in self.slots) == 1,
                             name="c1[%s]" % flight)
            self.p.addConstr(
                quicksum(self.x[flight.slot.index, j.index] for j in self.slots if j.time < flight.eta) == 0,
                name="c2[%s]" % flight)

        for j in self.slots:
            self.p.addConstr(quicksum(self.x[flight.slot.index, j.index] for flight in self.flights) <= 1,
                             name="c3[%s]" % j)

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.x[flight.slot.index, j.index] * flight.costVect[j.index] for flight in self.flights for j in
                     self.slots))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()

        cost_reduction = sum(
            flight.costVect[flight.slot.index] for flight in self.flights) - self.p.objVal
        if cost_reduction > 0:
            for flight in self.flights:
                new_slot = None
                for j in self.slots:
                    if round(self.x[flight.slot.index, j.index].x) == 1:
                        new_slot = j
                flight.slot = new_slot
            print("airline", self.flights[0].airline, "has an internal optim of", cost_reduction)
