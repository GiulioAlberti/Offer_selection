from input import *
from models.mincost import MinCost
from models.offers_choice import OffersChoice
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients)

couples = make_couples_air(airline_list)
for airline in airline_list:
    airline.make_flights_couples()
offers_list = []
for couple in couples:
    make_offers(offers_list, couple)
print(len(offers_list), " offers created")
offers_choice = OffersChoice(offers_list)
offers_choice.solve()

# min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
# min_cost.solve()
# nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
# nnb.solve()
