"""
This script contains the definition of a state in the Branch & Bound tree for the 
single machine scheduling problem.
"""

class State:
    def __init__(self, level):
        """
        This class represents a single node in the Branch and Bound
        search tree.

        @param level: int, the child level in bnb tree
        """
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

    def initialization(self, state, job, T):
        """
        This method can be used to initialize a state from
        the parent one.

        @param state: State, the parent of the current state
        @param job: Job, the job to add as scheduled
        @param T: int, the execution time
        """
        # update (un)scheduled in new states
        self.scheduled = state.scheduled[:] + [job]
        self.unscheduled = state.unscheduled[:]
        self.unscheduled.remove(job)
        # update completion time
        self.completion_time = T + job.processing_time
        self.weighted_completion_time = state.weighted_completion_time + job.weight * self.completion_time

    def get_children(self):
        return self.children

    def add_child(self, state):
        self.children.append(state)