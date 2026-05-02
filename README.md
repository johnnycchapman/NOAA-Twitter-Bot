# 🌊 NOAA Twitter Bot 🤖

This bot automatically tweets daily ocean conditions like wave height, water temperature, wind, and high and low tides from NOAA buoy stations — all converted to **imperial units**. Perfect for surfers, sailors, and beach lovers! 🏄‍♂️🚤🌴

## 🛠 Features
- 🌊 Wave height (in feet)
- 🌡 Water temperature (in Fahrenheit)
- 💨 Wind speed (in mph) and direction (degrees)
- 🤖 Automated tweets via GitHub Actions every day at 8:00 AM EST

## 🔧 Setup

1. **Fork or clone** this repo.
2. **Add your Twitter API credentials** as GitHub Repository Secrets:
   - `CONSUMER_KEY`
   - `CONSUMER_SECRET`
   - `ACCESS_TOKEN`
   - `ACCESS_TOKEN_SECRET`
3. *(Optional)* Change the `STATION_ID` in `main.py` to another NOAA buoy station.
4. Commit and push. GitHub Actions will handle the rest.

## 🧪 Example Tweet

```
NOAA Conditions for 11/21/2025
📍 Station: 41013
🌊 Wave Height: 3.5 ft
🌡️  Water Temp: 68.2 °F
💨 Wind: 12.3 mph from SE
⬇️  Low Tides: 3:45am, 4:12pm
⬆️  High Tides: 9:23am, 9:47pm
🌅 Sunset: 5:34pm
#NOAA #WrightsvilleBeachNC
```

## 🧭 Buoy Source
All data is pulled from NOAA’s National Data Buoy Center: [https://www.ndbc.noaa.gov/](https://www.ndbc.noaa.gov/)

## 🖥 Tech Stack
- Python 🐍
- GitHub Actions ⚙️
- Tweepy (Twitter API) 🐦
- Requests (for NOAA data) 🌐

## 📜 License
MIT License — use it, fork it, share it!
