__author__ = 'tylar'

import csv

from src.settings import setup, DATA_TYPES

MAX_LEN = 5*60*1000  # max legitimate view time in ms
REPLACE_TIME = 60*1000  # length of time placed at start and end of illegitimate times

settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

pids = settings.get_pid_list()

for pid in pids:
    view_file_loc = setup(dataset=settings.dataset, dataLoc=settings.dataLoc, subjectN=pid).get_file_name(DATA_TYPES.avatar_views)

    # read all the rows in
    cols = list()
    with open(view_file_loc, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:

            print ', '.join(row)    # print the raw data
            # print row        # print raw data matrix
            t0 = int(row[0])
            tf = int(row[1])
            len = int(row[2])
            act = row[3]

            if len <= MAX_LEN:  # if this row is fine
                cols.append([t0, tf, len, act])
            else:  # else this row needs to be modified
                # log point at start of overly long view
                n_tf = t0 + REPLACE_TIME
                cols.append([t0, n_tf, REPLACE_TIME, act])

                # log another point at end of overly long view
                n_t0 = tf - REPLACE_TIME
                cols.append([n_t0, tf, REPLACE_TIME, act])

    # rewrite the file
    with open(view_file_loc, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in cols:
            writer.writerow(row)
