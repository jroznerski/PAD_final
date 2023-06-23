import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px

df = pd.read_csv('pgp_pointed-gun-at-person-details_pgpdetail.csv')

df_phoenix = df[df['INC_CITY'] == 'Phoenix']

zipcodes = df_phoenix['INC_ZIPCODE'].unique().tolist()

geolocator = Nominatim(user_agent='my_heatmap')

locations = []
for zipcode in zipcodes:
    location = geolocator.geocode(zipcode)
    if location is not None:
        coordinates = (location.latitude, location.longitude)
        locations.append(coordinates)

data = pd.DataFrame(locations, columns=['Latitude', 'Longitude'])

fig = px.density_mapbox(data, lat='Latitude', lon='Longitude', radius=10)
fig.update_layout(mapbox_style='open-street-map', mapbox_center={'lat': 33.5, 'lon': -112}, mapbox_zoom=10)

fig.write_html('heatmap.html')