# AirAware API Documentation

## Overview

The AirAware API provides real-time air quality data, forecasts, and alerts using NASA TEMPO satellite data, ground-based measurements, and machine learning models.

**Base URL**: `https://api.airaware.com/api/v1`  
**API Version**: 1.0.0  
**Authentication**: None required for public endpoints

## Quick Start

```bash
# Get current air quality for a location
curl "https://api.airaware.com/api/v1/forecast/current?lat=40.7128&lon=-74.0060"

# Get air quality stations
curl "https://api.airaware.com/api/v1/stations?state=NY"

# Get map data for visualization
curl -X POST "https://api.airaware.com/api/v1/map" \
  -H "Content-Type: application/json" \
  -d '{
    "bounds": {
      "north": 45.0,
      "south": 25.0,
      "east": -65.0,
      "west": -125.0
    },
    "parameter": "aqi",
    "resolution": 0.1
  }'
```

## Authentication

Most endpoints are publicly accessible. For advanced features and higher rate limits, API keys may be required in the future.

## Rate Limits

- **Public endpoints**: 100 requests per minute per IP
- **Map endpoints**: 50 requests per minute per IP
- **Forecast endpoints**: 200 requests per minute per IP

## Endpoints

### Stations

#### GET /stations

Get air quality monitoring stations.

