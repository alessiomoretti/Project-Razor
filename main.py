from utils.reader import read_jobs
from scheduling.algorithm import *
from scheduling.bnb.bnb import scheduling_1rC_BnB

from sys import argv

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage error: <input_sample_csv>")

    # reading jobs 
    jobs = read_jobs(argv[1])
    for job in jobs:
        print("JOB {0} -> starting {1} -> processing time required {2}".format(job.id, job.release_date, job.processing_time))
    print("TOTAL JOBS: {0}\n\n".format(len(jobs)))

    if len(jobs) > 0:
        # executing the custom algorithm
        print("[Info] STARTING EXECUTION")
        scheduled = scheduling_1rC_BnB(jobs)

        print("[Info] EXECUTION COMPLETED: {0} RESULTS".format(len(scheduled)))
        s = scheduled[0]
        # printing the first of schedules
        print("\n\nSum Weighted Completion Times:", s[0])
        print([j.id for j in s[1]])
        print("")
    else:
        print("[Error] no job available for scheduling")