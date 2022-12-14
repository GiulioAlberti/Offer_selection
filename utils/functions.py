def sum_costs(flights, initial=True):
    return sum([flight.costVect[flight.slot.index if initial else flight.min_cost_sol] for flight in flights])
