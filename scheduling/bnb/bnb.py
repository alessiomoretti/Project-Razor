"""
This script contain the definitions a Branch & Bound algorithm and 
the derivation for the very problem in object
"""

from queue import Queue

from scheduling.bnb.state import State
from scheduling.algorithm import compute_euristic_H, compute_procedure_SS
from scheduling.job import get_jobs_dictionary

def scheduling_1rC_BnB(jobs):
    """
    This is an implementation of the branch and bound algorithm
    for the single machine, with weighted minimum completion time required 
    and release date constraints.

    @param jobs: list of Jobs object 
    @return: list of tuples representing the schedules (WC, [Job])
    """
    # 0. Heuristic solution
    h_schedule, h_WC = compute_euristic_H(jobs)

    # 1. Setup the BnB algorithm
    # create root state (with heuristic H bound) and initial params
    root = State(0)
    root.scheduled = []
    root.unscheduled = jobs
    root.lower_bound = h_WC

    # instantiating a queue for the visit of the tree
    q = Queue()
    q.put(root)
    # instantiating a bottom level candidate nodes
    best = []

    # 2. starting to iterate over the BnB tree (level i = i fixed scheduled jobs)
    while not q.empty():
        active_node = q.get()
        
        # 2.0 generate child level and check if end of tree is reached 
        child_level = active_node.level + 1
        if child_level > len(jobs):
            break
        print("LEVEL:", child_level)

        # 2.1 create the first candidates using release date dominance rules
        create_first_candidates(active_node, child_level)
        # 2.2 active node search by lower bound
        for child in active_node.children:
            print([job.id for job in child.scheduled])
            if child.lower_bound <= active_node.lower_bound or child.lower_bound <= root.lower_bound:
                print(child.lower_bound, "OK")
                if child_level == len(jobs):
                    best.append(child)
                else:
                    q.put(child)
            else:
                print("PRUNED!")
        print("")

    return [(b.weighted_completion_time, b.scheduled) for b in best]

                
            
def create_first_candidates(state, level):
    """
    This utility can be used to generate the first candidates of each state 
    and to update the list of children of the active state.
    
    @param state: State (current active state)
    @param level: int, the candidates level
    @return: None
    """
    # retrieve jobs by release_dates
    jobs_rd = get_jobs_dictionary(state.unscheduled)
    release_dates = list(jobs_rd.keys())
    # -> compute time variable from 
    T = max(state.completion_time, min(release_dates))

    # filtering jobs by p/w ratio and earliest release dates
    candidates = list(filter(lambda j: j.release_date <= T, state.unscheduled))
    
    # create new states
    for job in candidates:
        s = State(level)
        # update (un)scheduled in new states
        s.scheduled = state.scheduled[:] + [job]
        s.unscheduled = state.unscheduled[:]
        s.unscheduled.remove(job)
        # update completion time
        s.completion_time = T + job.processing_time
        s.weighted_completion_time = state.weighted_completion_time + job.weight * s.completion_time
        # compute and update the lower bound
        _, LB, _, _ = compute_procedure_SS(s.unscheduled)
        s.lower_bound = s.weighted_completion_time + LB
        # resetting all the release dates in the unscheduled jobs (RDA)
        # add as a new child
        state.add_child(s)
        