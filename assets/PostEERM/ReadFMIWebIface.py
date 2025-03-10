#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 20:24:59 2024

@author: junga1
"""

from fmiopendata.wfs import download_stored_query
import datetime as dt
import matplotlib.pyplot as plt
import random
import geopandas as gpd
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist



# Rounded polygon vertices
polygon_vertices = [
    (59.375, 20.285), (60.388, 20.179), (60.607, 20.973), (60.911, 21.530),
    (60.906, 21.463), (61.343, 22.503), (61.683, 22.546), (62.929, 22.919),
    (63.101, 24.282), (63.646, 24.778), (63.396, 25.100), (64.782, 25.075),
    (65.082, 25.348), (64.900, 26.413), (65.307, 26.648), (65.746, 26.810),
    (66.304, 27.662), (66.962, 27.680), (67.307, 29.034), (67.604, 28.863),
    (68.362, 29.746), (68.327, 29.874), (68.917, 30.562), (69.429, 31.068),
    (69.956, 31.185), (69.956, 31.185), (69.429, 31.068), (68.917, 30.562),
    (68.327, 29.874), (68.362, 29.746), (67.604, 28.863), (67.307, 29.034),
    (66.962, 27.680), (66.304, 27.662), (65.746, 26.810), (65.307, 26.648),
    (64.900, 26.413), (65.082, 25.348), (64.782, 25.075), (63.396, 25.100),
    (63.646, 24.778), (63.101, 24.282), (62.929, 22.919), (61.683, 22.546),
    (61.343, 22.503), (60.906, 21.463), (60.911, 21.530), (60.607, 20.973),
    (60.388, 20.179), (59.375, 20.285)
]

polygon_latitudes, polygon_longitudes = zip(*polygon_vertices)

# Retrieve the latest hour of data from a bounding box
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(hours=1)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z



# the code snippet below reads in data from web interface 

bbox="19,59.859,32.035,70.170"  #   for entire finlan 

#bbox = 21.02, 60.7, 21.03, 60.73 for Kustavi Isokaari


obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["bbox="+bbox,
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


# Combine latitudes and longitudes into a single array for clustering
coordinates = np.array(list(zip(latitudes, longitudes)))

# Define the number of clusters based on the sample size (20% of stations)
sample_size = int(len(coordinates) * 0.1)
kmeans = KMeans(n_clusters=sample_size, random_state=42)
kmeans.fit(coordinates)

# Find the station closest to the cluster mean for each cluster
sample_indices = []
for cluster_label in range(sample_size):
    # Get the indices of all points in the current cluster
    cluster_points = np.where(kmeans.labels_ == cluster_label)[0]
    
    # Calculate distances of all cluster points to the cluster centroid
    cluster_center = kmeans.cluster_centers_[cluster_label]
    distances = cdist([cluster_center], coordinates[cluster_points])
    
    # Find the index of the closest point
    closest_index_within_cluster = cluster_points[np.argmin(distances)]
    sample_indices.append(closest_index_within_cluster)

# Subset the data
sample_longitudes = [longitudes[i] for i in sample_indices]
sample_latitudes = [latitudes[i] for i in sample_indices]
sample_stationname = [stationname[i] for i in sample_indices]


# # Plot the stations
# plt.figure(figsize=(10, 6))
# plt.scatter(longitudes, latitudes, c='blue', alpha=0.7, edgecolors='k')

# # Annotate the stations with fmisid
# for i, fmisid in enumerate(fmisids):
#     #plt.text(longitudes[i], latitudes[i], str(i), fontsize=9, ha='right')
#     plt.text(longitudes[i], latitudes[i], stationname[i], fontsize=9, ha='right')
    
for station in obs.data.keys(): 
    print(obs.location_metadata[station])

formatted_dates = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in obs.data['Kustavi Isokari']['times']]


plt.figure(figsize=(10, 8))
    

    #plt.plot(polygon_longitudes, polygon_latitudes, c='red', linewidth=2, label="Polygon Approximation of Finland")
plt.scatter(sample_longitudes, sample_latitudes, c='blue', alpha=1, s=100, edgecolors='k')

    # Annotate the stations with their names
for i, name in enumerate(sample_stationname):
    plt.text(sample_longitudes[i], sample_latitudes[i]+0.2, name.split()[0], fontsize=15, ha='right')
        
    # Remove axes
plt.axis('off')
plt.savefig("FMIStations.png", dpi=100)
plt.show()



#print(formatted_dates)

# The times are as a list of datetime objects
times = obs.data['Kustavi Isokari']['times']
# Other data fields have another extra level, one for values and one for the unit
print(len(obs.data['Kustavi Isokari']['Air temperature']['values']))
# -> 71
print(obs.data['Kustavi Isokari']['Air temperature'])
# -> 'degC'

