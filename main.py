import os
import requests
from requests_oauthlib import OAuth1Session
from datetime import datetime

# NOAA Station
STATION_ID = "41013"
NOAA_URL = f"https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt"

# Twitter OAuth1 credentials
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

def get_noaa_data():
    response = requests.get(NOAA_URL)
    response.raise_for_status()
    lines = response.text.splitlines()
    headers = lines[0].split()

    for line in lines[2:]:
        values = line.split()
        if len(values) != len(headers):
            continue
        data = dict(zip(headers, values))
        if all(data.get(k, 'MM') != 'MM' for k in ['WVHT', 'WTMP', 'WDIR', 'WSPD']):
            try:
                wave_height_ft = round(float(data['WVHT']) * 3.28084, 1)
                water_temp_f = round(float(data['WTMP']) * 9 / 5 + 32, 1)
                wind_speed_mph = round(float(data['WSPD']) * 2.23694, 1)
                wind_dir = data['WDIR']
                return wave_height_ft, water_temp_f, wind_dir, wind_speed_mph
            except Exception as e:
                print("Error parsing data:", e)
                return None
    print("No complete NOAA data available.")
    return None

def post_tweet():
    data = get_noaa_data()
    if not data:
        print("Failed to retrieve or parse NOAA data.")
        return

    wave_height, water_temp, wind_dir, wind_speed = data
    now = datetime.now().strftime('%Y-%m-%d')

    tweet = (
        f"🌊 NOAA Marine Conditions for {now}\n"
        f"📍 Station {STATION_ID}\n"
        f"• Wave Height: {wave_height} ft\n"
        f"• Water Temp: {water_temp} °F\n"
        f"• Wind: {wind_speed} mph from {wind_dir}°\n"
        f"#NOAA #Maritime #Weather"
    )

    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_SECRET
    )

    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": tweet}
    )

    if response.status_code != 201:
        raise Exception(f"Tweet failed: {response.status_code} {response.text}")

    print("Tweet posted successfully!", response.json())

if __name__ == "__main__":
    post_tweet()
