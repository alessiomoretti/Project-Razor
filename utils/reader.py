"""
This script contains the utilities to read samples of jobs from the
single machine with release dates problem
"""

import csv

from constants import *
from scheduling.job import Job

def read_jobs(input_file_csv):
    """
    This utility can be called to read from a csv (with headers "id", "release")
    the sample records for jobs in the problem

    @param input_file_csv: string, the path of the samples csv
    @return: list of Jobs
    """
    # preparing the jobs list
    jobs = []

    try:
        # reading table with sample records from csv
        with open(input_file_csv) as sample_file:
            sample_records = csv.DictReader(sample_file)
            for record in sample_records:
                # creating a new job by id and release date
                j = Job(record[JOB_ID], int(record[JOB_RELEASE_DATE]), int(record[JOB_PROCESSING_TIME]), int(record[JOB_WEIGHT]))
                jobs.append(j)
    except FileNotFoundError:
        print("File not found at: {0}".format(input_file_csv))
    except Exception:
        print("An error occured reading file")

    return jobs