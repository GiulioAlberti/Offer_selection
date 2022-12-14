import numpy as np
from matplotlib import pyplot as plt

from models.offers_choice import OffersChoice
from objects.initializer import make_offers


def couples_eval(airline_list):
    couples_used = [fc for airline in airline_list for fc in airline.flights_couples if fc.selected]
    couples_not_used = [fc for airline in airline_list for fc in airline.flights_couples if not fc.selected]
    values_used = [fc.points for fc in couples_used]
    values_not_used = [fc.points for fc in couples_not_used]

    figure, (ax, ax2) = plt.subplots(ncols=2, sharey="all")
    ax.plot(values_used, 'g s')
    ax.axhline(y=-5)
    ax.set_title("Used")
    ax2.plot(values_not_used, 'r s')
    ax2.axhline(y=-5)
    ax2.set_title("Not Used")
    plt.show()
    plt.clf()


def make_combinations_and_solve(airline_list, air_couples, new_slot_times, cut):
    for airline in airline_list:
        airline.make_flights_comb(2, cut)
    #   airline.make_flights_comb(3, cut)
    offers_list = []
    for couple in air_couples:
        make_offers(offers_list, couple, new_slot_times)
    num_off = len(offers_list)
    print(num_off, " offers created")
    offers_choice = OffersChoice(offers_list)
    offers_choice.solve()
    return num_off, offers_choice.sol


def param_research(flights, param_vector1, sense):
    flight_selection = [flight.is_selected for flight in flights]

    for i in range(len(flights)):
        plt.plot(i, param_vector1[i], color=('green' if flight_selection[i] else 'red'), marker='o', linestyle='')
    if sense == 'later':
        x = [flight.index for flight in flights if flight.change == 1]  #qua da vedere se index o slot.index
        for i in range(len(x)):
            plt.plot([x[i], x[i]], [0, 8], 'k-')
    if sense == 'earlier':
        x = [flight.index for flight in flights if flight.change == -1] #qua da vedere se index o slot.index
        for i in range(len(x)):
            plt.plot([x[i], x[i]], [0, 8], 'k-')
    plt.show()
