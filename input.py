import numpy as np

np.random.seed(21)
num_flights = 40
interval = 3
interval_modifier = 2
cost_coefficients = np.array(np.random.randint(1, 5, num_flights))
airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H"]
#airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
airlines_name = np.random.choice(airlines_name_list, num_flights)
# Not random:
# cost_coefficients = np.array([10, 1, 2, 7, 8, 5, 1, 3, 6, 7])
# airlines_name = ["C", "A", "B", "A", "B", "C", "A", "B", "A", "B"]
indexes = range(num_flights)
slots = np.array([interval * index for index in indexes])
new_slot_times = np.array([interval_modifier * slot for slot in slots])
