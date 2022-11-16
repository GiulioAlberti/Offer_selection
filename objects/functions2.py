from matplotlib import pyplot as plt

from models.offers_choice import OffersChoice
from objects.initializer import make_offers


def couples_eval(airline_list):
    couples_used = [fc for airline in airline_list for fc in airline.flights_couples if fc.selected]
    couples_not_used = [fc for airline in airline_list for fc in airline.flights_couples if not fc.selected]
    values_used = [fc.points for fc in couples_used]
    values_not_used = [fc.points for fc in couples_not_used]

    level = 10
    plt.plot(values_used, 'g s')
    plt.axhline(y=level)
    plt.waitforbuttonpress()
    plt.clf()
    plt.plot(values_not_used, 'r s')
    plt.axhline(y=level)
    plt.waitforbuttonpress()
    plt.clf()

    for lv in range(level, level + 10):
        g_perc = 0
        r_perc = 0
        for val in values_used:
            if val > lv:
                g_perc += 100 / len(values_used)
        for val in values_not_used:
            if val <= lv:
                r_perc += 100 / len(values_not_used)
        print(lv, g_perc, r_perc)


def make_combinations_and_solve(airline_list, air_couples, cut):
    for airline in airline_list:
        airline.make_flights_comb(2, cut)
    #   airline.make_flights_comb(3, cut)
    offers_list = []
    for couple in air_couples:
        make_offers(offers_list, couple)
    print(len(offers_list), " offers created")
    offers_choice = OffersChoice(offers_list)
    offers_choice.solve()
    return offers_choice.sol
