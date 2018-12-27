"""
This script contains the definition of a state in the Branch & Bound tree for the 
single machine scheduling problem.
"""

class State:
    def __init__(self, level):
        self.level = level
        # scheduled and unscheduled jobs
        self.scheduled = dict()
        self.unscheduled = []
        # completion time and LB
        self.completion_time = 0
        self.weighted_completion_time = 0
        self.lower_bound = 0
        # children states
        self.children = []

    def get_children(self):
        return self.children

    def add_child(self, state):
        self.children.append(state)