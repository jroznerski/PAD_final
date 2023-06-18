import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px

# Wczytaj plik CSV
df = pd.read_csv('pgp_pointed-gun-at-person-details_pgpdetail.csv')

# Filtruj dane dla miasta Phoenix
df_phoenix = df[df['INC_CITY'] == 'Phoenix']

# Utwórz unikalną listę kodów pocztowych
zipcodes = df_phoenix['INC_ZIPCODE'].unique().tolist()

# Inicjalizuj geokoder Nominatim
geolocator = Nominatim(user_agent='my_heatmap')

# Przekształć kody pocztowe na współrzędne geograficzne
locations = []
for zipcode in zipcodes:
    location = geolocator.geocode(zipcode)
    if location is not None:
        coordinates = (location.latitude, location.longitude)
        locations.append(coordinates)

# Utwórz DataFrame z danymi geolokalizacyjnymi
data = pd.DataFrame(locations, columns=['Latitude', 'Longitude'])

# Wygeneruj mapę ciepła
fig = px.density_mapbox(data, lat='Latitude', lon='Longitude', radius=10)
fig.update_layout(mapbox_style='open-street-map', mapbox_center={'lat': 33.5, 'lon': -112}, mapbox_zoom=10)

# Zapisz mapę do pliku HTML
fig.write_html('heatmap.html')