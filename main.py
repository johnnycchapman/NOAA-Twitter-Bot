import os
import requests
import tweepy
from datetime import datetime

# NOAA Station ID and API URL
STATION_ID = "41013"  # Frying Pan Shoals, NC
NOAA_URL = f"https://www.ndbc.noaa.gov/data/realtime2/{STATION_ID}.txt"

# Twitter API keys from GitHub Actions Secrets
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Setup Twitter authentication
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
twitter = tweepy.API(auth)

def get_noaa_data():
    response = requests.get(NOAA_URL)
    response.raise_for_status()
    lines = response.text.splitlines()
    headers = lines[0].split()
    latest_data = lines[2].split()

    data = dict(zip(headers, latest_data))

    wave_height = data.get('WVHT', 'N/A')  # Wave Height (m)
    water_temp = data.get('WTMP', 'N/A')   # Water Temperature (°C)
    wind_dir = data.get('WDIR', 'N/A')
    wind_speed = data.get('WSPD', 'N/A')

    return wave_height, water_temp, wind_dir, wind_speed

def post_tweet():
    wave_height, water_temp, wind_dir, wind_speed = get_noaa_data()
    now = datetime.now().strftime('%Y-%m-%d')

    tweet = (
        f"🌊 NOAA Marine Conditions for {now} \n"
        f"📍 Station {STATION_ID} \n"
        f"• Wave Height: {wave_height} m\n"
        f"• Water Temp: {water_temp} °C\n"
        f"• Wind: {wind_speed} m/s from {wind_dir}°\n"
        f"#NOAA #Maritime #Weather"
    )

    twitter.update_status(tweet)

if __name__ == "__main__":
    post_tweet()
