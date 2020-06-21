#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: lucyrothwell
"""
import pandas as pd # For  data manipulation
import numpy as np # For ML algorithms

# Load your files and sample rate

# Loads the data csv file.
# *NOTE*: This programme assumes column 1 of this sheet is the timings
data_file_name = 'data_time_series_18PWS(S).csv' # This will also be
# # used for your labelled output file
data = pd.read_csv(data_file_name, encoding='utf-8', skiprows=0)

# Load event start and finish times doc. I.e., your csv where each row holds [start_time, end_time] of events.
events = pd.read_csv("event_durations_18PWS(S).csv", encoding='utf-8', skiprows=1)

# Your sample rate (ie seconds, deciseconds)
sample_rate = 0.1 # Deciseconds

# ************ NOTHING ELSE NEEDS EDITED FROM HERE ***************
#            (unless further customisation is needed)

# Function for extracting each decisecond in the stutter ranges extracted
# PSEUDO:
# > Take start time of R0,C0 (row 0, column 0)
# > Take end time of R0,C1 (row 0, column 1)
# > Extract range between R0,C0 and R0,C1, and write (apend) it into "labels" doc

def addRange (events):
    print("Running...")
    global events_split # A new df which will hold the data split into secs/decisecs
    events_split = pd.DataFrame()
    events = np.array(events)
    row = 0
    for _row in events:
        x = round(events[row,0],1) # Start time
        y = round(events[row,1],1) # End time
        events_split = events_split.append(pd.DataFrame([x]))
        while x < y:
            x = round((x + sample_rate),1)
            events_split = events_split.append(pd.DataFrame([x]))
        row = row + 1
    return events_split
addRange(events)

# PSEUDO
# Function for turning stutter labels into a column of 1s and 0s
# Take R1-C0 in data
# If the number exists in labels, then print "1" in R1-C0 in stutterList.
# If not print "0" in R1-C1 in stutterList and go to R2-C0 in data.
# Then take R2-C1 in data
# If the number exists in Labels, then print "1" in R2-C0 in stutterList.
# If not print "0" in R2-C0 in stutterList and go to R3-C0 in data.

# Create a variable containing the sampling times of your data
data_time_col = pd.DataFrame([data.iloc[:,0]])
data_time_col = data_time_col.T

# Function to create a column of 1s and 0s, corresponding to the sampling times
def addEvents(data_time_col):
    global labels_01_df
    labels_01_df = pd.DataFrame() # Create new csv to record the labels
    for i in data_time_col.values:
        if i in events_split.values:
            labels_01_df = labels_01_df.append([1], ignore_index=True)
        else:
            labels_01_df = labels_01_df.append([0], ignore_index=True)
    return labels_01_df

addEvents(data_time_col)

# for i in data_time_col.values:
#     print(i)

# Insert labels column into data dataframe
data.insert(loc=0, column="labels", value=labels_01_df)
data.to_csv(data_file_name + " - LABELLED.csv", index=False) # Convert dataframe back to csv
print("Done!")

# You should now have a file in your directory titled "[original data file name] - LABELLED".