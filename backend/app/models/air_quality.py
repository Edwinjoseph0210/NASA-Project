from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime

Base = declarative_base()

class AirQualityStation(Base):
    """Air quality monitoring station"""
    __tablename__ = "air_quality_stations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation = Column(Float)
    state = Column(String(50))
    county = Column(String(100))
    city = Column(String(100))
    address = Column(String(200))
    timezone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Geographic location as PostGIS geometry
    location = Column(Geometry('POINT', srid=4326))
    
    # Relationships
    readings = relationship("AirQualityReading", back_populates="station")

class AirQualityReading(Base):
    """Air quality measurement reading"""
    __tablename__ = "air_quality_readings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(UUID(as_uuid=True), ForeignKey("air_quality_stations.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Air quality parameters
    pm25 = Column(Float)  # PM2.5 (μg/m³)
    pm10 = Column(Float)  # PM10 (μg/m³)
    o3 = Column(Float)    # Ozone (ppb)
    no2 = Column(Float)   # Nitrogen Dioxide (ppb)
    so2 = Column(Float)   # Sulfur Dioxide (ppb)
    co = Column(Float)    # Carbon Monoxide (ppm)
    
    # Calculated AQI values
    aqi_pm25 = Column(Integer)
    aqi_pm10 = Column(Integer)
    aqi_o3 = Column(Integer)
    aqi_no2 = Column(Integer)
    aqi_so2 = Column(Integer)
    aqi_co = Column(Integer)
    overall_aqi = Column(Integer)
    
    # Data source
    data_source = Column(String(50))  # 'airnow', 'tempo', 'forecast'
    quality_flag = Column(String(20))  # 'good', 'moderate', 'unhealthy', etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    station = relationship("AirQualityStation", back_populates="readings")

class WeatherData(Base):
    """Weather forecast and observation data"""
    __tablename__ = "weather_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Weather parameters
    temperature = Column(Float)  # Celsius
    humidity = Column(Float)     # Percentage
    pressure = Column(Float)     # hPa
    wind_speed = Column(Float)   # m/s
    wind_direction = Column(Float)  # degrees
    visibility = Column(Float)   # km
    cloud_cover = Column(Float)  # percentage
    
    # Data source
    data_source = Column(String(50))  # 'nws', 'noaa'
    forecast_hours = Column(Integer)  # Hours ahead (0 for observations)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class TEMPOData(Base):
    """NASA TEMPO satellite data"""
    __tablename__ = "tempo_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # TEMPO measurements
    no2_column = Column(Float)      # NO2 column density
    o3_column = Column(Float)       # O3 column density
    hcho_column = Column(Float)     # HCHO column density
    cloud_fraction = Column(Float)  # Cloud fraction
    
    # Data quality
    quality_flag = Column(String(20))
    solar_zenith_angle = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ForecastModel(Base):
    """ML model metadata and performance metrics"""
    __tablename__ = "forecast_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    model_type = Column(String(50))  # 'xgboost', 'lstm', 'random_forest'
    
    # Model parameters
    parameters = Column(Text)  # JSON string of model parameters
    training_data_start = Column(DateTime)
    training_data_end = Column(DateTime)
    
    # Performance metrics
    rmse = Column(Float)
    mae = Column(Float)
    r2_score = Column(Float)
    
    # Model file path
    model_path = Column(String(200))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserAlert(Base):
    """User alert subscriptions"""
    __tablename__ = "user_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(100))  # Could be email, device ID, etc.
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Alert thresholds
    pm25_threshold = Column(Float)
    o3_threshold = Column(Float)
    no2_threshold = Column(Float)
    aqi_threshold = Column(Integer)
    
    # Notification preferences
    web_push_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=False)
    sms_enabled = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
