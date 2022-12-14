import numpy as np

from objects.slot import Slot


class Flight:

    def __init__(self, slot: Slot, airline, cost_coefficients, cost_kind, new_slot_times):

        self.name = "F" + airline.name + str(slot.index)
        self.airline = airline
        self.airline.flights.append(self)
        self.slot = slot
        self.index = slot.index
        self.eta = slot.old_time
        self.min_cost_sol = None
        self.cost_kind = cost_kind
        self.new_slot_times = new_slot_times

        if cost_kind == "quad":
            self.cost = cost_coefficients
            self.norm_cost = None
            self.normCostVect = None

        if cost_kind == "smj":
            self.slope = cost_coefficients[0]
            self.margin = cost_coefficients[1]
            self.jump = cost_coefficients[2]

        self.earlier_points = None
        self.later_points = None

        if cost_kind == "quad":
            cost_fun = lambda delay: 0 if delay < 0 else (self.cost * delay ** 2) / 2
        elif cost_kind == "smj":
            cost_fun = lambda delay: 0 if delay < 0 else (
                    self.slope * delay + (0 if delay <= self.margin else self.jump))
        else:
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay

        self.costVect = np.array([cost_fun(t - self.eta) for t in self.new_slot_times])
        self.is_selected = False
        self.change = 0

    def normalise(self, max_cost):
        self.norm_cost = self.cost / max_cost
        if self.cost_kind == "quad":
            norm_cost_fun = lambda delay: 0 if delay < 0 else (self.norm_cost * delay ** 2) / 2
        else:
            norm_cost_fun = lambda delay: 0 if delay < 0 else self.norm_cost * delay
        self.normCostVect = np.array([norm_cost_fun(t - self.eta) for t in self.new_slot_times])

    def assign_points(self):
        if self.slot.time > self.eta + self.margin:  # Oltre salto
            self.later_points = -30
            # self.earlier_points = 1
            self.earlier_points = 30 * self.slope + 1 * self.jump / (
                        0.5 + self.slot.time - self.eta - self.margin)


        else:  # prima del salto
            # self.later_points = 1
            self.later_points = 30 * (1 / 6 - self.slope) + 1 * (
                    self.eta + self.margin - self.slot.time) / self.jump
            self.earlier_points = -30

    def select_flight(self):
        self.is_selected = True

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
