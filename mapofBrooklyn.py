import pandas as pd
import folium

import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

wifi = pd.read_csv("NYC_Wi-Fi_Hotspot_Locations.csv",
                   delimiter=',', skiprows=0, low_memory=False)
wifi2 = wifi[['Name', 'Provider', 'Location', 'Latitude', 'Longitude']]
wifi2 = wifi2.rename(
    columns={'Latitude': 'wifiLatitude', 'Longitude': 'wifiLongitude'})

benches = pd.read_csv("City_Bench_Locations.csv", delimiter=',',
                      skiprows=0, low_memory=False)
benches2 = benches[['Address', 'BenchType',
                    'BusRoute', 'Latitude', 'Longitude']]
benches2 = benches2.rename(
    columns={'Latitude': 'benchLatitude', 'Longitude': 'benchLongitude'})


def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    distance_lon = long2 - long1
    distance_lat = lat2 - lat1
    a = sin(distance_lat/2)**2 + cos(lat1) * cos(lat2) * sin(distance_lon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


def find_nearest(lat, long):
    distances = benches2.apply(
        lambda row: dist(
            lat, long, row['benchLatitude'], row['benchLongitude']),
        axis=1)
    return benches.loc[distances.idxmin(), 'Address']


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    # Creating a new column to generate the output by passing lat long information to Haversine Equationmembers['distance'] = [haversine(members.m_lon[i],members.m_lat[i],members.h_lon[i],members.h_lat[i]) for i in range(len(members))]
    return km


df = pd.DataFrame()
wifi3 = wifi2
wifi3['Address'] = wifi2.apply(
    lambda row: find_nearest(row['wifiLatitude'], row['wifiLongitude']),
    axis=1)
wifi3 = pd.merge(
    wifi3, benches2[['Address', 'BenchType',
                    'BusRoute', 'benchLatitude', 'benchLongitude']], on='Address', how='left')

wifi3['distance'] = [haversine(wifi3.benchLongitude[i], wifi3.benchLatitude[i],
                               wifi3.wifiLongitude[i], wifi3.wifiLatitude[i]) for i in range(len(wifi3))]
finaldf = wifi3[wifi3['distance'] < 0.04573]
finaldf = finaldf.drop_duplicates()
print()
# myMap = folium.Map(location=[40.768731, -73.964915])
# for index, row in finaldf.iterrows():
#     lat = row["wifiLatitude"]
#     lon = row["wifiLongitude"]
#     name = 'Wifi Spots + Benches'
#     newMarker = folium.Marker([lat, lon], popup=name)
#     newMarker.add_to(myMap)

# for index, row in benches.iterrows():
#     lat = row["Latitude"]
#     lon = row["Longitude"]
#     name = 'Bench Spots'
#     newMarker = folium.Marker([lat, lon], popup=name,
#                               icon=folium.Icon(color='green'))
#     newMarker.add_to(myMap)


# myMap.save(outfile="myMap2.html")
