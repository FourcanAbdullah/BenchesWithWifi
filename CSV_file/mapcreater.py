"""
Title: Locations with Free Internet, Charging Port and a Bench
URL: https://fourcanabdullah.github.io/BenchesWithWifi/
Name: Fourcan Abdullah
Email: fourcan.abdullah69@myhunter.cuny.edu
Resources: Asked advice from and worked with student:Saiman Tamang. Data from: https://data.cityofnewyork.us/City-Government/NYC-Wi-Fi-Hotspot-Locations/yjub-udmw   https://data.cityofnewyork.us/Transportation/City-Bench-Locations/kuxa-tauh   Other resources used: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/    https://discuss.dizzycoding.com/haversine-formula-in-python-bearing-and-distance-between-two-gps-points/    https://python-visualization.github.io/folium/   https://medium.com/analytics-vidhya/finding-nearest-pair-of-latitude-and-longitude-match-using-python-ce50d62af546    https://gigaom.com/2015/02/01/link-nyc-explained/    https://stjohn.github.io/teaching/data/fall21/work.html    https://stackoverflow.com/    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html



"""

import pandas as pd
import folium
from sklearn.metrics.pairwise import haversine_distances
from math import radians

"""
    csv cleaner is used to clean the given csv files, and it outputs a folium map.
    CSV cleaner takes in the wifi dataset, the bench dataset, and a output file name.
    
"""


def csv_cleaner(wificsv, benchcsv, outputname):
    # reads the wifi csv file
    wifi = pd.read_csv(wificsv,
                       delimiter=',', skiprows=0, low_memory=False)
    # takes the columns Name, Provider, Location, Longitude, Latitude
    wifi2 = wifi[['Name', 'Provider', 'Location', 'Latitude', 'Longitude']]
    # renames the Latitude and Longitude to help tell the diffrerence from bench long and lat
    wifi2 = wifi2.rename(
        columns={'Latitude': 'wifiLatitude', 'Longitude': 'wifiLongitude'})
    # read bench csv
    benches = pd.read_csv(benchcsv, delimiter=',',
                          skiprows=0, low_memory=False)
    # takes the Address, Banchtype, Busroute, Latitude, Longitude columns
    benches2 = benches[['Address', 'BenchType',
                        'BusRoute', 'Latitude', 'Longitude']]
    # rename longitude and latitude to unique names
    benches2 = benches2.rename(
        columns={'Latitude': 'benchLatitude', 'Longitude': 'benchLongitude'})
    # create new dateframe
    wifi3 = wifi2
    # created new column address that holds the address of the benches that is closest to the hotspot
    wifi3['Address'] = wifi2.apply(lambda row: min_distance(
        row['wifiLatitude'], row['wifiLongitude'], benches2), axis=1)
    # left - merged the benches dataframe and the hot spot dataframe based on the address column
    wifi3 = wifi3.merge(
        benches2[['Address', 'BenchType',
                  'BusRoute', 'benchLatitude', 'benchLongitude']],  how='left', on='Address')
    # calcuted the distances between the benches longitude and latitude and wifi longitude and latitude using haversine
    wifi3['distance'] = [haversine_dist(wifi3.benchLongitude[i], wifi3.benchLatitude[i],
                                        wifi3.wifiLongitude[i], wifi3.wifiLatitude[i]) for i in range(len(wifi3))]
    # filtered out the rows that go outside the 150ft wifi limit
    finaldf = wifi3[wifi3['distance'] < 0.04572]
    # droped any duplicate coordinates
    finaldf = finaldf.drop_duplicates()
    # print(finaldf)
    # created folium map
    myMap = folium.Map(location=[40.768731, -73.964915])
    # iterate through all rows and get the longitude and latitude addresses and create markers and add them to the map
    for index, row in finaldf.iterrows():
        lat = row["wifiLatitude"]
        lon = row["wifiLongitude"]
        name = 'Hotspot with Bench: ' + row["Location"]
        newMarker = folium.Marker([lat, lon], popup=name)
        newMarker.add_to(myMap)
    # output a folium map based on the input outputname
    myMap.save(outfile=outputname)

    """haversine_dist is used to find the distance between two points on a sphear
        I used this function to calculate the distace between two points
        from: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html 
    """


def haversine_dist(lon1, lat1,  lon2, lat2,):
    # mapped my lat1, lon1 and lat2 lon2  to radians
    radone = [radians(_) for _ in [lat1, lon1]]
    radtwo = [radians(_) for _ in [lat2, lon2]]
    # used the formula
    result = haversine_distances([radone, radtwo])
    # Radius of earth in kilometers is 6371 so multiplied my km
    kilometers = 6371 * result
    val = 0
    for i in kilometers:
        val = max(i)
    return val

    """min_distance is used to find the minimum distance between the benches lon and lat and the wifi lon and lat
    """


def min_distance(lat, lon, benchframe):
    # used haversine_dist to find distance of each row of the bench dataframe
    alldist = benchframe.apply(
        lambda row: haversine_dist(
            lon, lat, row['benchLongitude'], row['benchLatitude']),
        axis=1)
    # returned the row with the least distance and the address
    return benchframe.loc[alldist.idxmin(), 'Address']

    """hotspot_map is a function with a input csv and a outname
    IT outputs a folium map of all the hotspot LinkNYc locations
    """


def hotspot_map(wificsv, outputname):
    # create a folium map
    myMap = folium.Map(location=[40.768731, -73.964915])
    # reads the given csv
    wifi = pd.read_csv(wificsv,
                       delimiter=',', skiprows=0, low_memory=False)
    # marks the lat and lon points on the map with the location
    for index, row in wifi.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]
        name = 'Hotspot: ' + row['Location']
        newMarker = folium.Marker([lat, lon], popup=name,
                                  icon=folium.Icon(color='green'))
        newMarker.add_to(myMap)
    # outputs the html folium map with the outputname
    myMap.save(outfile=outputname)

    """the below code was used to run the functions
    """


csv_cleaner('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Brooklyn.csv',
            "CSV_file/City_Bench_Locations_Brooklyn.csv", 'Maps/BrooklynMap.html')
csv_cleaner('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Manhatten.csv',
            "CSV_file/City_Bench_Locations_Manhatten.csv", 'Maps/ManhattenMap.html')
csv_cleaner('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Bronx.csv',
            "CSV_file/City_Bench_Locations_Bronx.csv", 'Maps/BronxMap.html')
csv_cleaner('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Queens.csv',
            "CSV_file/City_Bench_Locations_Queens.csv", 'Maps/QueensMap.html')
csv_cleaner('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Staten_Island.csv',
            "CSV_file/City_Bench_Locations_Staten_Island.csv", 'Maps/Staten_IslandMap.html')

hotspot_map('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Brooklyn.csv',
            'Maps/BrooklynHotspotMap.html')
hotspot_map('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Manhatten.csv',
            'Maps/ManhattenHotspotMap.html')
hotspot_map('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Bronx.csv',
            'Maps/BronxHotspotMap.html')
hotspot_map('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Queens.csv',
            'Maps/QueensHotspotMap.html')
hotspot_map('CSV_file/NYC_Wi-Fi_Hotspot_Locations_Staten_Island.csv',
            'Maps/Staten_IslandHotspotMap.html')
