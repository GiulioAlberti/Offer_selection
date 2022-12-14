from __future__ import annotations
from typing import Union


class Slot:
    def __init__(self, index: Union[int, None] = None, old_time: Union[float, None] = None,
                 time: Union[float, None] = None):
        self.index = index
        self.old_time = old_time
        self.time = time

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index) + ":" + str(self.time)

    def __eq__(self, other: Slot):
        return self.time == other.time

    def __lt__(self, other: Slot):
        return self.time < other.time

    def __le__(self, other: Slot):
        return self.time <= other.time

    def __gt__(self, other: Slot):
        return self.time > other.time

    def __ge__(self, other: Slot):
        return self.time >= other.time

    def __hash__(self):
        return hash(self.index)
