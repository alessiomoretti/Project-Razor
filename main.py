from utils.reader import read_jobs
from scheduling.algorithm import *
from scheduling.bnb.bnb import scheduling_1rC_BnB

if __name__ == "__main__":
    # reading jobs 
    jobs = read_jobs("./samples/test_sample_2.csv")
    for job in jobs:
        print("JOB {0} -> starting {1} -> processing time required {2}".format(job.id, job.release_date, job.processing_time))
    print("TOTAL JOBS: {0}\n\n".format(len(jobs)))

    if len(jobs) > 0:
        print("EXECUTION")
        scheduling_1rC_BnB(jobs)
    else:
        print("[Error] no job available for scheduling")