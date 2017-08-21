import json
import time
import os.path
import difflib
import multiprocessing

variables = {}
print("Downloading new adds from gorkanajobs.")
execfile("gorkanajobs.py", variables)
print("Downloading new adds from holdthefrontpage.")
execfile("holdthefrontpage.py", variables)
print("Downloading new adds from journalism.co.uk.")
execfile("journalism.py", variables)
print("Finding the duplicates.")

# Creating empty array for storing the duplicates
duplicates = []

# Opening the data file
with open('data.json') as inFile:
    try:
        data = json.load(inFile)
    except ValueError:
        data = []

# A worker method
def worker(idx, duplicates):
    """thread worker function"""
    for idx2 in range(idx+1, len(data)):
        # Using SequenceMatcher to identify if two records are identical. The aprove ratio is >= 0.7
        s = difflib.SequenceMatcher(None, data[idx]["Details"], data[idx2]["Details"])
        if s.ratio() >= 0.70:
            print(idx)
            duplicates[idx] = 1
            return

# Creating pool of processes
pool = multiprocessing.Pool()
manager = multiprocessing.Manager()
duplicates = manager.dict()

# Preparing the duplicates array.
for indx, row in enumerate(data):
    duplicates[indx] = 0

# Calling the worker function for each record
for indx, row in enumerate(data):
    pool.apply_async(worker, args=(indx, duplicates))

# After all processes from the pool are finished joining the pool with the main process.
pool.close()
pool.join()
2
# Going trough the shared duplicates array and checking up the duplicates in the main data array
for indx, row in enumerate(data):
    if duplicates[indx] == 1:
        data[indx]["Duplicate"] = 1

# Saving the data
with open('dataReady.json', 'w') as outfile2:
    json.dump(data, outfile2, sort_keys=True, indent=4)
