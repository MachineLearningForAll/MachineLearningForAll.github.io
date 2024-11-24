#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 20:24:59 2024

@author: junga1
"""

from fmiopendata.wfs import download_stored_query
import datetime as dt
import matplotlib.pyplot as plt

# Retrieve the latest hour of data from a bounding box
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(hours=10)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z




obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["bbox=19,59.859,32.035,70.170",
                                  "starttime=" + start_time,
                                  "endtime=" + end_time,
                                  "timeseries=True"])

# Extract latitude, longitude, and fmisid
latitudes = []
longitudes = []
fmisids = []
stationname=[]


for station in obs.data.keys():
    metadata = obs.location_metadata.get(station, {})
    lat = metadata.get("latitude")
    lon = metadata.get("longitude")
    fmisid = metadata.get("fmisid")
    

    if lat is not None and lon is not None:
        latitudes.append(lat)
        longitudes.append(lon)
        fmisids.append(fmisid)
        stationname.append(station)

# Plot the stations
plt.figure(figsize=(10, 6))
plt.scatter(longitudes, latitudes, c='blue', alpha=0.7, edgecolors='k')

# Annotate the stations with fmisid
for i, fmisid in enumerate(fmisids):
    plt.text(longitudes[i], latitudes[i], stationname[i], fontsize=9, ha='right')
    
for station in obs.data.keys(): 
    print(obs.location_metadata[station])

formatted_dates = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in obs.data['Kustavi Isokari']['times']]


#print(formatted_dates)

# The times are as a list of datetime objects
times = obs.data['Kustavi Isokari']['times']
# Other data fields have another extra level, one for values and one for the unit
print(len(obs.data['Kustavi Isokari']['Air temperature']['values']))
# -> 71
print(obs.data['Kustavi Isokari']['Air temperature'])
# -> 'degC'

