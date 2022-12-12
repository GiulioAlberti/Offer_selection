import numpy as np
import pandas as pd

from input import InputGenerator
from models.mincost import MinCost
from objects.functions import sum_costs
from objects.functions2 import make_combinations_and_solve, couples_eval
from objects.initializer import make_flights, make_couples_air

s_, tot_in, noc, nob, cr, br = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

for seed in range(1, 2):
    print('Seed:', seed)
    instance = InputGenerator(seed=seed, num_flights=45, interval=1, interval_modifier=2, cost_kind="smj")

    flights, airline_list = make_flights(instance)
    for flight in flights:
        flight.assign_points()
        # print(flight, flight.earlier_points, flight.later_points)

    air_couples = make_couples_air(airline_list)

    total_initial = sum_costs(flights)
    num_off_cut, Cut_reduction = make_combinations_and_solve(airline_list, air_couples, instance.new_slot_times, True)
    num_off_best, Best_reduction = make_combinations_and_solve(airline_list, air_couples, instance.new_slot_times,
                                                               False)
    # couples_eval(airline_list)

    # tot_in.append(total_initial)
    # s_.append(seed)
    # noc.append(num_off_cut)
    # nob.append(num_off_best)
    # cr.append(Cut_reduction)
    # br.append(Best_reduction)
    # df = pd.DataFrame(
    #     {'seed': s_, 'total_initial': tot_in, 'num_off_cut': noc, 'num_off_best': nob, 'cut_reduction': cr,
    #      'best_reduction': br})
    tot_in = np.append(tot_in, total_initial)
    s_ = np.append(s_, seed)
    noc = np.append(noc, num_off_cut)
    nob = np.append(nob, num_off_best)
    cr = np.append(cr, Cut_reduction)
    br = np.append(br, Best_reduction)

df = pd.DataFrame(
    {'seed': s_, 'total_initial': tot_in, 'num_off_cut': noc,
     'num_off_best': nob, 'cut_reduction': cr,
     'best_reduction': br})

df['cut_over_total'] = df.cut_reduction / df.total_initial
df['best_over_total'] = df.best_reduction / df.total_initial
df['off_cut_over_best'] = df.num_off_cut / df.num_off_best
df.to_csv('neg11_45_10_NN.csv', index_label=False, index=False)

df2 = pd.DataFrame(
    {'cut_over_total_mean': np.array([df['cut_over_total'].mean()]),
     'best_over_total_mean': np.array([df['best_over_total'].mean()]),
     'off_cut_over_best_mean': np.array([df['off_cut_over_best'].mean()])})
df2.to_csv('neg11_45_10_NN.csv', index_label=False, index=False, mode='a')

# pd.read_csv('namefile.csv')

# param_research(flights, [flight.later_points for flight in flights], 'later')
# param_research(flights, [flight.earlier_points for flight in flights], 'earlier')


# min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
# min_cost.solve()
# nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
# nnb.solve()
