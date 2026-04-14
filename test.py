import os
from dotenv import load_dotenv
import requests

if __name__ == "__main__":

    load_dotenv()

    mapbox_token = os.environ.get("MAPBOX_API_KEY")
    address = "Department of Gastrointestinal Surgery, Guangxi Medical University Cancer Hospital, Nanning, China"
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={mapbox_token}"

    response = requests.get(url)
    data = response.json()

    breakpoint()
    coords = data["features"][0]["center"]
    print(f"Longitude: {coords[0]}, Latitude: {coords[1]}")
