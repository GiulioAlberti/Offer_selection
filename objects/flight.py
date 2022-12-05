import numpy as np

from input import new_slot_times
import matplotlib.pyplot as plt


class Flight:

    def __init__(self, index, slot, airline, cost_coefficients, cost_kind):

        self.name = "F" + airline.name + str(index)
        self.airline = airline
        self.airline.flights.append(self)
        self.index = index
        self.eta = slot
        self.sol = None
        self.cost_kind = cost_kind

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

        self.costVect = np.array([cost_fun(t - self.eta) for t in new_slot_times])
        self.is_selected = False
        self.change = 0
        # plt.plot(new_slot_times, self.costVect, 'b-')
        # plt.waitforbuttonpress()
        # plt.clf()

    def normalise(self, max_cost):
        self.norm_cost = self.cost / max_cost
        if self.cost_kind == "quad":
            norm_cost_fun = lambda delay: 0 if delay < 0 else (self.norm_cost * delay ** 2) / 2
        else:
            norm_cost_fun = lambda delay: 0 if delay < 0 else self.norm_cost * delay
        self.normCostVect = np.array([norm_cost_fun(t - self.eta) for t in new_slot_times])

    # def get_best_appr(self):
    #     max_delay = new_slot_times[-1] - self.eta
    #     sum_diff_values = {}
    #     for slope in np.linspace(0, 50, 50):
    #         for margin in np.linspace(0, 3 * max_delay // 4, 10):
    #             for jump in np.linspace(300, 9000, 20):
    #                 approx_cost_fun = lambda delay: 0 if delay < 0 else (
    #                         slope * delay + (0 if delay <= margin else jump))
    #                 sum_diff_values[(slope, margin, jump)] = sum(abs(self.normCostVect - np.array(
    #                     [approx_cost_fun(t - self.eta) for t in new_slot_times])))
    #     self.slope, self.margin, self.jump = min(sum_diff_values, key=sum_diff_values.get)
    #
    #     appr = lambda delay: 0 if delay < 0 else (
    #             self.slope * delay + (0 if delay <= self.margin else self.jump))
    #     values = np.array([appr(t - self.eta) for t in new_slot_times])
    #     plt.plot(new_slot_times, self.normCostVect, 'b-')
    #     plt.plot(new_slot_times, values, 'g-')
    #     plt.waitforbuttonpress()
    #     plt.clf()

    def assign_points(self):
        if new_slot_times[self.index] > self.eta + self.margin:  # Oltre salto
            self.later_points = 0
            self.earlier_points = 20 * self.slope + self.jump / self.margin

        else:  # prima del salto
            self.later_points = 20 * (1 / 6 - self.slope) + self.jump / self.margin
            self.earlier_points = 0

        # if new_slot_times[self.index] > self.eta + self.margin:  # Oltre salto
        #     self.later_points = (1 / self.slope + (len(new_slot_times) - self.index) / len(
        #         new_slot_times)) * (0.25 if (len(new_slot_times) - self.index) / len(
        #         new_slot_times) < 0.15 else 1)
        #     self.earlier_points = (12 * self.slope + (
        #         self.jump / 25 if (new_slot_times[self.index] - self.eta - self.margin) < new_slot_times[
        #             -1] / 5 else 1 / 5)) * (              #qua forse cambiare per renderlo indip da lunghezza intervalli
        #                               0.25 if (len(new_slot_times) - self.index) / len(
        #                                   new_slot_times) > 0.85 else 1)
        #
        # else:  # prima del salto
        #     self.later_points = (1 / self.slope + 25 / self.jump * self.margin / len(new_slot_times)) * (    #qua forse cambiare per renderlo indip da lunghezza intervalli
        #         0.25 if (len(new_slot_times) - self.index) / len(new_slot_times) < 0.15 else 1)
        #
        #     self.earlier_points = (12 * self.slope + self.index / len(new_slot_times)) * (
        #         0.25 if (len(new_slot_times) - self.index) / len(new_slot_times) > 0.85 else 1)

    def select_flight(self):
        self.is_selected = True

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
