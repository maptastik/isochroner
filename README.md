# isochroner.py

A Python command-line tool for generating GeoJSON isochrones of a set of locations via Mapzen's Isochrone API.

## Dependencies

- pandas
- requests
- geojsonio
- [Python Fire](https://github.com/google/python-fire)

## Command Line Interface

Currently, isochroner.py relies on Google's Python Fire to allow for interaction at the command line.

### Arguments

isochroner.py accepts several arguments to customize your command (Required arguments are **bold**)

- **data**: CSV of data points you want to generate isochrones from
- **key**: Mapzen API key. If you don't have one, create a [Mapzen](https://mapzen.com) account and create one.
- **lat_field**: name of the field in your CSV that contains the latitude coordinates
- **lon_field**: name of the field in your CSV that contains the longitude coordinates
- id_field: If you have some sort of attribute you'd like to pass as an ID, specify the field here (*Default: None*)
- travel type: Mode of transportation. Must be `bicycle`, `pedestrian`, or `pedestrian` (*Default: pedestrian*)
- polygons: Specify if the output will polygons or polylines (*Default: true*)
- travel_time: Travel time for each isochrone from each point in the CSV (*Default: 10*)
- to_geojsonio: Open up output GeoJSON isochrones in geojson.io (*Default: False*)

### Example(s)
These examples use `data.csv` from this repo

#### Basic Example
```bash
python isochroner.py data.csv mapzen-XXXXXX Y X
```
