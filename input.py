import numpy as np

np.random.seed(24)
num_flights = 45
interval = 1
interval_modifier = 2
total_int = interval * interval_modifier
indexes = range(num_flights)
slots = np.array([interval * index for index in indexes])
new_slot_times = np.array([interval_modifier * slot for slot in slots])

slopes_vect = np.array(np.random.uniform(0, 1 / 6, num_flights))
margins_vect = np.array([(np.random.uniform(15, max([20, new_slot_times[-1] + 5 - x]))) for x in slots])
jumps_vect = np.array(np.random.uniform(5, 20, num_flights))

cost_coefficients = np.array([(slopes_vect[fl], margins_vect[fl], jumps_vect[fl]) for fl in range(num_flights)])

airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
# airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
airlines_name = np.random.choice(airlines_name_list, num_flights)
