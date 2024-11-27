#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 09:35:07 2024

@author: junga1
"""

import requests

import requests

# Corrected URL with valid outputFormat
url = (
    "https://opendata.fmi.fi/wfs?"
    "service=WFS&"
    "request=GetFeature&"
    "version=2.0.0&"
    "TYPENAMES=omso:GridSeriesObservation&"
    "bbox=24.9354,60.1695,25.9354,61.1695,EPSG:4326&"
    "time=2024-11-01T00:00:00Z/2024-11-01T23:59:59Z&"
    "outputFormat=application/gml+xml; subtype=gml/3.2"
)

try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Data retrieved successfully!")
        print(response.text)  # Print the raw GML/XML response
    else:
        print(f"Error: {response.status_code}")
        print(response.text)  # Print the error message
except requests.RequestException as e:
    print(f"Request failed: {e}")
