# 🌊 NOAA Twitter Bot 🤖

This bot automatically tweets daily ocean conditions like wave height, water temperature, wind, and high and low tides from NOAA buoy stations — all converted to **imperial units**. Perfect for surfers, sailors, and beach lovers! 🏄‍♂️🚤🌴

## 🛠 Features
- 🌊 Wave height (in feet) — sourced from the **Stormglass Weather API** at the surf spot (Wrightsville Beach: `34.192607, -77.803778`), converted from meters
- 🌡 Water temperature (in Fahrenheit)
- 💨 Wind speed (in mph) and direction (degrees)
- 🤖 Automated tweets every day at 7:00 AM Eastern

## 🔧 Setup

1. **Fork or clone** this repo.
2. **Add your Twitter API credentials** as GitHub Repository Secrets:
   - `CONSUMER_KEY`
   - `CONSUMER_SECRET`
   - `ACCESS_TOKEN`
   - `ACCESS_TOKEN_SECRET`
   - `STORMGLASS_API_KEY` — your [Stormglass.io](https://stormglass.io/) API key (free tier available), used for wave height
3. *(Optional)* Change the `STATION_ID` in `main.py` to another NOAA buoy station.
4. Commit and push. GitHub Actions will handle the rest.

## ⏰ How it works

The bot runs **every day at 7:00 AM Eastern**, scheduled externally by [cron-job.org](https://cron-job.org/). Because cron-job.org is timezone-aware (`America/New_York`), the 7:00 AM run holds year-round through both EST and EDT — no DST handling needed inside the repo.

At the scheduled time, cron-job.org sends an authenticated POST to GitHub's workflow-dispatch REST API, which triggers the `schedule.yml` workflow on the `main` branch. GitHub Actions then checks out the repo, installs dependencies, and runs `main.py` to gather the data and post the tweet.

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

## 🧭 Data Sources
- Water temp, wind, and buoy metadata from NOAA’s National Data Buoy Center: [https://www.ndbc.noaa.gov/](https://www.ndbc.noaa.gov/)
- Wave height from the Stormglass Weather API: [https://stormglass.io/](https://stormglass.io/)
- Tides from NOAA CO-OPS; sunset from sunrise-sunset.org

## 🖥 Tech Stack
- Python 🐍
- GitHub Actions ⚙️
- Tweepy (Twitter API) 🐦
- Requests (for NOAA data) 🌐
- Stormglass Weather API (for wave height) 🌊

## 📜 License
MIT License — use it, fork it, share it!
