# 🚀 NASA TEMPO Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements-tempo.txt
```

### Step 2: Start the Server
```bash
python main.py
```

Or use the startup script:
```bash
./start-tempo.sh
```

### Step 3: View the Dashboard
Open `dashboard-tempo.html` in your web browser, or visit:
- **API Docs**: http://localhost:8000/docs
- **Summary**: http://localhost:8000/api/summary

---

## 🛰️ What is NASA TEMPO?

**TEMPO** (Tropospheric Emissions: Monitoring Pollution) is NASA's first space-based instrument to monitor air quality over North America **hourly** during daylight.

- **Launched**: April 2023
- **Orbit**: Geostationary (stays over North America)
- **Coverage**: Atlantic to Pacific, Yucatan to Canada
- **Resolution**: ~10 km, hourly updates
- **Measures**: NO₂, O₃, HCHO, Aerosols

---

## 📍 Monitored Cities

### 10 Major Cities Across North America:

| City | Country | City ID |
|------|---------|---------|
| New York City | 🇺🇸 USA | NYC001 |
| Los Angeles | 🇺🇸 USA | LAX001 |
| Chicago | 🇺🇸 USA | CHI001 |
| Houston | 🇺🇸 USA | HOU001 |
| Phoenix | 🇺🇸 USA | PHX001 |
| Miami | 🇺🇸 USA | MIA001 |
| Seattle | 🇺🇸 USA | SEA001 |
| Denver | 🇺🇸 USA | DEN001 |
| Toronto | 🇨🇦 Canada | TOR001 |
| Mexico City | 🇲🇽 Mexico | MEX001 |

---

## 🔌 Quick API Examples

### Get North America Summary
```bash
curl http://localhost:8000/api/summary
```

### Get All Cities
```bash
curl http://localhost:8000/api/cities
```

### Get New York City Data
```bash
curl http://localhost:8000/api/cities/NYC001
```

### Get 24-Hour History for Los Angeles
```bash
curl "http://localhost:8000/api/cities/LAX001/history?hours=24"
```

### Get 48-Hour Forecast for Mexico City
```bash
curl "http://localhost:8000/api/cities/MEX001/forecast?hours=48"
```

---

## 🌐 Data Sources

### 1. NASA TEMPO Satellite (Primary)
- Real-time satellite observations
- Hourly updates during daylight
- NO₂, O₃, HCHO measurements
- ~10 km spatial resolution

### 2. OpenAQ Ground Stations (Secondary)
- Free, real-time ground station data
- Automatic integration
- PM2.5, PM10, NO₂, O₃, SO₂, CO
- Validates satellite observations

---

## 📊 Understanding AQI

| AQI | Category | What to Do |
|-----|----------|------------|
| 0-50 | Good 🟢 | Enjoy outdoor activities! |
| 51-100 | Moderate 🟡 | Sensitive people be cautious |
| 101-150 | Unhealthy (Sensitive) 🟠 | Reduce outdoor activities |
| 151-200 | Unhealthy 🔴 | Avoid prolonged outdoor exertion |
| 201-300 | Very Unhealthy 🟣 | Stay indoors |
| 301+ | Hazardous 🟤 | Health emergency! |

---

## 🔐 Using Real NASA Data (Optional)

Want to use actual TEMPO satellite data?

1. **Create NASA Earthdata account**: https://urs.earthdata.nasa.gov/

2. **Create `.env` file** in `backend/`:
   ```
   NASA_EARTHDATA_USERNAME=your_username
   NASA_EARTHDATA_PASSWORD=your_password
   ```

3. **Install NetCDF libraries**:
   ```bash
   pip install xarray netCDF4 h5netcdf
   ```

4. **Access TEMPO data** at:
   https://asdc.larc.nasa.gov/data/TEMPO/

---

## 🎨 Features

✅ Real-time air quality for 10 major cities  
✅ NASA TEMPO satellite integration  
✅ OpenAQ ground station data  
✅ Hourly updates (matching TEMPO)  
✅ Historical data (up to 7 days)  
✅ 72-hour forecasts  
✅ AQI calculation & health advisories  
✅ Beautiful web dashboard  
✅ REST API for integration  

---

## 🧪 Test the API

Run the test script:
```bash
python test_api.py
```

---

## 🗂️ Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI application |
| `backend/requirements-tempo.txt` | Dependencies |
| `backend/app/services/tempo_data.py` | TEMPO data service |
| `dashboard-tempo.html` | Web dashboard |
| `start-tempo.sh` | Startup script |
| `NASA_TEMPO_README.md` | Full documentation |

---

## 🌟 Why TEMPO?

TEMPO is revolutionary because it:

1. **First of its kind**: First space-based hourly air quality monitor
2. **Geostationary**: Continuous coverage of North America
3. **High resolution**: Can see pollution at neighborhood scale
4. **Hourly updates**: Track pollution changes throughout the day
5. **Multiple pollutants**: NO₂, O₃, HCHO, aerosols

---

## 🎯 Use Cases

- **Public Health**: Monitor pollution in real-time
- **Research**: Study pollution patterns and trends
- **Policy**: Support environmental regulations
- **Education**: Learn about satellite remote sensing
- **Integration**: Build apps using the REST API

---

## 📚 Learn More

- **TEMPO Mission**: https://science.nasa.gov/mission/tempo/
- **TEMPO Data**: https://asdc.larc.nasa.gov/data/TEMPO/
- **NASA Earthdata**: https://www.earthdata.nasa.gov/
- **OpenAQ**: https://openaq.org/

---

## 🚀 Ready to Start?

```bash
./start-tempo.sh
```

Then open `dashboard-tempo.html` in your browser!

---

**🛰️ Powered by NASA TEMPO Satellite**

*Monitoring North America's air from space, every hour, every day.*
