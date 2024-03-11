#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 12:03:26 2022

@author: eebjs
"""

from meteostat import Stations, Hourly
from datetime import datetime
import matplotlib.pyplot as plt


# Get nearby weather stations
stations = Stations()
stations = stations.nearby(53.7953, -1.5455).fetch(5)

print(stations)

# We can use the Leeds Bradford Airport data ('EGNM0')

# Set time period
start = datetime(2016, 1, 1)
end = datetime(2024, 3, 6)

# Get hourly data
data = Hourly('EGNM0', start, end)
data = data.fetch()

data.to_csv('./weather_data/LBA_weather_data.csv')