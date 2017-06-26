"""Isochrone creator.

This tool allows a user to pass a CSV containing latitude and longitude
coordinates to Mapzen's Isochrone API. This returns a GeoJSON file of
isochrones based on a user-definted time and transport type (pedestrian,
bicycle, and multimodal). It also includesan option to open the output in
geojson.io

"""

import pandas as pd
import requests
import time
from datetime import datetime
import json
import geojsonio
import fire


def isochroner(
                data,
                key,  # mapzen-3iGEB8a
                lat_field,
                lon_field,
                id_field=None,
                travel_type='pedestrian',
                polygons='true',
                travel_time=10,
                to_geojsonio=False
):
    """Isochroner function.

    This function takes the user inputs and passes them to the Mapzen
    API. It then creates a GeoJSON output and optionally opens that output in
    geojson.io

    """
    valid = True
    while valid:
        travel_types = ['bicycle', 'pedestrian', 'multimodal']
        if travel_type not in travel_types:
            print(travel_type, "is not a valid input for travel_type.")
            print('Select from', travel_types)
            valid = False

        # Read in a CSV of locations from which to generate isochrones
        df = pd.read_csv(data)

        # Create and empty list into which isochrones should be placed
        isochrone_list = []

        # Hit the Mapzen Isochrone API for each point
        i = 0
        while i < len(df):
            if id_field is not None:
                id_field = i
            val = df.iloc[i, ]

            query_dict = {
                "locations": [{
                    "lat": val[lat_field],
                    "lon": val[lon_field]
                }],
                "costing": travel_type,
                "contours": [{
                    "time": travel_time
                }],
                "polygons": polygons,

            }

            query_str = str(query_dict).strip().replace(" ", "").replace("'", "\"")

            payload = {
                "id": id_field,
                "api_key": key
            }

            print("query_str:", type(query_str))
            id_str = '&id=' + str(id_field)
            print("id_str:", type(id_str))
            key_str = '&api_key=' + key
            print("key_str:", type(key_str))

            api_call = 'http://matrix.mapzen.com/isochrone?json=' + query_str
            print("api_call:", api_call)
            response = requests.get(api_call, params=payload)
            print("Response URL:", response.url)
            response_json = response.json()
            isochrone = response_json["features"][0]
            # Append response_json to response_list
            isochrone_list.append(isochrone)
            i += 1
            time.sleep(1)
        isochrones = {"type": "FeatureCollection", "features": isochrone_list}

        if to_geojsonio:
            geojsonio.display(json.dumps(isochrones))

        # Save isochrones to GeoJSON file
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        with open('isochrones_{}.geojson'.format(current_time), 'w') as outfile:
                json.dump(isochrones, outfile)

        valid = False


if __name__ == '__main__':
    fire.Fire(isochroner)
