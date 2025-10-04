# Ernakulam Air Quality Monitor

A simplified, real-time air quality monitoring system focused specifically on **Ernakulam District, Kerala, India**.

## Overview

This application monitors air pollution levels across 6 key locations in Ernakulam district:

1. **Kochi City Center** (MG Road) - Urban area
2. **Kakkanad IT Park** (Infopark) - Industrial/IT hub
3. **Fort Kochi** (Beach area) - Coastal zone
4. **Aluva** (Metro Station) - Urban transport hub
5. **Thrippunithura** (Hill Palace Road) - Residential area
6. **Edappally** (NH Bypass) - High traffic zone

## Features

- ✅ Real-time air quality data for Ernakulam district
- ✅ Monitoring of key pollutants (PM2.5, PM10, NO2, O3, SO2, CO)
- ✅ Air Quality Index (AQI) calculation
- ✅ Health advisories based on pollution levels
- ✅ Historical data tracking (up to 7 days)
- ✅ 24-72 hour pollution forecasts
- ✅ District-wide pollution summary
- ✅ Simple REST API (no database required)

## Monitored Pollutants

| Pollutant | Description | Health Impact |
|-----------|-------------|---------------|
| **PM2.5** | Fine particulate matter (< 2.5 μm) | Respiratory issues, heart disease |
| **PM10** | Coarse particulate matter (< 10 μm) | Breathing problems, lung irritation |
| **NO2** | Nitrogen Dioxide | Respiratory inflammation |
| **O3** | Ground-level Ozone | Breathing difficulties, asthma |
| **SO2** | Sulfur Dioxide | Respiratory problems |
| **CO** | Carbon Monoxide | Reduces oxygen delivery to organs |

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements-simple.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - API Root: http://localhost:8000
   - Health Check: http://localhost:8000/health

## API Endpoints

### 1. District Summary
Get overall air quality summary for Ernakulam district.

```bash
GET /api/summary
```

**Response:**
```json
{
  "district": "Ernakulam",
  "timestamp": "2024-10-04T05:56:25.123456",
  "overall_aqi": 65,
  "aqi_category": "Moderate",
  "health_advisory": "Air quality is acceptable...",
  "averages": {
    "pm25": 45.2,
    "pm10": 75.8,
    "no2": 35.1
  },
  "worst_location": {
    "name": "Edappally",
    "aqi": 95
  },
  "best_location": {
    "name": "Fort Kochi",
    "aqi": 42
  },
  "total_stations": 6,
  "stations": [...]
}
```

### 2. All Stations
Get current readings from all monitoring stations.

```bash
GET /api/stations
```

### 3. Station Details
Get current reading for a specific station.

```bash
GET /api/stations/{station_id}
```

**Example:**
```bash
GET /api/stations/EKM001
```

**Available Station IDs:**
- `EKM001` - Kochi City Center
- `EKM002` - Kakkanad IT Park
- `EKM003` - Fort Kochi
- `EKM004` - Aluva
- `EKM005` - Thrippunithura
- `EKM006` - Edappally

### 4. Historical Data
Get historical pollution data for a station.

```bash
GET /api/stations/{station_id}/history?hours=24
```

**Parameters:**
- `hours`: Number of hours of historical data (1-168, default: 24)

**Example:**
```bash
GET /api/stations/EKM001/history?hours=48
```

### 5. Forecast
Get pollution forecast for a station.

```bash
GET /api/stations/{station_id}/forecast?hours=24
```

**Parameters:**
- `hours`: Forecast horizon in hours (1-72, default: 24)

**Example:**
```bash
GET /api/stations/EKM002/forecast?hours=48
```

## Understanding AQI (Air Quality Index)

| AQI Range | Category | Health Impact | Color Code |
|-----------|----------|---------------|------------|
| 0-50 | Good | Minimal impact | Green |
| 51-100 | Moderate | Acceptable; sensitive groups may be affected | Yellow |
| 101-150 | Unhealthy for Sensitive Groups | Sensitive groups may experience health effects | Orange |
| 151-200 | Unhealthy | Everyone may begin to experience health effects | Red |
| 201-300 | Very Unhealthy | Health alert: everyone may experience more serious effects | Purple |
| 301+ | Hazardous | Health warnings of emergency conditions | Maroon |

## Example Usage

### Using cURL

**Get district summary:**
```bash
curl http://localhost:8000/api/summary
```

