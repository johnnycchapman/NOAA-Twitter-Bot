# 🌊 WBNC Surf Bot 🤖

Automated daily X (Twitter) bot that posts NOAA buoy observations, tide
predictions, and sunset time for Wrightsville Beach, NC — all in imperial units.
Perfect for surfers, sailors, and beach lovers! 🏄‍♂️🚤🌴

Live at: [@WBNCSurfBot](https://x.com/WBNCSurfBot)

## 🛠 Features

- 🌊 Wave height (ft) from NDBC Buoy 41013 (Frying Pan Shoals)
- 🌡 Water temperature (°F)
- 💨 Wind speed (mph) and cardinal direction
- 🌙 High and low tides from CO-OPS Station 8658163 (Wrightsville Beach)
- 🌅 Sunset time (sunrise-sunset.org)

## 🤖 How it runs

The bot posts daily at **7:00 AM Eastern year-round**, automatically tracking the
EST/EDT switch.

GitHub Actions cron is always UTC and has no timezone support, so the workflow
uses **two daily crons** — `47 10 * * *` and `47 11 * * *` — one for each Eastern
offset. A `gate` job reads the live `America/New_York` UTC offset at runtime and
lets through only the cron that maps to 7 AM Eastern that day, skipping the other.

Both crons fire ~13 minutes early (06:47 ET) on an off-peak minute. This is
deliberate: GitHub's scheduled runs are best-effort and fire late (never early),
with the worst delays at the top of the hour. Firing early on an off-minute
absorbs that delay, and a **wait step then sleeps until exactly 07:00:00 Eastern**
before posting, so the tweet lands within a few seconds of 7:00. If GitHub is
delayed past 07:00 on a given day, the wait is a no-op and the bot posts as soon
as the runner picks it up.

`workflow_dispatch` allows manual triggering, which skips the wait and posts
immediately.

Each successful run appends a timestamped entry to `data/run-log.txt` and commits
it back to the repo — this both produces a useful history *and* prevents the
workflow from being auto-disabled by GitHub's 60-day scheduled-workflow
inactivity rule.

## 🔧 Setup

### GitHub repository secrets

Set these four values under Settings → Secrets and variables → Actions:

- `CONSUMER_KEY`
- `CONSUMER_SECRET`
- `ACCESS_TOKEN`
- `ACCESS_TOKEN_SECRET`

These names must match the `secrets.*` references in the workflow `env:` block
and the `os.getenv(...)` calls in `main.py` — all three use the `CONSUMER_*` /
`ACCESS_TOKEN*` prefix.

All four must come from the same X app under an active (non-deprecated) Project,
and the Access Token / Secret must be generated **after** the app permissions are
set to "Read and Write."

### X Developer account requirements

- Project on the Pay-Per-Use tier (the legacy Free tier is deprecated)
- App with User Authentication configured, Read and Write permissions
- App type: "Web App, Automated App or Bot"
- Callback URI: any valid URL (e.g. `https://x.com`)
- Access Token & Secret regenerated AFTER permissions were set to Read/Write
- Pre-loaded credits in the developer console (~$0.15 per post)

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
#NOAA #WrightsvilleBeach #Wilmington
```

## 💻 Local development

```bash
pip install -r requirements.txt
export CONSUMER_KEY="..."
export CONSUMER_SECRET="..."
export ACCESS_TOKEN="..."
export ACCESS_TOKEN_SECRET="..."
python main.py
```

## 🧭 Data Source

All buoy data is pulled from NOAA's National Data Buoy Center:
[https://www.ndbc.noaa.gov/](https://www.ndbc.noaa.gov/)

## 🖥 Tech Stack

- Python 🐍
- GitHub Actions ⚙️
- requests-oauthlib (X API v2, OAuth 1.0a) 🐦
- requests (NOAA / tide / sunset data) 🌐

## 🗂 File layout

```
.
├── main.py                       # Bot script
├── requirements.txt              # Python deps
├── .github/
│   └── workflows/
│       └── noaa-bot.yml          # GitHub Actions workflow
└── data/
    └── run-log.txt               # Append-only run history (auto-generated)
```

## 📜 License

MIT License — use it, fork it, share it!
