# 🛰️ NASA TEMPO Air Quality Monitor

Real-time air quality monitoring for **North America** using NASA's TEMPO (Tropospheric Emissions: Monitoring Pollution) satellite data.

## 🌍 About NASA TEMPO

**TEMPO** is NASA's first Earth Venture Instrument mission dedicated to monitoring air quality. Launched in April 2023, TEMPO provides:

- **Hourly measurements** during daylight hours
- **High spatial resolution** (~10 km)
- **Geostationary orbit** for continuous North American coverage
- **Coverage area**: Atlantic to Pacific, Yucatan Peninsula to Canadian oil sands

### Measured Pollutants
- **NO₂** (Nitrogen Dioxide)
- **O₃** (Ozone)
- **HCHO** (Formaldehyde)
- **Aerosols** (Particulate matter)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements-tempo.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **View the dashboard:**
   Open `dashboard-tempo.html` in your browser

## 📍 Monitored Cities

The application monitors 10 major cities across North America:

### United States 🇺🇸
1. **New York City** - Major metro area
2. **Los Angeles** - High pollution, smog
3. **Chicago** - Industrial hub
4. **Houston** - Industrial/petrochemical
5. **Phoenix** - Desert environment
6. **Miami** - Coastal city
7. **Seattle** - Pacific Northwest
8. **Denver** - High altitude

### Canada 🇨🇦
9. **Toronto** - Major Canadian metro

### Mexico 🇲🇽
10. **Mexico City** - One of world's largest cities

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### 1. Root Information
```bash
GET /
```

Returns API information and TEMPO satellite details.

### 2. North America Summary
```bash
GET /api/summary
```

**Response:**
```json
{
  "region": "North America",
  "coverage": "TEMPO Satellite Coverage Area",
  "overall_aqi": 65,
  "aqi_category": "Moderate",
  "averages": {
    "pm25": 35.2,
    "pm10": 60.8,
    "no2": 40.1
  },
  "worst_location": {
    "name": "Los Angeles, USA",
    "aqi": 95
  },
  "best_location": {
    "name": "Seattle, USA",
    "aqi": 42
  },
  "total_cities": 10,
  "cities": [...],
  "tempo_info": {
    "instrument": "NASA TEMPO",
    "orbit": "Geostationary",
    "coverage": "North America",
    "temporal_resolution": "Hourly during daylight",
    "spatial_resolution": "~10 km",
    "measured_pollutants": ["NO2", "O3", "HCHO", "Aerosols"]
  }
}
```

### 3. All Cities
```bash
GET /api/cities
```

Returns current air quality data for all monitored cities.

### 4. Specific City
```bash
GET /api/cities/{city_id}
```

**Available City IDs:**
- `NYC001` - New York City
- `LAX001` - Los Angeles
- `CHI001` - Chicago
- `HOU001` - Houston
- `TOR001` - Toronto
- `MEX001` - Mexico City
- `PHX001` - Phoenix
- `MIA001` - Miami
- `SEA001` - Seattle
- `DEN001` - Denver

**Example:**
```bash
curl http://localhost:8000/api/cities/NYC001
```

### 5. Historical Data
```bash
GET /api/cities/{city_id}/history?hours=24
```

**Parameters:**
- `hours`: Number of hours (1-168, default: 24)

**Example:**
```bash
curl "http://localhost:8000/api/cities/LAX001/history?hours=48"
```

### 6. Forecast
```bash
GET /api/cities/{city_id}/forecast?hours=24
```

**Parameters:**
- `hours`: Forecast horizon (1-72, default: 24)

**Example:**
```bash
curl "http://localhost:8000/api/cities/MEX001/forecast?hours=48"
```

## 🔐 Using Real NASA TEMPO Data

To access actual NASA TEMPO satellite data:

### 1. Create NASA Earthdata Account
Sign up at: https://urs.earthdata.nasa.gov/

### 2. Set Environment Variables
Create a `.env` file in the `backend` directory:

```bash
NASA_EARTHDATA_USERNAME=your_username
NASA_EARTHDATA_PASSWORD=your_password
```

### 3. Install NetCDF Libraries
Uncomment these lines in `requirements-tempo.txt`:
```bash
xarray==2023.12.0
netCDF4==1.6.5
h5netcdf==1.3.0
```

Then reinstall:
```bash
pip install -r requirements-tempo.txt
```

### 4. Access TEMPO Data Products

**Available Products:**
- `TEMPO_NO2_L2_V03` - Nitrogen Dioxide
- `TEMPO_O3TOT_L2_V03` - Total Ozone
- `TEMPO_HCHO_L2_V03` - Formaldehyde

**Data Location:**
```
https://asdc.larc.nasa.gov/data/TEMPO/
```

## 🌐 Real Ground Station Data

The application integrates with **OpenAQ** for real ground station measurements:

- **Free API** (no key required)
- **Global coverage** including North America
- **Real-time data** from government monitoring stations
- **Automatic fallback** to simulated data if unavailable

