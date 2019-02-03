# asdb_group_proj_bkup
playground.py : extract start point data and zones from database and store as GeoJson
playground.html : display result on a leaflet map

- geojson in the html file is copied and pasted from the python result, not linked by jinja template yet (linking codes are currently comments in the python file)
- coordinates read from database are in projection EPSG:3857, changed to lat-lon in python using pyproj and exported to json 