**Parameters:**
- `lat` (float, optional): Latitude for location-based filtering
- `lon` (float, optional): Longitude for location-based filtering
- `radius` (float, optional): Radius in kilometers (default: 50.0)
- `state` (string, optional): Filter by state code
- `active_only` (boolean, optional): Only return active stations (default: true)

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/stations?lat=40.7128&lon=-74.0060&radius=25&state=NY"
```

**Example Response:**
```json
{
  "stations": [
    {
      "id": "uuid-here",
      "station_id": "NYC001",
      "name": "New York City - Manhattan",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "state": "NY",
      "city": "New York",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total_count": 1,
  "timestamp": "2024-01-15T12:00:00Z"
}
```

#### GET /stations/{station_id}

Get a specific air quality monitoring station.

**Parameters:**
- `station_id` (string, required): Station identifier

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/stations/NYC001"
```

#### GET /stations/{station_id}/readings

Get recent air quality readings for a specific station.

**Parameters:**
- `station_id` (string, required): Station identifier
- `hours` (integer, optional): Number of hours of data to retrieve (default: 24)

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/stations/NYC001/readings?hours=48"
```

**Example Response:**
```json
{
  "station_id": "NYC001",
  "station_name": "New York City - Manhattan",
  "readings": [
    {
      "timestamp": "2024-01-15T12:00:00Z",
      "pm25": 15.2,
      "pm10": 25.8,
      "o3": 42.1,
      "no2": 18.7,
      "so2": 3.2,
      "co": 0.8,
      "overall_aqi": 52,
      "data_source": "airnow",
      "quality_flag": "Good"
    }
  ],
  "time_range": {
    "start": "2024-01-14T12:00:00Z",
    "end": "2024-01-15T12:00:00Z"
  },
  "total_readings": 24
}
```

### Forecast

#### POST /forecast

Get air quality forecast for a specific location.

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "forecast_hours": 24,
  "include_confidence": false
}
```

**Parameters:**
- `latitude` (float, required): Latitude (-90 to 90)
- `longitude` (float, required): Longitude (-180 to 180)
- `forecast_hours` (integer, optional): Forecast horizon in hours (1-72, default: 24)
- `include_confidence` (boolean, optional): Include confidence intervals (default: false)

**Example Response:**
```json
{
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "forecast_hours": 24,
  "generated_at": "2024-01-15T12:00:00Z",
  "forecast_data": [
    {
      "timestamp": "2024-01-15T13:00:00Z",
      "pm25": 16.2,
      "o3": 43.5,
      "no2": 19.1,
      "aqi": 55,
      "confidence_lower": 12.8,
      "confidence_upper": 19.6
    }
  ],
  "model_info": {
    "models_loaded": 3,
    "available_parameters": ["pm25", "o3", "no2"],
    "model_path": "./ml/models/",
    "last_updated": "2024-01-15T11:00:00Z"
  },
  "data_sources": ["airnow", "tempo", "weather"]
}
```

#### GET /forecast/{lat}/{lon}

Get air quality forecast for specific coordinates.

**Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude
- `hours` (integer, optional): Forecast horizon in hours (max 72)
- `include_confidence` (boolean, optional): Include confidence intervals

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/forecast/40.7128/-74.0060?hours=48&include_confidence=true"
```

#### GET /forecast/current

Get current air quality conditions for a location.

**Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/forecast/current?lat=40.7128&lon=-74.0060"
```

### Map Data

#### POST /map

Get gridded air quality data for map visualization.

**Request Body:**
```json
{
  "bounds": {
    "north": 45.0,
    "south": 25.0,
    "east": -65.0,
    "west": -125.0
  },
  "resolution": 0.1,
  "parameter": "aqi",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

**Parameters:**
- `bounds` (object, required): Geographic bounds
  - `north` (float): Northern boundary
  - `south` (float): Southern boundary
  - `east` (float): Eastern boundary
  - `west` (float): Western boundary
- `resolution` (float, optional): Grid resolution in degrees (0.01-1.0, default: 0.1)
- `parameter` (string, optional): Air quality parameter (default: "aqi")
- `timestamp` (string, optional): Specific timestamp (defaults to latest)

**Example Response:**
```json
{
  "bounds": {
    "north": 45.0,
    "south": 25.0,
    "east": -65.0,
    "west": -125.0
  },
  "resolution": 0.1,
  "parameter": "aqi",
  "timestamp": "2024-01-15T12:00:00Z",
  "data": [
    {
      "latitude": 40.0,
      "longitude": -74.0,
      "value": 52.3,
      "confidence": 0.85
    }
  ],
  "generated_at": "2024-01-15T12:00:00Z"
}
```

#### GET /map/heatmap

Get heatmap data for a geographic region.

**Parameters:**
- `north` (float, required): Northern boundary
- `south` (float, required): Southern boundary
- `east` (float, required): Eastern boundary
- `west` (float, required): Western boundary
- `parameter` (string, optional): Air quality parameter (default: "aqi")
- `resolution` (float, optional): Grid resolution in degrees (default: 0.1)

#### GET /map/tempo-coverage

Get NASA TEMPO satellite coverage data for a region.

**Parameters:**
- `north` (float, required): Northern boundary
- `south` (float, required): Southern boundary
- `east` (float, required): Eastern boundary
- `west` (float, required): Western boundary

### Alerts

#### GET /alerts

Get active air quality alerts for a region.

**Parameters:**
- `lat` (float, optional): Latitude for location filtering
- `lon` (float, optional): Longitude for location filtering
- `radius` (float, optional): Radius in kilometers (default: 50.0)
- `hours` (integer, optional): Hours of alerts to retrieve (default: 24)

**Example Request:**
```bash
curl "https://api.airaware.com/api/v1/alerts?lat=40.7128&lon=-74.0060&radius=25"
```

**Example Response:**
```json
[
  {
    "id": "alert-123",
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "parameter": "pm25",
    "threshold": 35.4,
    "current_value": 45.2,
    "severity": "Unhealthy for Sensitive Groups",
    "message": "PM2.5 levels in New York are elevated",
    "timestamp": "2024-01-15T12:00:00Z",
    "expires_at": "2024-01-15T18:00:00Z"
  }
]
```

#### POST /alerts/subscribe

Subscribe to air quality alerts for a location.

**Request Body:**
```json
{
  "user_id": "user123",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "pm25_threshold": 35.4,
  "o3_threshold": 0.070,
  "no2_threshold": 0.100,
  "aqi_threshold": 100,
  "web_push_enabled": true,
  "email_enabled": false,
  "sms_enabled": false
}
```

#### DELETE /alerts/subscribe/{subscription_id}

Cancel an alert subscription.

**Parameters:**
- `subscription_id` (string, required): Subscription identifier

#### GET /alerts/subscribe/{user_id}

Get all alert subscriptions for a user.

**Parameters:**
- `user_id` (string, required): User identifier

#### GET /alerts/thresholds

Get standard air quality alert thresholds.

**Example Response:**
```json
{
  "aqi_thresholds": {
    "good": {"min": 0, "max": 50, "color": "#00e400"},
    "moderate": {"min": 51, "max": 100, "color": "#ffff00"},
    "unhealthy_sensitive": {"min": 101, "max": 150, "color": "#ff7e00"},
    "unhealthy": {"min": 151, "max": 200, "color": "#ff0000"},
    "very_unhealthy": {"min": 201, "max": 300, "color": "#8f3f97"},
    "hazardous": {"min": 301, "max": 500, "color": "#7e0023"}
  },
  "parameter_thresholds": {
    "pm25": {"unhealthy": 35.4, "very_unhealthy": 55.4},
    "o3": {"unhealthy": 0.164, "very_unhealthy": 0.204},
    "no2": {"unhealthy": 0.360, "very_unhealthy": 0.649}
  },
  "timestamp": "2024-01-15T12:00:00Z"
}
```

## Data Models

### Air Quality Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| `pm25` | μg/m³ | Fine particulate matter (PM2.5) |
| `pm10` | μg/m³ | Coarse particulate matter (PM10) |
| `o3` | ppb | Ozone |
| `no2` | ppb | Nitrogen dioxide |
| `so2` | ppb | Sulfur dioxide |
| `co` | ppm | Carbon monoxide |
| `aqi` | index | Air Quality Index |

### AQI Categories

| AQI Range | Category | Color | Health Advisory |
|-----------|----------|-------|-----------------|
| 0-50 | Good | Green | Air quality is satisfactory |
| 51-100 | Moderate | Yellow | Air quality is acceptable for most people |
| 101-150 | Unhealthy for Sensitive Groups | Orange | Sensitive people should limit outdoor activities |
| 151-200 | Unhealthy | Red | Everyone should limit outdoor activities |
| 201-300 | Very Unhealthy | Purple | Avoid outdoor activities |
| 301+ | Hazardous | Maroon | Stay indoors and avoid outdoor activities |

## Error Handling

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `422` - Unprocessable Entity (validation error)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

### Common Error Codes

- `VALIDATION_ERROR` - Request parameters are invalid
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `DATA_UNAVAILABLE` - Requested data is not available
- `SERVICE_UNAVAILABLE` - Service is temporarily unavailable

## SDKs and Libraries

### Python

```python
import requests

# Get current air quality
response = requests.get(
    "https://api.airaware.com/api/v1/forecast/current",
    params={"lat": 40.7128, "lon": -74.0060}
)
data = response.json()
print(f"Current AQI: {data['aqi']}")
```

### JavaScript

```javascript
// Get air quality forecast
const response = await fetch(
  'https://api.airaware.com/api/v1/forecast/current?lat=40.7128&lon=-74.0060'
);
const data = await response.json();
console.log(`Current AQI: ${data.aqi}`);
```

### cURL Examples

```bash
# Get stations in New York
curl "https://api.airaware.com/api/v1/stations?state=NY"

# Get forecast for coordinates
curl "https://api.airaware.com/api/v1/forecast/40.7128/-74.0060?hours=48"

# Subscribe to alerts
curl -X POST "https://api.airaware.com/api/v1/alerts/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "aqi_threshold": 100,
    "web_push_enabled": true
  }'
```

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release
- Air quality stations endpoint
- Forecast endpoint
- Map data endpoint
- Alerts endpoint
- NASA TEMPO integration
- AirNow integration
- Machine learning forecasting

## Support

- **Documentation**: https://docs.airaware.com
- **Status Page**: https://status.airaware.com
- **Support Email**: support@airaware.com
- **GitHub Issues**: https://github.com/airaware/api/issues
