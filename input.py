import numpy as np

np.random.seed(160)
num_flights = 60
interval = 3
interval_modifier = 2
total_int = interval * interval_modifier
# cost_coefficients = np.array(np.random.randint(1, 5, num_flights))     era per il caso quadratico

slopes_vect = np.array(1 / np.random.randint(2, 7, num_flights))
margins_vect = np.array(
    [(np.random.randint((num_flights - x) * total_int // 8, 3 * (num_flights - x) * total_int // 4)) for x in
     range(num_flights)])
jumps_vect = np.array(np.random.randint(10, 50, num_flights))

cost_coefficients = np.array([(slopes_vect[fl], margins_vect[fl], jumps_vect[fl]) for fl in range(num_flights)])

airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
# airlines_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
airlines_name = np.random.choice(airlines_name_list, num_flights)

indexes = range(num_flights)
slots = np.array([interval * index for index in indexes])
new_slot_times = np.array([interval_modifier * slot for slot in slots])
