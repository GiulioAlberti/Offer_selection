import numpy as np

from input import InputGenerator
from models.offer_eval import OfferEval
from objects.airline import Airline
from objects.flight import Flight
from objects.offer import Offer


def make_flights(instance: InputGenerator):
    airlines_names, slots, cost_kind, cost_coefficients = \
        instance.airlines_names, instance.slots, instance.cost_kind, instance.cost_coefficients
    airlines = [Airline(air_name) for air_name in np.unique(airlines_names)]
    airlines_dict = dict(zip([air.name for air in airlines], airlines))
    flights = []
    if cost_kind == "smj":
        for i in range(len(airlines_names)):
            flights.append(
                Flight(slots[i], airlines_dict[airlines_names[i]], cost_coefficients[i, :], cost_kind,
                       instance.new_slot_times))
    if cost_kind == "quad":
        for i in range(len(airlines_names)):
            flights.append(
                Flight(slots[i], airlines_dict[airlines_names[i]], cost_coefficients[i], cost_kind,
                       instance.new_slot_times))
        for air in airlines:
            normalise_flights(air)
    return flights, airlines


def normalise_flights(airline: Airline):
    max_cost = max([flight.cost for flight in airline.flights])
    for flight in airline.flights:
        flight.normalise(max_cost)


def make_couples_air(airline_list):
    couples = []
    for i in range(len(airline_list)):
        for j in range(i + 1, len(airline_list)):
            couples.append((airline_list[i], airline_list[j]))
    return couples


def make_offers(offers_list, air_couple, new_slot_times):
    air_a = air_couple[0]
    air_b = air_couple[1]
    num_ac = len(air_a.flights_couples)
    num_bc = len(air_b.flights_couples)
    for i in range(num_ac):
        for j in range(num_bc):
            number = len(offers_list)
            offer = Offer(number, air_a, air_b, air_a.flights_couples[i], air_b.flights_couples[j])
            offer_eval = OfferEval(offer, new_slot_times)
            offer_eval.solve()
            if offer.cost_reduction is not None:
                offers_list.append(offer)
    # num_at = len(air_a.flights_triples)
    # num_bt = len(air_b.flights_triples)
    # for i in range(num_at):
    #     for j in range(num_bt):
    #         number = len(offers_list)
    #         flights_a_list = []
    #         flights_b_list = []
    #         flights_a_list.extend(
    #             [air_a.flights_triples[i][0], air_a.flights_triples[i][1], air_a.flights_triples[i][2]])
    #         flights_b_list.extend(
    #             [air_b.flights_triples[j][0], air_b.flights_triples[j][1], air_b.flights_triples[j][2]])
    #         offer = Offer(number, air_a, air_b, flights_a_list, flights_b_list)
    #         offer_eval = OfferEval(offer, new_slot_times)
    #         offer_eval.solve()
    #         if offer.cost_reduction is not None:
    #             offers_list.append(offer)
