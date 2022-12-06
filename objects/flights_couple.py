class FlightsCouple:

    def __init__(self, fl_one, fl_two, points):
        self.name = "Couple " + str(fl_one) + " " + str(fl_two)
        self.fl_one = fl_one
        self.fl_two = fl_two
        self.points = points
        self.selected = False

    def select_in_solution(self):
        self.selected = True
        self.fl_one.select_flight()
        self.fl_two.select_flight()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
