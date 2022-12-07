import numpy as np
import pandas as pd


class InputGenerator:

    def __init__(self, seed, num_flights, interval, interval_modifier, cost_kind):
        self.cost_kind = cost_kind
        np.random.seed(seed)
        total_int = interval * interval_modifier
        indexes = range(num_flights)
        self.slots = np.array([interval * index for index in indexes])
        self.new_slot_times = np.array([interval_modifier * slot for slot in self.slots])

        slopes_vect = np.array(np.random.uniform(0, 1 / 6, num_flights))
        margins_vect = np.array([(np.random.uniform(15, max([20, self.new_slot_times[-1] + 5 - x]))) for x in self.slots])
        jumps_vect = np.array(np.random.uniform(5, 20, num_flights))

        self.cost_coefficients = np.array([(slopes_vect[fl], margins_vect[fl], jumps_vect[fl]) for fl in range(num_flights)])

        airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        # airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
        self.airlines_names = np.random.choice(airlines_name_list, num_flights)
