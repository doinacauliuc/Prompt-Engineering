from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="geoapi")

indirizzi = [
    "Chiozzola di Taro"

]

for ind in indirizzi:
    try:
        location = geolocator.geocode(ind)
        if location:
            print(ind, "->", (location.latitude, location.longitude))
        else:
            print(ind, "-> non trovato")
        time.sleep(1)  # per non stressare il server
    except Exception as e:
        print(ind, "-> errore:", e)