## 📊 Understanding AQI

| AQI Range | Category | Color | Health Impact |
|-----------|----------|-------|---------------|
| 0-50 | Good | 🟢 Green | Minimal impact |
| 51-100 | Moderate | 🟡 Yellow | Acceptable; sensitive groups may be affected |
| 101-150 | Unhealthy (Sensitive) | 🟠 Orange | Sensitive groups may experience effects |
| 151-200 | Unhealthy | 🔴 Red | Everyone may begin to experience effects |
| 201-300 | Very Unhealthy | 🟣 Purple | Health alert for everyone |
| 301+ | Hazardous | 🟤 Maroon | Health emergency |

## 🧪 Testing

Run the test script:
```bash
python test_api.py
```

This will test all endpoints and display sample data.

## 📁 Project Structure

```
NASA/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── requirements-tempo.txt       # Dependencies
│   └── app/
│       ├── core/
│       │   └── config.py           # Configuration
│       └── services/
│           └── tempo_data.py       # TEMPO data service
├── dashboard-tempo.html             # Web dashboard
├── test_api.py                     # API tests
└── NASA_TEMPO_README.md            # This file
```

## 🔬 Data Sources

### Primary: NASA TEMPO Satellite
- **Launch**: April 7, 2023
- **Orbit**: Geostationary (35,786 km altitude)
- **Coverage**: North America
- **Resolution**: Hourly, ~10 km spatial
- **Data Products**: NO₂, O₃, HCHO, Aerosols

### Secondary: OpenAQ Ground Stations
- **Type**: Ground-based monitoring stations
- **Coverage**: Global (including North America)
- **Update Frequency**: Varies by station (typically hourly)
- **Data**: PM2.5, PM10, NO₂, O₃, SO₂, CO

## 🌟 Features

- ✅ Real-time air quality monitoring
- ✅ 10 major North American cities
- ✅ Integration with OpenAQ for ground truth data
- ✅ Hourly updates (matching TEMPO's observation frequency)
- ✅ Historical data tracking
- ✅ 72-hour forecasts
- ✅ AQI calculation and health advisories
- ✅ Beautiful web dashboard
- ✅ REST API for integration
- ✅ Support for real NASA TEMPO data (with credentials)

## 🎯 Use Cases

1. **Public Health Monitoring**
   - Track pollution levels in major cities
   - Issue health advisories
   - Monitor vulnerable populations

2. **Research**
   - Study pollution patterns
   - Analyze temporal variations
   - Compare urban vs. coastal areas

3. **Policy Making**
   - Assess air quality trends
   - Evaluate pollution control measures
   - Support environmental regulations

4. **Education**
   - Learn about satellite remote sensing
   - Understand air quality science
   - Explore NASA Earth observation data

## 🔄 Data Update Frequency

- **TEMPO Satellite**: Hourly during daylight (6 AM - 8 PM local time)
- **OpenAQ Ground Stations**: Varies (typically hourly)
- **API Cache**: Refreshes every 60 minutes
- **Dashboard**: Auto-refreshes every 10 minutes

## 🌐 TEMPO Coverage Map

```
         CANADA 🇨🇦
    ┌─────────────────────┐
    │                     │
    │   ┌─────────┐       │
    │   │ Toronto │       │
    │   └─────────┘       │
    │                     │
    └─────────────────────┘
         USA 🇺🇸
    ┌─────────────────────┐
    │ Seattle             │
    │         Denver      │
    │                     │
    │ Los Angeles  Phoenix│
    │         Houston     │
    │              Miami  │
    │ New York            │
    │ Chicago             │
    └─────────────────────┘
         MEXICO 🇲🇽
    ┌─────────────────────┐
    │                     │
    │   Mexico City       │
    │                     │
    └─────────────────────┘
```

## 📚 Additional Resources

- **NASA TEMPO Mission**: https://science.nasa.gov/mission/tempo/
- **TEMPO Data**: https://asdc.larc.nasa.gov/data/TEMPO/
- **NASA Earthdata**: https://www.earthdata.nasa.gov/
- **OpenAQ API**: https://docs.openaq.org/
- **EPA AQI Guide**: https://www.airnow.gov/aqi/

## 🤝 Contributing

To enhance this project:

1. **Add More Cities**: Edit `NORTH_AMERICA_CITIES` in `tempo_data.py`
2. **Integrate Real TEMPO Data**: Implement NetCDF processing
3. **Add ML Forecasting**: Train models on historical data
4. **Create Mobile App**: Use the REST API
5. **Add Notifications**: Email/SMS alerts for high pollution

## 📄 License

This project uses publicly available NASA data and is for educational purposes.

## 🙏 Acknowledgments

- **NASA** for the TEMPO satellite mission
- **OpenAQ** for free air quality data
- **ASDC** (Atmospheric Science Data Center) for data hosting

---

**🛰️ Powered by NASA TEMPO Satellite Data**

*Monitoring North America's air quality from space, hourly, every day.*
