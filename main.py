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
        # executing the custom algorithm
        print("[Info] STARTING EXECUTION")
        scheduled = scheduling_1rC_BnB(jobs)

        print("----- RESULTS -----")
        for s in scheduled:
            # printing the obtained schedules
            print("Sum Weighted Completion Times:", s[0])
            print([j.id for j in s[1]])
            print("")
    else:
        print("[Error] no job available for scheduling")