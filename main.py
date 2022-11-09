from input import *
from models.mincost import MinCost
from models.offers_choice import OffersChoice
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients)
#for airline in airline_list:
#    for flight in airline.flights:
for flight in flights:
    flight.get_best_appr()
    flight.assign_points()
#    print(flight, flight.slope, flight.margin, flight.jump, flight.norm_cost)
#    print(flight, flight.later_points, flight.earlier_points)
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
