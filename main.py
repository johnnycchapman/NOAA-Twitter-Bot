import os
import requests
from requests_oauthlib import OAuth1Session
from datetime import datetime

# NOAA Buoy Station
STATION_ID = "41013"
NOAA_URL = f"https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt"

# NOAA CO-OPS Station for tide data (nearest to buoy 41013 - Frying Pan Shoals, NC)
# Station 8658163 - Wrightsville Beach, NC
TIDE_STATION_ID = "8658163"

# Twitter OAuth1 credentials
CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

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

def get_tide_data():
    """Fetch today's high and low tides from NOAA CO-OPS API"""
    try:
        today = datetime.now().strftime('%Y%m%d')
        url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        params = {
            'product': 'predictions',
            'application': 'NOS.COOPS.TAC.WL',
            'begin_date': today,
            'end_date': today,
            'datum': 'MLLW',
            'station': TIDE_STATION_ID,
            'time_zone': 'lst_ldt',
            'units': 'english',
            'interval': 'hilo',
            'format': 'json'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'predictions' not in data:
            return None, None

        high_tide = None
        low_tide = None

        for prediction in data['predictions']:
            time_str = prediction['t']
            tide_type = prediction['type']

            # Parse time and convert to 12-hour format
            tide_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            formatted_time = tide_time.strftime('%-I:%M%p').lower()

            if tide_type == 'H' and not high_tide:
                high_tide = formatted_time
            elif tide_type == 'L' and not low_tide:
                low_tide = formatted_time

        return high_tide, low_tide
    except Exception as e:
        print(f"Error fetching tide data: {e}")
        return None, None

def post_tweet():
    data = get_noaa_data()
    if not data:
        print("Failed to retrieve or parse NOAA data.")
        return

    wave_height, water_temp, wind_dir, wind_speed = data
    high_tide, low_tide = get_tide_data()
    now = datetime.now().strftime('%-m/%-d/%Y')

    tweet = (
        f"🌊 NOAA Marine Conditions for {now}\n"
        f"📍 Station {STATION_ID}\n"
        f"🌊 Wave Height: {wave_height} ft\n"
        f"🌡️ Water Temp: {water_temp} °F\n"
        f"💨 Wind: {wind_speed} mph from {wind_dir}°\n"
    )

    if high_tide:
        tweet += f"⬆️ High Tide: {high_tide}\n"
    if low_tide:
        tweet += f"⬇️ Low Tide: {low_tide}\n"

    tweet += "#NOAA #Maritime #Weather"

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
