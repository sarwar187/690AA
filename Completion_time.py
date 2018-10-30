import numpy as np  
import random
import sys
from scipy.optimize import linprog
import copy

N=int(raw_input("Number of jobs: "))
release_time=[int(x) for x in raw_input("Enter the release times of the jobs separated by space: ").split()]
processing_time=[int(x) for x in raw_input("Enter the processing times of the jobs separated by space: ").split()]
jobs=np.arange(N)

#SRPT algorithm

jobs_completed=[] #keeps track of completed jobs and its order  
jobs_available=[] #keeps track of available jobs to schedule
release_time_copy=copy.copy(release_time) # copy of release time array
SRPT={} #keeps track of Shortest Remaining Processing time for available jobs
running_job=None
time_start=min(release_time) #keeps track of the last time a job was started/changed
for i in range(len(set(release_time_copy))):
    time_final=min(release_time) #keeps track of current time
    jobs_available=jobs_available+[x for x in jobs if release_time_copy[x]==time_final]
    for x in jobs:
        if release_time_copy[x]==time_final:
            SRPT[x]=processing_time[x]
    while(time_final in release_time):
       release_time.remove(time_final)
    if (running_job!=min(SRPT, key=SRPT.get)):
       previous_job=running_job    
       running_job=min(SRPT, key=SRPT.get)
    if (previous_job!=None):
       SRPT[previous_job]-=time_final-time_start
    if (len(release_time)==0 or time_final+SRPT[running_job]<=min(release_time)):   
        if(len(release_time)!=0):
            while(time_final+SRPT[running_job]<=min(release_time) and len(jobs_available)>=1):
               time_start=time_final
               jobs_completed.append(running_job)
               jobs_available.remove(running_job)
               del SRPT[running_job]
               if(len(jobs_available)==0):
                   running_job=None;time_start=min(release_time)
                   break   
               running_job=min(SRPT, key=SRPT.get)
               time_final=time_final+SRPT[running_job]
        else:
            while(len(jobs_completed)!=N):
               jobs_completed.append(running_job)
               jobs_available.remove(running_job)
               del SRPT[running_job]
               if(len(jobs_available)==0):
                   break      
               running_job=min(SRPT, key=SRPT.get)

objective=0 #calculates the final objective value
for i in range(len(jobs_completed)):
    if(release_time_copy[jobs_completed[i]]>objective):
        objective+=release_time_copy[jobs_completed[i]]+processing_time[jobs_completed[i]]
    else:
        objective+=objective+processing_time[jobs_completed[i]] 

print objective            







