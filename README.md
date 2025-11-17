# 🌊 NOAA Twitter Bot 🤖

This bot automatically tweets daily ocean conditions like wave height, water temperature, and wind from NOAA buoy stations — all converted to **imperial units**. Perfect for surfers, sailors, and beach lovers! 🏄‍♂️🚤🌴

## 🛠 Features
- 🌊 Wave height (in feet)
- 🌡 Water temperature (in Fahrenheit)
- 💨 Wind speed (in mph) and direction (degrees)
- 🤖 Automated tweets via GitHub Actions every day at 8:00 AM EST

## 🔧 Setup

1. **Fork or clone** this repo.
2. **Add your Twitter API credentials** as GitHub Repository Secrets:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
3. *(Optional)* Change the `STATION_ID` in `main.py` to another NOAA buoy station.
4. Commit and push. GitHub Actions will handle the rest.

## 🧪 Example Tweet

```
 NOAA Marine Conditions for 6/29/2025
📍 Station 41013 
🌊 Wave Height: 2.0 ft
🌡️ Water Temp: 78.8 °F
💨 Wind: 10.1 mph from 180°
⬆️ High Tide: 6:01pm
⬇️ Low Tide: 8:12am
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
