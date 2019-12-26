#! /usr/bin/env python

"""
This program polls the open-notify API repeatedly to calculate the current
speed of the international space station and prints it to standard output
in a DataFrame format

Author: Jyoti C Dingle
"""

# -----------------------------------
# Import required modules
# -----------------------------------
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import time
import sys

# -----------------------------------
# Define Constants
# -----------------------------------
TIME_DURATION = 15 # seconds
POLLING_INTERVAL = 5 # seconds
RADIUS_OF_EARTH = 6371 # km
AVG_ISS_ALTITUDE = 400 # km

# -------------------------------------
# Read optional command line arguments
# -------------------------------------
if len(sys.argv) > 1: TIME_DURATION = sys.argv[1]
if len(sys.argv) > 2: POLLING_INTERVAL = int(sys.argv[2])

def get_coordinates():
    """
    This method opens the url & reads the json response every POLLING_INTERVAL
    seconds for maximum TIME_DURATION specified.
    Populates dictionary with incoming parameter values for following keys
        - Timestamp
        - Latitude
        - Longitude

    :return: Dictionary with populated data.
    """
    resp_dict={'Timestamp':[],'Latitude':[],'Longitude':[]}
    start_time = time.time()
    while ((time.time() - start_time) < float(TIME_DURATION)):
        url = ("http://api.open-notify.org/iss-now.json")
        response = urlopen(url)
        obj = json.loads(response.read())
        print("Reading incoming response...", obj)
        resp_dict['Timestamp'].append(obj['timestamp'])
        resp_dict['Latitude'].append(obj['iss_position']['latitude'])
        resp_dict['Longitude'].append(obj['iss_position']['longitude'])
        time.sleep(POLLING_INTERVAL)
    return resp_dict

def cal_distance(resp_df):
    """
    This method uses the Haversine Formula to calculate the distance
    between 2 consecutive points of ISS positions mentioned in resp_df
    :param resp_df: Pandas DataFrame with 3 columns:
        - Timestamp
        - Latitude
        - Longitude
    :return: resp_df DataFrame with 3 additional columns,
        - Diff_Lon
        - Diff_Lat
        - Distance
    """
    # Converting position values to radians
    resp_df['Latitude'] = resp_df['Latitude'].astype(float)
    resp_df['Longitude'] = resp_df['Longitude'].astype(float)
    resp_df['Latitude'] = np.deg2rad(resp_df['Latitude'])
    resp_df['Longitude'] = np.deg2rad(resp_df['Latitude'])

    # Calculate diff between current & last point
    resp_df['Diff_Lon'] = resp_df['Longitude'].diff(+1)
    resp_df['Diff_Lat'] = resp_df['Latitude'].diff(+1)

    # Haversine Formula
    # a is the square of half the chord length between the points.
    a = np.sin(resp_df['Diff_Lat'] / 2)**2 + np.cos(resp_df['Latitude']) * np.cos(resp_df['Latitude']) * np.sin(resp_df['Diff_Lon']/ 2)**2

    # c is the angular distance in radians.
    c = 2 * np.arcsin(np.sqrt(a))

    # Calculate the distance between successive points
    resp_df['Distance(km)'] = c * (RADIUS_OF_EARTH + AVG_ISS_ALTITUDE)
    return resp_df

# -----------------------------------
# MAIN
# -----------------------------------
coord_dict = get_coordinates()
resp_df = pd.DataFrame.from_dict(coord_dict)
cal_distance(resp_df)

# Calculate Speed of ISS between 2 consecutive positions
resp_df['Speed(km/hr)']= resp_df['Distance(km)']/(POLLING_INTERVAL/3600)

#Saving the dataframe to csv file
file_ts = time.time()
file_name = str(int(file_ts)) + "_iss_data.csv"
resp_df.to_csv(file_name)
Average_Speed = resp_df['Speed(km/hr)'].mean()

print("\n\n\t\t\t\t-------- Response DataFrame --------\n")
print(resp_df)
print("Average Speed of ISS is : {} km/hr".format(round(Average_Speed,6)))
