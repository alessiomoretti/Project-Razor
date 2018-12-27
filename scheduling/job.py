"""
This script contains the definition of a Job and related utilities
"""

class Job:
    def __init__(self, id, release_date, processing_time, weight=1):
        """
        This class represent the Job 
        @param id: integer, the job unique identifier
        @param release_date: int, the job release date
        @param processing_time: int, the job required processing time
        @param weight: int, the weight of the job processing
        """
        self.id = id
        self.release_date = release_date
        self.processing_time = processing_time
        self.weight = weight

    def set_completion(self, completion_time):
        self.completion_time = completion_time

    def get_weighted_processing(self):
        return self.processing_time / self.weight

def get_jobs_dictionary(jobs):
    """
    This utility can be used to return a dictionary for further processing
    key => release_date
    value => job

    @return: Dictionary(release_date, job)
    """
    jobs_dict = dict()

    for j in jobs:
        r = j.release_date
        if r not in jobs_dict:
            jobs_dict[r] = [j]
        else:
            jobs_dict[r].append(j)

    return jobs_dict