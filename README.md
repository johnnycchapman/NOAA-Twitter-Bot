# 🌊 NOAA Twitter Bot 🤖

This bot automatically tweets daily ocean conditions like wave height, water temperature, and wind from NOAA buoy stations. It’s perfect for surfers, sailors, and marine enthusiasts! 🚤🌤

## 🛠 Features
- Gets latest data from NOAA buoy station (default: Frying Pan Shoals, NC).
- Posts a daily tweet every morning at 8:00 AM EST.
- Deployed via GitHub Actions ⏰✅

## 🔧 Setup

1. Clone this repo.
2. Add your Twitter API credentials as **GitHub Secrets**:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
3. Customize `STATION_ID` in `main.py` if you'd like to change the location.
4. Push to GitHub – Actions will run every day.

## 🧪 Example Tweet

```
🌊 NOAA Marine Conditions for 2025-06-19 
📍 Station 41013 
• Wave Height: 0.6 m
• Water Temp: 26.1 °C
• Wind: 4.5 m/s from 180°
#NOAA #Maritime #Weather
```

## 📜 License

MIT License
