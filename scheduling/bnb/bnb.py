"""
This script contain the definitions a Branch & Bound algorithm and 
the derivation for the very problem in object

References: 
-  Hariri & Potts ("An algorithm for single machine sequencing with release dates to minimize total weighted completion time")
-  Belouadah, Posner & Potts ("Scheduling with release dates on a single machine to minimize total weighted completion time")
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

    # initializing list of active lower bounds
    lower_bounds = [root.lower_bound]

    # instantiating a queue for the visit of the tree
    q = Queue()
    q.put(root)
    # instantiating a bottom level candidate nodes
    schedules = []

    # 2. starting to iterate over the BnB tree (level i = i fixed scheduled jobs)
    while not q.empty():
        active_node = q.get()
        
        # 2.0 generate child level and check if end of tree is reached 
        child_level = active_node.level + 1
        if child_level > len(jobs):
            break

        # 2.1 create the first candidates using release date dominance rules
        create_first_candidates(active_node, child_level)
        # 2.2 active node search by lower bound
        for child in active_node.children:
            if child.lower_bound <= min(lower_bounds):
                if child_level == len(jobs):
                    schedules.append(child)
                else:
                    q.put(child)
                    lower_bounds.append(child.lower_bound)

    return [(s.weighted_completion_time, s.scheduled) for s in schedules]

                
            
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
    # -> compute time variable representing the eligible release date
    T = max(state.completion_time, min(release_dates))    
    unscheduled = state.unscheduled
    
    # Thm2 (Rinaldi&Sassano) from Hariri-Potts
    # -> filtering jobs by earliest due dates
    candidates_thm2 = list(filter(lambda j: j.release_date <= T, unscheduled))
    # -> selecting the min p_w jobs
    if len(candidates_thm2) >= 1:
        min_pw = min([j.get_weighted_processing() for j in candidates_thm2])
        candidates = list(filter(lambda j: j.get_weighted_processing() <= min_pw, candidates_thm2))
        # create new states
        for job in candidates:
            s = State(level)
            s.initialization(state, job, T)
            # it is not necessary to compute lower bound in this case 
            # (it is exactly the lower bound of the parent state)
            s.lower_bound = state.lower_bound
            # resetting all the release dates in the unscheduled jobs (RDA)
            # add as a new child
            state.add_child(s)

    else:
        # Thm3 (Dessouky&Deogun) + Thm4 Hariri-Potts 
        # -> retrieving min expected completion time and job with that C
        min_C = min([T + j.processing_time for j in unscheduled])
        min_WC = min([j.weight * (T + j.processing_time) for j in unscheduled])
        thm3_dominance_rule = lambda j: T + j.processing_time <= min_C or j.release_date < min_C
        thm4_dominance_rule = lambda j: j.weight * (T + j.processing_time) <= min_WC
        thm34_dominance_rule = lambda j: thm3_dominance_rule(j) or thm4_dominance_rule(j)
        candidates_thm34 = list(filter(thm34_domination_rule, unscheduled))

        for job in candidates_thm34:
            # create new states
            s = State(level)
            s.initialization(state, job, T)
            # computing LB
            _, LB, _, _ = compute_procedure_SS(s.unscheduled)
            s.lower_bound = state.completion_time + LB
            # resetting all the release dates in the unscheduled jobs (RDA)
            # add as a new child
            state.add_child(s)