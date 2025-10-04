# 🚀 Quick Start Guide - Ernakulam Air Quality Monitor

## Get Started in 3 Steps!

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements-simple.txt
```

### Step 2: Start the Server
```bash
python main.py
```

Or use the startup script:
```bash
./start-ernakulam.sh
```

### Step 3: View the Dashboard
Open `dashboard.html` in your web browser, or visit:
- **API Docs**: http://localhost:8000/docs
- **District Summary**: http://localhost:8000/api/summary

---

## What You'll See

### 6 Monitoring Stations in Ernakulam:
1. **Kochi City Center** (EKM001) - MG Road area
2. **Kakkanad IT Park** (EKM002) - Infopark
3. **Fort Kochi** (EKM003) - Beach area
4. **Aluva** (EKM004) - Metro Station
5. **Thrippunithura** (EKM005) - Hill Palace Road
6. **Edappally** (EKM006) - NH Bypass

### Monitored Pollutants:
- **PM2.5** - Fine particles
- **PM10** - Coarse particles
- **NO2** - Nitrogen dioxide
- **O3** - Ozone
- **SO2** - Sulfur dioxide
- **CO** - Carbon monoxide

---

## Quick API Examples

### Get District Summary
```bash
curl http://localhost:8000/api/summary
```

### Get All Stations
```bash
curl http://localhost:8000/api/stations
```

### Get Specific Station (Kochi)
```bash
curl http://localhost:8000/api/stations/EKM001
```

### Get 24-Hour History
```bash
curl "http://localhost:8000/api/stations/EKM001/history?hours=24"
```

### Get 48-Hour Forecast
```bash
curl "http://localhost:8000/api/stations/EKM001/forecast?hours=48"
```

---

## Test the API

Run the test script:
```bash
python test_api.py
```

This will test all endpoints and show you sample data!

---

## Understanding AQI Values

| AQI | Category | Color | What to Do |
|-----|----------|-------|------------|
| 0-50 | Good | 🟢 Green | Enjoy outdoor activities! |
| 51-100 | Moderate | 🟡 Yellow | Sensitive people should be cautious |
| 101-150 | Unhealthy (Sensitive) | 🟠 Orange | Reduce prolonged outdoor activities |
| 151-200 | Unhealthy | 🔴 Red | Avoid prolonged outdoor exertion |
| 201-300 | Very Unhealthy | 🟣 Purple | Stay indoors |
| 301+ | Hazardous | 🟤 Maroon | Health emergency! |

---

## Project Structure

```
NASA/
├── backend/
│   ├── main.py                    # Main API server
│   ├── requirements-simple.txt    # Dependencies
│   └── app/
│       ├── core/
│       │   └── config.py         # Ernakulam config
│       └── services/
│           └── ernakulam_data.py # Data service
├── dashboard.html                 # Web dashboard
├── test_api.py                   # API test script
├── start-ernakulam.sh            # Startup script
├── ERNAKULAM_README.md           # Full documentation
└── QUICKSTART.md                 # This file!
```

---

## Troubleshooting

### Server won't start?
- Make sure you're in the `backend` directory
- Check if port 8000 is already in use
- Install dependencies: `pip install -r requirements-simple.txt`

### Dashboard shows error?
- Make sure the server is running
- Check the API URL in dashboard.html (should be http://localhost:8000)
- Open browser console (F12) to see detailed errors

### Need help?
- Check the full documentation: `ERNAKULAM_README.md`
- View API docs: http://localhost:8000/docs
- Run tests: `python test_api.py`

---

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **View the Dashboard**: Open `dashboard.html` in your browser
3. **Test Endpoints**: Run `python test_api.py`
4. **Read Full Docs**: Check `ERNAKULAM_README.md`

---

**Happy Monitoring! 🌍**

Made for Ernakulam District, Kerala 🌴
