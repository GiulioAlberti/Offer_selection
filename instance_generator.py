import numpy as np
import pandas as pd
from objects.slot import Slot


class InstanceGenerator:

    def __init__(self, seed, num_flights, interval, interval_modifier, cost_kind):
        self.cost_kind = cost_kind
        np.random.seed(seed)
        indexes = range(num_flights)

        self.slots = []
        for index in indexes:
            self.slots.append(Slot(index, interval * index, interval_modifier * interval * index))

        self.new_slot_times = np.array([slot.time for slot in self.slots])

        slopes_vect = np.array(np.random.uniform(0, 1 / 6, num_flights))
        margins_vect = np.array(
            [(np.random.uniform(15, max([20, self.new_slot_times[-1] + 5 - slot.old_time]))) for slot in self.slots])
        jumps_vect = np.array(np.random.uniform(5, 20, num_flights))

        self.cost_coefficients = np.array(
            [(slopes_vect[fl], margins_vect[fl], jumps_vect[fl]) for fl in range(num_flights)])

        self.df_airports =pd.read_csv("utils/airportMore25M.csv")
        self.airport =self.df_airports.Airport.sample(n=1).iloc[0]
        print("airport", self.airport)
        self.all_freq = pd.read_csv("utils/airport_airline_cluster_frequency.csv")
        self.df_airport_freq = self.all_freq[self.all_freq.airport == self.airport]
        self.df_airline_freq =self.df_airport_freq.groupby(['airline'])['frequency'].sum().to_frame('frequency').reset_index()
        self.airlines_names =self.df_airline_freq.airline.sample(n=num_flights, weights=self.df_airline_freq.frequency, replace=True).values

        # airlines_name_list = ["A", "B", "C", "D", "E", "F"]
        # # airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
        # self.airlines_names = np.random.choice(airlines_name_list, num_flights)