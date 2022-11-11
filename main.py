from input import *
from models.mincost import MinCost
from models.offers_choice import OffersChoice
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients, cost_kind="smj")
print("flight, earlier, later, oltre salto, slope, margin, jump")
for flight in flights:
    flight.assign_points()
    print(flight, flight.earlier_points, flight.later_points, new_slot_times[flight.index] > flight.eta + flight.margin,
          flight.slope, flight.margin, flight.jump)

air_couples = make_couples_air(airline_list)
for airline in airline_list:
    airline.make_flights_comb(2)
#   airline.make_flights_comb(3)
offers_list = []
for couple in air_couples:
    make_offers(offers_list, couple)
print(len(offers_list), " offers created")
offers_choice = OffersChoice(offers_list)
offers_choice.solve()

# min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
# min_cost.solve()
# nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
# nnb.solve()
