import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.air_quality import AirQualityStation, AirQualityReading, TEMPOData, WeatherData
from app.schemas import AirQualityParameter, DataSource

logger = logging.getLogger(__name__)

class DataIngestionService:
    """Service for ingesting data from various sources"""
    
    def __init__(self):
        self.session = None
        self.nasa_credentials = None
        
    async def initialize(self):
        """Initialize the service"""
        self.session = aiohttp.ClientSession()
        
        # Initialize NASA Earthdata credentials
        if settings.NASA_EARTHDATA_USERNAME and settings.NASA_EARTHDATA_PASSWORD:
            self.nasa_credentials = aiohttp.BasicAuth(
                settings.NASA_EARTHDATA_USERNAME,
                settings.NASA_EARTHDATA_PASSWORD
            )
    
    async def close(self):
        """Close the service"""
        if self.session:
            await self.session.close()
    
    async def fetch_airnow_data(self) -> Dict[str, Any]:
        """Fetch data from AirNow API"""
        try:
            if not settings.AIRNOW_API_KEY:
                logger.warning("AirNow API key not configured")
                return {"stations_updated": 0, "error": "API key not configured"}
            
            # Fetch current observations
            url = f"{settings.AIRNOW_API_BASE_URL}zipCode/query"
            params = {
                "format": "application/json",
                "API_KEY": settings.AIRNOW_API_KEY,
                "date": datetime.utcnow().strftime("%Y-%m-%dT%H-0000")
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return await self._process_airnow_data(data)
                else:
                    logger.error(f"AirNow API error: {response.status}")
                    return {"stations_updated": 0, "error": f"API error: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error fetching AirNow data: {str(e)}")
            return {"stations_updated": 0, "error": str(e)}
    
    async def _process_airnow_data(self, data: List[Dict]) -> Dict[str, Any]:
        """Process AirNow API response data"""
        stations_updated = 0
        
        for observation in data:
            try:
                # Extract station information
                station_data = {
                    "station_id": observation.get("SiteCode"),
                    "name": observation.get("SiteName"),
                    "latitude": float(observation.get("Latitude", 0)),
                    "longitude": float(observation.get("Longitude", 0)),
                    "state": observation.get("StateCode"),
                    "county": observation.get("CountyName"),
                    "city": observation.get("CityName"),
                    "timezone": observation.get("TimeZone"),
                    "is_active": True
                }
                
                # Extract air quality readings
                readings = []
                timestamp = datetime.fromisoformat(observation.get("DateObserved", "").replace("Z", "+00:00"))
                
                # Process each pollutant
                for pollutant in ["PM2.5", "PM10", "O3", "NO2", "SO2", "CO"]:
                    if pollutant in observation:
                        reading_data = {
                            "timestamp": timestamp,
                            "data_source": DataSource.AIRNOW,
                            "quality_flag": observation.get("Category", {}).get("Name", "Unknown")
                        }
                        
                        # Map pollutant names to database fields
                        pollutant_map = {
                            "PM2.5": ("pm25", "AQI"),
                            "PM10": ("pm10", "AQI"),
                            "O3": ("o3", "AQI"),
                            "NO2": ("no2", "AQI"),
                            "SO2": ("so2", "AQI"),
                            "CO": ("co", "AQI")
                        }
                        
                        if pollutant in pollutant_map:
                            field_name, aqi_field = pollutant_map[pollutant]
                            reading_data[field_name] = float(observation[pollutant])
                            reading_data[f"aqi_{field_name}"] = observation.get(aqi_field)
                
                # Calculate overall AQI
                aqi_values = [v for v in [
                    observation.get("AQI"),
                    observation.get("AQI_PM25"),
                    observation.get("AQI_PM10"),
                    observation.get("AQI_O3"),
                    observation.get("AQI_NO2"),
                    observation.get("AQI_SO2"),
                    observation.get("AQI_CO")
                ] if v is not None]
                
                if aqi_values:
                    reading_data["overall_aqi"] = max(aqi_values)
                
                stations_updated += 1
                
            except Exception as e:
                logger.error(f"Error processing AirNow observation: {str(e)}")
                continue
        
        return {
            "stations_updated": stations_updated,
            "timestamp": datetime.utcnow()
        }
    
    async def fetch_tempo_data(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Fetch NASA TEMPO satellite data"""
        try:
            if not self.nasa_credentials:
                logger.warning("NASA Earthdata credentials not configured")
                return {"data_points": 0, "error": "Credentials not configured"}
            
            # TEMPO data URL structure
            base_url = settings.TEMPO_API_BASE_URL
            
            # Generate time range for data requests
            current_time = start_time
            data_points = 0
            
            while current_time < end_time:
                # TEMPO data is typically available hourly
                year = current_time.year
                month = current_time.month
                day = current_time.day
                hour = current_time.hour
                
                # Construct data URL (this is a simplified example)
                data_url = f"{base_url}{year:04d}/{month:02d}/{day:02d}/TEMPO_L2_NO2_{year:04d}{month:02d}{day:02d}T{hour:02d}0000Z.nc"
                
                try:
                    async with self.session.get(data_url, auth=self.nasa_credentials) as response:
                        if response.status == 200:
                            # Process NetCDF data (simplified)
                            tempo_data = await self._process_tempo_netcdf(await response.read())
                            data_points += len(tempo_data)
                        else:
                            logger.debug(f"TEMPO data not available for {current_time}")
                            
                except Exception as e:
                    logger.debug(f"Error fetching TEMPO data for {current_time}: {str(e)}")
                
                current_time += timedelta(hours=1)
            
            return {
                "data_points": data_points,
                "time_range": {
                    "start": start_time,
                    "end": end_time
                },
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error fetching TEMPO data: {str(e)}")
            return {"data_points": 0, "error": str(e)}
    
    async def _process_tempo_netcdf(self, netcdf_data: bytes) -> List[Dict]:
        """Process TEMPO NetCDF data"""
        # This is a simplified implementation
        # In practice, you would use xarray or netCDF4 to read the data
        try:
            import xarray as xr
            import io
            
            # Load NetCDF data
            ds = xr.open_dataset(io.BytesIO(netcdf_data))
            
            # Extract relevant variables
            tempo_data = []
            
            # Get coordinates
            lats = ds.latitude.values
            lons = ds.longitude.values
            
            # Get NO2 column data
            no2_data = ds.no2_column.values
            
            # Process each data point
            for i in range(len(lats)):
                for j in range(len(lons)):
                    if not (lats[i] == 0 and lons[j] == 0):  # Skip invalid coordinates
                        tempo_data.append({
                            "latitude": float(lats[i]),
                            "longitude": float(lons[j]),
                            "timestamp": datetime.utcnow(),
                            "no2_column": float(no2_data[i, j]) if no2_data[i, j] is not None else None,
                            "quality_flag": "good"  # Simplified
                        })
            
            return tempo_data
            
        except ImportError:
            logger.error("xarray not available for NetCDF processing")
            return []
        except Exception as e:
            logger.error(f"Error processing TEMPO NetCDF: {str(e)}")
            return []
    
    async def fetch_weather_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Fetch weather data from NWS/NOAA API"""
        try:
            # Get weather station for coordinates
            station_url = f"{settings.NWS_API_BASE_URL}/points/{latitude},{longitude}"
            
            async with self.session.get(station_url) as response:
                if response.status == 200:
                    station_data = await response.json()
                    
                    # Get current conditions
                    forecast_url = station_data["properties"]["forecast"]
                    
                    async with self.session.get(forecast_url) as forecast_response:
                        if forecast_response.status == 200:
                            forecast_data = await forecast_response.json()
                            return await self._process_weather_data(forecast_data, latitude, longitude)
                        else:
                            logger.error(f"Weather forecast API error: {forecast_response.status}")
                            return {"error": f"Forecast API error: {forecast_response.status}"}
                else:
                    logger.error(f"Weather station API error: {response.status}")
                    return {"error": f"Station API error: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return {"error": str(e)}
    
    async def _process_weather_data(self, data: Dict, latitude: float, longitude: float) -> Dict[str, Any]:
        """Process NWS weather data"""
        try:
            periods = data.get("properties", {}).get("periods", [])
            
            weather_data = []
            for period in periods:
                weather_data.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": datetime.fromisoformat(period["startTime"].replace("Z", "+00:00")),
                    "temperature": period.get("temperature"),
                    "humidity": period.get("relativeHumidity", {}).get("value"),
                    "pressure": period.get("pressure", {}).get("value"),
                    "wind_speed": period.get("windSpeed"),
                    "wind_direction": period.get("windDirection"),
                    "visibility": period.get("visibility"),
                    "cloud_cover": None,  # Not always available
                    "data_source": "nws",
                    "forecast_hours": 0  # Current conditions
                })
            
            return {
                "weather_data": weather_data,
                "location": {"latitude": latitude, "longitude": longitude},
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error processing weather data: {str(e)}")
            return {"error": str(e)}
    
    async def store_data_in_database(self, data: Dict[str, Any], db: Session):
        """Store ingested data in the database"""
        try:
            # Store stations
            if "stations" in data:
                for station_data in data["stations"]:
                    existing_station = db.query(AirQualityStation).filter(
                        AirQualityStation.station_id == station_data["station_id"]
                    ).first()
                    
                    if not existing_station:
                        station = AirQualityStation(**station_data)
                        db.add(station)
                    else:
                        # Update existing station
                        for key, value in station_data.items():
                            setattr(existing_station, key, value)
            
            # Store readings
            if "readings" in data:
                for reading_data in data["readings"]:
                    reading = AirQualityReading(**reading_data)
                    db.add(reading)
            
            # Store TEMPO data
            if "tempo_data" in data:
                for tempo_data in data["tempo_data"]:
                    tempo = TEMPOData(**tempo_data)
                    db.add(tempo)
            
            # Store weather data
            if "weather_data" in data:
                for weather_data in data["weather_data"]:
                    weather = WeatherData(**weather_data)
                    db.add(weather)
            
            db.commit()
            return {"success": True, "timestamp": datetime.utcnow()}
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing data in database: {str(e)}")
            return {"success": False, "error": str(e)}
