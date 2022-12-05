from input import *
from models.mincost import MinCost
from objects.functions2 import *
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients, cost_kind="smj")
for flight in flights:
    flight.assign_points()
    # print(flight, flight.earlier_points, flight.later_points, flight.slope, flight.margin, flight.jump, 10 * flight.slope, flight.jump / flight.margin)

air_couples = make_couples_air(airline_list)

num_off_cut, Cut_reduction = make_combinations_and_solve(airline_list, air_couples, True)
num_off_init, Best_reduction = make_combinations_and_solve(airline_list, air_couples, False)
print("Percentage loss:", (Best_reduction - Cut_reduction) / Best_reduction * 100)
print("Percentage num offers red:", (num_off_init - num_off_cut) / num_off_init * 100)

couples_eval(airline_list)


# param_research(flights, [flight.later_points for flight in flights], 'later')
# param_research(flights, [flight.earlier_points for flight in flights], 'earlier')


# min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
# min_cost.solve()
# nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
# nnb.solve()
