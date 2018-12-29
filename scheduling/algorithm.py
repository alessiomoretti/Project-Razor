"""
In this script the definition of the used algorithms, upon which is built the BnB algorithm.
References: 
-  Hariri & Potts ("An algorithm for single machine sequencing with release dates to minimize total weighted completion time")
-  Belouadah, Posner & Potts ("Scheduling with release dates on a single machine to minimize total weighted completion time")
"""
from scheduling.job import *

def compute_euristic_H(jobs):
    # setting initial values
    u = 0       # schedule position
    t = 0       # counter for completion time
    WC = 0      # counter for weighted completion time
    
    # preparing scheduling structures
    jobs_list = jobs[:]
    schedule = dict()

    while len(jobs_list) > 0:
        
        # select the minimum release date
        jobs_dict = get_jobs_dictionary(jobs_list)
        min_r = min(jobs_dict.keys())
        if t < min_r: t = min_r 

        # select the feasible job
        feasible_r = list(filter(lambda r: r <= t, jobs_dict.keys()))
        feasible_j = None
        for r in feasible_r:
            for job in jobs_dict[r]:
                if feasible_j == None:
                    feasible_j = job
                else:
                    # for the minimum r, get the job with minimum (p / w) value
                    if feasible_j.get_weighted_processing() > job.get_weighted_processing():
                        feasible_j = job
        # remove selected job from the original schedule
        jobs_list.remove(feasible_j)

        # update execution params
        u = u + 1
        t = t + feasible_j.processing_time
        WC = WC + feasible_j.weight * t
        
        feasible_j.set_completion(t)
        schedule[u] = feasible_j        
    
    return schedule, WC


def compute_procedure_SS(jobs):
    # setting initial values
    u = 0       # schedule position
    t = 0       # counter for completion time
    WC = 0      # counter for weighted completion time
    CBRK = 0    # cost of breaking jobs in splitting procedure

    # preparing scheduling structures
    jobs_list = jobs[:]
    schedule = dict()

    # to verify if any pre-emption occured
    pre_emption_occured = False
    
    while len(jobs_list) > 0:

        # select the minimum release date
        jobs_dict = get_jobs_dictionary(jobs_list)
        min_r = min(jobs_dict.keys())
        # set time
        if t < min_r: t = min_r 

        # select the feasible job
        feasible_r = list(filter(lambda r: r <= t, jobs_dict.keys()))
        feasible_j = None
        for r in feasible_r:
            for job in jobs_dict[r]:
                if feasible_j == None:
                    feasible_j = job
                else:
                    # for the minimum r, get the job with minimum (p / w) value
                    if feasible_j.get_weighted_processing() > job.get_weighted_processing():
                        feasible_j = job
        
        # -> check over relaxing of the integer constraints (splitting required)
        to_be_splitted = False
        lighter_jobs = []                                   # lighter jobs aux list
        for job in jobs_list: 
            if job.get_weighted_processing() < feasible_j.get_weighted_processing():
                lighter_jobs.append(job)                    # update lighter jobs list
                if job.release_date < t + feasible_j.processing_time:
                    to_be_splitted = True                   # verified splitting condition

        # update general execution params
        u = u + 1

        # simple split procedure 
        if to_be_splitted:
            # get job with earliest release date amongst the light jobs found before
            lighter_jobs.sort(key = lambda j: j.release_date)
            earliest_job = lighter_jobs[0]
            # [SS] splitting feasible job
            j1, j2 = job_splitting_procedure(feasible_j, t, earliest_job.release_date)

            # update exec. params
            t = earliest_job.release_date
            j1.set_completion(t)
            WC = WC + j1.weight * t
            CBRK = CBRK + (j1.weight * j2.processing_time)

            # update schedule 
            schedule[u] = j1 
            jobs_list.remove(feasible_j)
            jobs_list.append(j2)

        else:
            # update exec. params (no splitting)
            t = t + feasible_j.processing_time
            feasible_j.set_completion(t)
            WC = WC + feasible_j.weight * t
            # update schedule (no splitting)
            schedule[u] = feasible_j
            jobs_list.remove(feasible_j)

    # compute lowerbound
    LB = WC + CBRK

    return schedule, LB, WC, CBRK


def job_splitting_procedure(job, t, early_r):
    # retrieving new release dates
    r_1 = r_2 = job.release_date
    # computing new processing times
    p_1 = early_r - t
    p_2 = job.processing_time - p_1
    # computing new weights
    w_1 = p_1 * job.weight / job.processing_time
    w_2 = job.weight - w_1

    # creating the new jobs
    job1 = Job(job.id + "_1", r_1, p_1, w_1)
    job2 = Job(job.id + "_2", r_2, p_2, w_2)

    return job1, job2