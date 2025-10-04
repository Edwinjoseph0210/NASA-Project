from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AirQualityParameter(str, Enum):
    """Air quality parameters"""
    PM25 = "pm25"
    PM10 = "pm10"
    O3 = "o3"
    NO2 = "no2"
    SO2 = "so2"
    CO = "co"
    AQI = "aqi"

class DataSource(str, Enum):
    """Data sources"""
    AIRNOW = "airnow"
    TEMPO = "tempo"
    FORECAST = "forecast"
    FUSED = "fused"

class StationResponse(BaseModel):
    """Air quality station response"""
    id: str
    station_id: str
    name: str
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    state: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    timezone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StationListResponse(BaseModel):
    """List of air quality stations"""
    stations: List[StationResponse]
    total_count: int
    timestamp: datetime

class ForecastRequest(BaseModel):
    """Air quality forecast request"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    forecast_hours: int = Field(24, ge=1, le=72, description="Forecast horizon in hours")
    include_confidence: bool = Field(False, description="Include confidence intervals")

class ForecastDataPoint(BaseModel):
    """Single forecast data point"""
    timestamp: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    o3: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    aqi: Optional[int] = None
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None

class ForecastResponse(BaseModel):
    """Air quality forecast response"""
    location: Dict[str, float]
    forecast_hours: int
    generated_at: datetime
    forecast_data: List[ForecastDataPoint]
    model_info: Dict[str, Any]
    data_sources: List[str]

class MapDataRequest(BaseModel):
    """Map data request"""
    bounds: Dict[str, float] = Field(..., description="Geographic bounds (north, south, east, west)")
    resolution: float = Field(0.1, ge=0.01, le=1.0, description="Grid resolution in degrees")
    parameter: AirQualityParameter = Field(AirQualityParameter.AQI, description="Air quality parameter")
    timestamp: Optional[datetime] = Field(None, description="Specific timestamp (defaults to latest)")

class MapDataPoint(BaseModel):
    """Single map data point"""
    latitude: float
    longitude: float
    value: float
    confidence: Optional[float] = None

class MapDataResponse(BaseModel):
    """Map data response"""
    bounds: Dict[str, float]
    resolution: float
    parameter: AirQualityParameter
    timestamp: datetime
    data: List[MapDataPoint]
    generated_at: datetime

class AlertRequest(BaseModel):
    """Alert request"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    parameter: AirQualityParameter
    threshold: float
    message: Optional[str] = None
    user_id: Optional[str] = None

class AlertResponse(BaseModel):
    """Alert response"""
    id: str
    location: Dict[str, float]
    parameter: AirQualityParameter
    threshold: float
    current_value: float
    severity: str
    message: str
    timestamp: datetime
    expires_at: Optional[datetime] = None

class AlertSubscription(BaseModel):
    """Alert subscription"""
    user_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    pm25_threshold: Optional[float] = Field(None, ge=0)
    o3_threshold: Optional[float] = Field(None, ge=0)
    no2_threshold: Optional[float] = Field(None, ge=0)
    aqi_threshold: Optional[int] = Field(None, ge=0, le=500)
    web_push_enabled: bool = Field(True)
    email_enabled: bool = Field(False)
    sms_enabled: bool = Field(False)

class WeatherData(BaseModel):
    """Weather data"""
    latitude: float
    longitude: float
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    visibility: Optional[float] = None
    cloud_cover: Optional[float] = None
    data_source: str

class TEMPOData(BaseModel):
    """NASA TEMPO satellite data"""
    latitude: float
    longitude: float
    timestamp: datetime
    no2_column: Optional[float] = None
    o3_column: Optional[float] = None
    hcho_column: Optional[float] = None
    cloud_fraction: Optional[float] = None
    quality_flag: Optional[str] = None
    solar_zenith_angle: Optional[float] = None
