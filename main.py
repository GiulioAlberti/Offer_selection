from input import *
from models.mincost import MinCost
from objects.functions2 import couples_eval, make_combinations_and_solve
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients, cost_kind="smj")
print("flight, earlier, later, post salto, slope, margin, jump")
for flight in flights:
    flight.assign_points()
# for airline in airline_list:
#     for flight in airline.flights:
#         print(flight, flight.earlier_points, flight.later_points,
#               new_slot_times[flight.index] > flight.eta + flight.margin, flight.slope, flight.margin, flight.jump)

air_couples = make_couples_air(airline_list)

Cut_reduction = make_combinations_and_solve(airline_list, air_couples, True)
Best_reduction = make_combinations_and_solve(airline_list, air_couples, False)
print("Percentage loss:", (Best_reduction - Cut_reduction) / Best_reduction *100)
couples_eval(airline_list)

# min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
# min_cost.solve()
# nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
# nnb.solve()
