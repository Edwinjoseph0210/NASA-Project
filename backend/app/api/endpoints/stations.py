from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.models.air_quality import AirQualityStation, AirQualityReading
from app.services.data_ingestion import DataIngestionService
from app.schemas.station import StationResponse, StationListResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stations", response_model=StationListResponse)
async def get_stations(
    lat: Optional[float] = Query(None, description="Latitude for location-based filtering"),
    lon: Optional[float] = Query(None, description="Longitude for location-based filtering"),
    radius: Optional[float] = Query(50.0, description="Radius in kilometers for location filtering"),
    state: Optional[str] = Query(None, description="Filter by state"),
    active_only: bool = Query(True, description="Only return active stations"),
    db: Session = Depends(get_db)
):
    """
    Get air quality monitoring stations.
    
    Returns a list of air quality monitoring stations, optionally filtered by location,
    state, or activity status.
    """
    try:
        query = db.query(AirQualityStation)
        
        if active_only:
            query = query.filter(AirQualityStation.is_active == True)
        
        if state:
            query = query.filter(AirQualityStation.state == state.upper())
        
        # Location-based filtering using PostGIS
        if lat and lon and radius:
            # Convert radius from km to degrees (approximate)
            radius_degrees = radius / 111.0  # Rough conversion
            query = query.filter(
                AirQualityStation.latitude.between(lat - radius_degrees, lat + radius_degrees),
                AirQualityStation.longitude.between(lon - radius_degrees, lon + radius_degrees)
            )
        
        stations = query.all()
        
        return StationListResponse(
            stations=[StationResponse.from_orm(station) for station in stations],
            total_count=len(stations),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error fetching stations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stations/{station_id}", response_model=StationResponse)
async def get_station(
    station_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific air quality monitoring station by ID.
    """
    try:
        station = db.query(AirQualityStation).filter(
            AirQualityStation.station_id == station_id
        ).first()
        
        if not station:
            raise HTTPException(status_code=404, detail="Station not found")
        
        return StationResponse.from_orm(station)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching station {station_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stations/{station_id}/readings")
async def get_station_readings(
    station_id: str,
    hours: int = Query(24, description="Number of hours of data to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get recent air quality readings for a specific station.
    """
    try:
        station = db.query(AirQualityStation).filter(
            AirQualityStation.station_id == station_id
        ).first()
        
        if not station:
            raise HTTPException(status_code=404, detail="Station not found")
        
        # Calculate time range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        readings = db.query(AirQualityReading).filter(
            AirQualityReading.station_id == station.id,
            AirQualityReading.timestamp >= start_time,
            AirQualityReading.timestamp <= end_time
        ).order_by(AirQualityReading.timestamp.desc()).all()
        
        return {
            "station_id": station_id,
            "station_name": station.name,
            "readings": [
                {
                    "timestamp": reading.timestamp,
                    "pm25": reading.pm25,
                    "pm10": reading.pm10,
                    "o3": reading.o3,
                    "no2": reading.no2,
                    "so2": reading.so2,
                    "co": reading.co,
                    "overall_aqi": reading.overall_aqi,
                    "data_source": reading.data_source,
                    "quality_flag": reading.quality_flag
                }
                for reading in readings
            ],
            "time_range": {
                "start": start_time,
                "end": end_time
            },
            "total_readings": len(readings)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching readings for station {station_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/stations/refresh")
async def refresh_stations_data(db: Session = Depends(get_db)):
    """
    Trigger a refresh of station data from external APIs.
    """
    try:
        ingestion_service = DataIngestionService()
        result = await ingestion_service.fetch_airnow_data()
        
        return {
            "message": "Station data refresh initiated",
            "stations_updated": result.get("stations_updated", 0),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error refreshing station data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to refresh station data")
