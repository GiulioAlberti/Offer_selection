import numpy as np

from input import new_slot_times


class Flight:

    def __init__(self, index, slot, airline, cost_coefficient, cost_kind="quad"):

        self.name = "F" + airline.name + str(index)
        self.airline = airline
        self.airline.flights.append(self)
        self.index = index
        self.cost = cost_coefficient
        self.eta = slot
        self.cost_kind = cost_kind
        self.sol = None
        self.norm_cost = None
        self.normCostVect = None
        self.jump = None
        self.margin = None
        self.slope = None
        self.earlier_points = None
        self.later_points = None

        if cost_kind == "quad":
            cost_fun = lambda delay: 0 if delay < 0 else (self.cost * delay ** 2) / 2
        else:
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay

        self.costVect = np.array([cost_fun(t - self.eta) for t in new_slot_times])

    def normalise(self, max_cost):
        self.norm_cost = self.cost / max_cost
        if self.cost_kind == "quad":
            norm_cost_fun = lambda delay: 0 if delay < 0 else (self.norm_cost * delay ** 2) / 2
        else:
            norm_cost_fun = lambda delay: 0 if delay < 0 else self.norm_cost * delay
        self.normCostVect = np.array([norm_cost_fun(t - self.eta) for t in new_slot_times])

    def get_best_appr(self):
        max_delay = new_slot_times[-1] - self.eta
        sum_diff_values = {}
        for slope in np.linspace(0, 50, 50):
            for margin in np.linspace(0, 3 * max_delay // 4, 10):
                for jump in np.linspace(10, 10 * max_delay, 10):
                    approx_cost_fun = lambda delay: 0 if delay < 0 else (
                            slope * delay + (0 if delay <= margin else jump))
                    sum_diff_values[(slope, margin, jump)] = sum(abs(self.normCostVect - np.array(
                        [approx_cost_fun(t - self.eta) for t in new_slot_times])))
        self.slope, self.margin, self.jump = min(sum_diff_values, key=sum_diff_values.get)

    def assign_points(self):
        if new_slot_times[self.index] > self.eta + self.margin:
            self.later_points = 100 / self.slope * (
                0.25 if (len(new_slot_times) - self.index) / len(new_slot_times) < 0.2 else 1)
            self.earlier_points = self.slope / 6 * (
                0.2 * self.jump / (new_slot_times[-1] - self.eta) if (new_slot_times[
                                                                          self.index] - self.eta - self.margin) <
                                                                     new_slot_times[-1] / 10 else 1)
        else:
            self.later_points = 100 / self.slope * 10 * (new_slot_times[-1] - self.eta) / self.jump * (
                0.25 if (len(new_slot_times) - self.index) / len(new_slot_times) < 0.2 else 1)
            self.earlier_points = self.slope / 6 * (
                0.25 if (len(new_slot_times) - self.index) / len(new_slot_times) > 0.8 else 1)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
