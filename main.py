import os
import requests
import tweepy
from datetime import datetime

# NOAA Station ID and API URL
STATION_ID = "41013"  # Frying Pan Shoals, NC
NOAA_URL = f"https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt"

# Twitter API keys from GitHub Actions Secrets
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Setup Twitter v2 client
twitter_client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

def get_noaa_data():
    response = requests.get(NOAA_URL)
    response.raise_for_status()
    lines = response.text.splitlines()
    headers = lines[0].split()
    latest_data = lines[2].split()

    data = dict(zip(headers, latest_data))

    wave_height_m = data.get('WVHT', 'N/A')
    water_temp_c = data.get('WTMP', 'N/A')
    wind_dir = data.get('WDIR', 'N/A')
    wind_speed_ms = data.get('WSPD', 'N/A')

    try:
        wave_height_ft = round(float(wave_height_m) * 3.28084, 1)
    except:
        wave_height_ft = 'N/A'

    try:
        water_temp_f = round((float(water_temp_c) * 9/5) + 32, 1)
    except:
        water_temp_f = 'N/A'

    try:
        wind_speed_mph = round(float(wind_speed_ms) * 2.23694, 1)
    except:
        wind_speed_mph = 'N/A'

    return wave_height_ft, water_temp_f, wind_dir, wind_speed_mph

def post_tweet():
    wave_height, water_temp, wind_dir, wind_speed = get_noaa_data()
    now = datetime.now().strftime('%Y-%m-%d')

    tweet = (
        f"🌊 NOAA Marine Conditions for {now}\n"
        f"📍 Station {STATION_ID}\n"
        f"• Wave Height: {wave_height} ft\n"
        f"• Water Temp: {water_temp} °F\n"
        f"• Wind: {wind_speed} mph from {wind_dir}°\n"
        f"#NOAA #Maritime #Weather"
    )

    twitter_client.create_tweet(text=tweet)

if __name__ == "__main__":
    post_tweet()