**Get Kochi City Center data:**
```bash
curl http://localhost:8000/api/stations/EKM001
```

**Get 48-hour history for Kakkanad:**
```bash
curl "http://localhost:8000/api/stations/EKM002/history?hours=48"
```

**Get 24-hour forecast for Fort Kochi:**
```bash
curl "http://localhost:8000/api/stations/EKM003/forecast?hours=24"
```

### Using Python

```python
import requests

# Get district summary
response = requests.get("http://localhost:8000/api/summary")
data = response.json()

print(f"District: {data['district']}")
print(f"Overall AQI: {data['overall_aqi']} ({data['aqi_category']})")
print(f"Health Advisory: {data['health_advisory']}")
print(f"\nWorst Location: {data['worst_location']['name']} (AQI: {data['worst_location']['aqi']})")
print(f"Best Location: {data['best_location']['name']} (AQI: {data['best_location']['aqi']})")
```

### Using JavaScript (Browser/Node.js)

```javascript
// Get all stations
fetch('http://localhost:8000/api/stations')
  .then(response => response.json())
  .then(data => {
    console.log(`Monitoring ${data.total_stations} stations in ${data.district}`);
    data.stations.forEach(station => {
      console.log(`${station.station_name}: AQI ${station.aqi} (${station.aqi_category})`);
    });
  });
```

## Data Generation

**Note:** This simplified version uses **mock data** that simulates realistic pollution patterns for Ernakulam district. The data includes:

- Time-based variations (higher pollution during peak traffic hours: 7-10 AM, 5-8 PM)
- Location-based variations (industrial areas have higher pollution than coastal areas)
- Random fluctuations to simulate real-world conditions

### Pollution Patterns by Location Type

- **Urban areas** (Kochi, Aluva): Moderate pollution
- **Industrial zones** (Kakkanad IT Park): Higher pollution
- **Coastal areas** (Fort Kochi): Lower pollution
- **Residential areas** (Thrippunithura): Moderate pollution
- **Traffic zones** (Edappally): Highest pollution

## Project Structure

```
backend/
├── main.py                          # Main FastAPI application
├── requirements-simple.txt          # Minimal dependencies
└── app/
    ├── core/
    │   └── config.py               # Configuration (Ernakulam coordinates)
    └── services/
        └── ernakulam_data.py       # Data service for Ernakulam
```

## Future Enhancements

To make this production-ready with real data, you could:

1. **Integrate with real APIs:**
   - Central Pollution Control Board (CPCB) API
   - Kerala State Pollution Control Board data
   - NASA TEMPO satellite data
   - OpenWeatherMap Air Pollution API

2. **Add database:**
   - PostgreSQL for storing historical data
   - TimescaleDB for time-series optimization

3. **Implement ML forecasting:**
   - LSTM models for pollution prediction
   - Weather data integration
   - Traffic pattern analysis

4. **Add notifications:**
   - SMS/Email alerts for high pollution
   - Push notifications for mobile apps

5. **Create frontend:**
   - Interactive map of Ernakulam
   - Real-time charts and graphs
   - Mobile-responsive design

## Health Recommendations by AQI

### Good (0-50)
- ✅ Ideal for outdoor activities
- ✅ No restrictions needed

### Moderate (51-100)
- ⚠️ Sensitive individuals should limit prolonged outdoor exertion
- ✅ Generally acceptable for most people

### Unhealthy for Sensitive Groups (101-150)
- ⚠️ Children, elderly, and people with respiratory conditions should limit outdoor activities
- ⚠️ Everyone else should reduce prolonged outdoor exertion

### Unhealthy (151-200)
- 🚫 Everyone should avoid prolonged outdoor exertion
- 🚫 Sensitive groups should avoid all outdoor activities

### Very Unhealthy (201-300)
- 🚫 Everyone should avoid all outdoor activities
- 🏠 Stay indoors with air purifiers if possible

### Hazardous (301+)
- 🚨 Health emergency - everyone should remain indoors
- 🚨 Use N95 masks if you must go outside

## Contributing

This is a simplified demonstration project. For production use:
- Replace mock data with real API integrations
- Add proper error handling and logging
- Implement data validation and sanitization
- Add authentication and rate limiting
- Set up monitoring and alerting

## License

This project is for educational and demonstration purposes.

## Contact & Support

For questions or issues, please refer to the API documentation at `/docs` when the server is running.

---

**Made for Ernakulam District, Kerala 🌴**
